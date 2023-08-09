from functools import partial
import numpy as np
from hdbscan import HDBSCAN
from umap import UMAP
from hyperopt import fmin, tpe, STATUS_OK, space_eval, Trials, choice
from sentence_transformers import SentenceTransformer

from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.representation import KeyBERTInspired

class TopicModel:
    def __init__(self) -> None:
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.embeddings = None
        self.optimizer = HyperparamOptimizer
        self.model = None
        self.params = None
        self.random_state = 321456 # want that settable or just take current datetime as int
    
    def embed(self, txts: list[str]) -> None:
        self.embeddings = self.embedder.encode(txts)

    def search_hyperparams(self,  min_max_cluster=(10, 50), max_evals=50):
        
        search_space = {
            "n_neighbors": choice("n_neighbors", range(3, 12)),
            "n_components": choice("n_components", range(3, 12)),
            "min_cluster_size": choice("min_cluster_size", range(4, 15)),
            "min_samples": choice("min_samples", range(2, 4)),
            "random_state": self.random_state
        }
        min_cluster, max_cluster = min_max_cluster
        Optimizer = self.optimizer(doc_embeddings=self.embeddings, prob_threshold=0.05)

        Optimizer.bayesian_search(search_space, min_cluster, max_cluster, max_evals)
        self.params = Optimizer.best_params
    
    def fit(self) -> None:
        umap_model = UMAP(
            n_neighbors=self.params["n_neighbors"],
            n_components=self.params["n_components"], 
            metric="cosine", 
            random_state=self.params["random_state"]
        )

        hdbscan_model = HDBSCAN(
            min_cluster_size=self.params["min_cluster_size"], 
            min_samples=self.params["min_samples"]
        )

        vectorizer_model = CountVectorizer(min_df=0.01, max_df=0.7)
        representation_model = KeyBERTInspired(random_state=self.random_state)

        self.model = BERTopic(
            embedding_model=self.embedder, 
            umap_model=umap_model, 
            hdbscan_model=hdbscan_model,
            vectorizer_model=vectorizer_model,
            representation_model=representation_model,
            calculate_probabilities=False,
            verbose=True
        )


    

