import optuna
from umap import UMAP
from hdbscan import HDBSCAN
import numpy as np
from sentence_transformers import SentenceTransformer

class TopicModel:
    def __init__(self, 
                 docs: list[str], 
                 min_cluster: int, max_cluster: int, 
                 prob_threshold: float = 0.1,
                 max_evals: int = 20, 
                 seed: int = 42423) -> None:
        """Initializes the TopicModel class
        
        Args:
          docs: the documents

        Returns:
          None
        """

        assert min_cluster < max_cluster, "min_cluster must be smaller than max_cluster"
        self.docs = docs
        self._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embeddings = self._embedding_model.encode(docs)
        self.best_model = {"cost": None, "ntopics": None, "umap": None, "cluster": None}
        self.min_cluster = min_cluster
        self.max_cluster = max_cluster
        self.prob_threshold = prob_threshold
        self.max_evals = max_evals
        self.seed = seed

    def is_better_model(self, cost: float) -> bool:
        """Returns True if the cost is better than the current best model
        
        Args:
          cost: the cost of the model
          
        Returns:
          True if the cost is better than the current best model
        """
        if self.best_model["cost"] is None:
            return True
        else:
            return cost < self.best_model["cost"]
        
    def set_best_model(self, cost: float, ntopics: int, umap: UMAP, cluster: HDBSCAN) -> None:
        """Sets the best model
        
        Args:
          cost: the cost of the model
          ntopics: the number of topics
          umap: the umap model
          cluster: the cluster model
          
        Returns:
          None
        """
        self.best_model["cost"] = cost
        self.best_model["ntopics"] = ntopics
        self.best_model["umap"] = umap
        self.best_model["cluster"] = cluster

    def compute_cost(self, clusters: HDBSCAN, out_of_range_cluster_penalty: float = 0.15) -> tuple[int, float]:
        """Computes the cost function for the model
        
        Args:
          clusters: the fitted cluster model
          label_lower: the lower bound for the number of clusters
          label_upper: the upper bound for the number of clusters
          prob_threshold: the probability threshold for the cluster
          out_of_range_cluster_penalty: the penalty for the number of clusters outside the desired range
          
        Returns:
          label_count: the number of clusters
          cost: the cost of the model
        """
        cluster_labels = clusters.labels_
        label_count = len(np.unique(cluster_labels)) - 1
        total_num = len(clusters.labels_)
        cost = (np.count_nonzero(clusters.probabilities_ < self.prob_threshold) / total_num)
        
        # 15% penalty on the cost function if outside the desired range
        # for the number of clusters
        if (label_count < self.min_cluster) | (label_count > self.max_cluster):
            penalty = out_of_range_cluster_penalty
        else:
            penalty = 0.
        
        cost = cost + penalty
        
        return label_count, cost

    def objective(self, trial, X: np.ndarray) -> float:
        """The objective function for the model
        
        Args:
          trial: the optuna trial
          X: the embeddings

        Returns:
          cost: the cost of the model
        """
        # search space
        n_neighbors = trial.suggest_int("n_neighbors", 4, 12)
        n_components = trial.suggest_int("n_components", 3, 12)
        min_cluster_size = trial.suggest_int("min_cluster_size", 5, 15)
        min_samples = trial.suggest_int("min_samples", 2, 4)

        # setup models
        dim_reducer = UMAP(n_neighbors=n_neighbors, n_components=n_components, metric="cosine", random_state=self.seed)
        cluster = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples)
        
        # fit model
        dim_reducer.fit(X)
        cluster.fit_predict(dim_reducer.embedding_)

        label_count, cost = self.compute_cost(cluster, 0.15)

        if self.is_better_model(cost):
            self.set_best_model(cost, label_count, dim_reducer, cluster)

        return cost
    
    def optim(self) -> dict:
        """Optimizes the models

        Returns:
          best_params: the best parameters for the model
        """
        study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=self.seed))
        study.optimize(lambda trial: self.objective(trial, self.embeddings), n_trials=self.max_evals)
        return study.best_params
    
    def get_labels(self) -> np.ndarray:
        """Returns the labels for the best model

        Returns:
          labels: the labels for the best model
        """
        return self.best_model["cluster"].labels_


if __name__ == "__main__":
  from sklearn.datasets import fetch_20newsgroups
  from umap import UMAP
  from sentence_transformers import SentenceTransformer

  newsgroups_train = fetch_20newsgroups(subset='train')

  # only keep computer related topics
  comp_docs = []
  targets = []
  for doc, target in zip(newsgroups_train.data, newsgroups_train.target):
    if newsgroups_train.target_names[target].startswith("comp"):
      comp_docs.append(doc)
      targets.append(target)

  model = TopicModel(comp_docs)
  best_params = model.optim()
  print(f"\n\n #### BEST PARAMETERS ({model.best_model['ntopics']} clusters):\n {best_params}")

  unique_labels = np.unique(targets)
  print(f"\n\n #### TRUE LABELS:\n {len(unique_labels)}")