class HyperparamOptimizer:
    # adapted from https://github.com/dborrelli/chat-intents
    def __init__(self, doc_embeddings: np.ndarray, prob_threshold: float) -> None:
        self.doc_embeddings = doc_embeddings
        self.prob_threshold = prob_threshold
        self.search_space = None
        self.best_params = None
        self.best_dim_reduction = None
        self.best_clusters = None
        self.trials = None
        """
        Initialize hyperparameter optimization object

        Arguments:
            doc_embeddings: numpy array of document embeddings created using desired model for class instance
            prob_threshold: float, probability threshold to use for deciding what cluster labels are considered low
                            confidence. Passed to method `score_clusters`
            search_space:   parameter space to search. dictionary with keys: n_neighbours, n_components,
                            min_cluster_size, min_samples
            best_params:    UMAP + HDBSCAN hyperparameters associated with the best performance after performing
                            bayesian search using 'bayesian_search' method
            best_clusters:  HDBSCAN clusters and labels associated with the best performance after performing bayesian
                            search using the 'bayesian_search' method
            trials:         hyperopt trials saved from bayesian search using 'bayesian_search' method
        """

    def generate_clusters(self,
                          n_neighbors: int,
                          n_components: int,
                          min_cluster_size: int,
                          min_samples: int = None,
                          random_state: int = None) -> HDBSCAN:
        """
        Generate HDBSCAN clusters from UMAP embeddings of embeddings

        Arguments:
            n_neighbors: float, UMAP n_neighbors parameter representing the
                         size of local neighborhood (in terms of number of
                         neighboring sample points) used
            n_components: int, UMAP n_components parameter representing
                          dimension of the space to embed into
            min_cluster_size: int, HDBSCAN parameter minimum size of clusters
            min_samples: int, HDBSCAN parameter representing the number of
                         samples in a neighbourhood for a point to be
                         considered a core point
            random_state: int, random seed to use in UMAP process

        Returns:
            umap_embeddings: UMAP object
            clusters: HDBSCAN clustering object storing results of fit to embeddings

        """

        umap_embeddings = (UMAP(n_neighbors=n_neighbors,
                                     n_components=n_components,
                                     metric='cosine',
                                     random_state=random_state)
                               .fit_transform(self.doc_embeddings))

        clusters = (HDBSCAN(min_cluster_size=min_cluster_size,
                                    min_samples=min_samples,
                                    metric='euclidean',
                                    gen_min_span_tree=True,
                                    cluster_selection_method='eom')
                           .fit(umap_embeddings))

        # would make sense to also return the umap object
        return umap_embeddings, clusters


    @staticmethod
    def score_clusters(clusters, prob_threshold=0.05):
        """
        Returns the label count and cost of a given clustering

        Arguments:
            clusters: HDBSCAN clustering object
            prob_threshold: float, probability threshold to use for deciding
                            what cluster labels are considered low confidence

        Returns:
            label_count: int, number of unique cluster labels, including noise
            cost: float, fraction of data points whose cluster assignment has
                  a probability below cutoff threshold
        """

        cluster_labels = clusters.labels_
        label_count = len(np.unique(cluster_labels))
        total_num = len(clusters.labels_)
        cost = (np.count_nonzero(clusters.probabilities_ < prob_threshold)
                / total_num)

        return label_count, cost

    def _objective(self, params: dict, label_lower: int, label_upper: int):
        """
        Objective function for hyperopt to minimize

        Arguments:
            params: dict, contains keys for 'n_neighbors', 'n_components',
                   'min_cluster_size', 'min_samples', 'random_state' and
                   their values to use for evaluation
            label_lower: int, lower end of range of number of expected clusters
            label_upper: int, upper end of range of number of expected clusters

        Returns:
            loss: cost function result incorporating penalties for falling
                  outside desired range for number of clusters
            label_count: int, number of unique cluster labels, including noise
            status: string, hypoeropt status

        """

        embeds, clusters = self.generate_clusters(n_neighbors=params['n_neighbors'],
                                          n_components=params['n_components'],
                                          min_cluster_size=params['min_cluster_size'],
                                          min_samples=params['min_samples'],
                                          random_state=params['random_state'])

        label_count, cost = self.score_clusters(clusters, self.prob_threshold)

        # 15% penalty on the cost function if outside the desired range
        # for the number of clusters
        if (label_count < label_lower) | (label_count > label_upper):
            penalty = 0.15
        else:
            penalty = 0

        loss = cost + penalty

        return {'loss': loss, 'label_count': label_count, 'status': STATUS_OK}

    def bayesian_search(self,
                        space,
                        label_lower,
                        label_upper,
                        max_evals=100):
        """
        Perform bayesian search on hyperparameter space using hyperopt

        Arguments:
            space: dict, contains keys for 'n_neighbors', 'n_components',
                   'min_cluster_size', 'min_samples', and 'random_state' and
                   values that use built-in hyperopt functions to define
                   search spaces for each
            label_lower: int, lower end of range of number of expected clusters
            label_upper: int, upper end of range of number of expected clusters
            max_evals: int, maximum number of parameter combinations to try

        Saves the following to instance variables:
            best_params: dict, contains keys for 'n_neighbors', 'n_components',
                   'min_cluster_size', 'min_samples', and 'random_state' and
                   values associated with lowest cost scenario tested
            best_dim_reduction: UMAP object associated with lowest cost scenario
            best_clusters: HDBSCAN object associated with lowest cost scenario
                           tested
            trials: hyperopt trials object for search

        """

        trials = Trials()
        fmin_objective = partial(self._objective,
                                 label_lower=label_lower,
                                 label_upper=label_upper)

        best = fmin(fmin_objective,
                    space=space,
                    algo=tpe.suggest,
                    max_evals=max_evals,
                    trials=trials)

        best_params = space_eval(space, best)
        print('Best params:')
        print(best_params)
        print(f"Number of clusters (including noise): {trials.best_trial['result']['label_count']}")

        best_umap, best_clusters = self.generate_clusters(
            n_neighbors=best_params['n_neighbors'],
            n_components=best_params['n_components'],
            min_cluster_size=best_params['min_cluster_size'],
            min_samples=best_params['min_samples'],
            random_state=best_params['random_state']
        )

        self.best_params = best_params
        self.best_dim_reduction = best_umap
        self.best_clusters = best_clusters
        self.trials = trials
        # return best_params, best_clusters, trials


if __name__ == "__main__":
    print("bababa")