from langchain.prompts import ChatPromptTemplate
import os
from langchain.chat_models import ChatOpenAI
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import dot_score
import numpy as np


KEY = os.getenv("OPENAI_KEY")  
ORG = os.getenv("OPENAI_ORG")

PROMPTS = {
    "SYSTEM": "You are a highly intelligent question answering bot. You take Question and Context as input and return the answer from the Paragraph. Retain as much information as needed to answer the question at a later time. The answer must only address the question. Use a descriptive and objective tone. If Context lacks the answer you must only return 'NOT FOUND', nothing else.",
    "HUMAN": "Question: \n```{question}```\n\nContext: \n```{context}```"
}

TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", PROMPTS["SYSTEM"]),
    ("human", PROMPTS["HUMAN"])
])

class QAProcessor():
    def __init__(self, key: str = KEY, org: str = ORG, prompt_template: ChatPromptTemplate = TEMPLATE, max_tokens: int = 256) -> None:
        """Initializes the QAProcessor
      
        Args:
            key: the openai api key
            org: the openai organization key
            prompt_template: the chat prompt template
            max_tokens: the maximum number of tokens to generate
          
        Returns:
            None
        """
        self.llm = ChatOpenAI(openai_api_key=KEY, openai_organization=ORG, max_tokens=max_tokens)
        self.prompt_template = prompt_template

    def ask_question_to_txt(self, question: str, txt: str, debug: bool = False) -> str:
        """Asks a question to a text

        Args:
            question: the question
            txt: the text
            debug: if True, does return the txt without an API call

        Returns:
            the answer, 'NOT FOUND' if the answer cannot be provided from the text
        """
        msg = self.prompt_template.format_messages(question=question, context=txt)
      
        if debug:
            return txt
        response = self.llm(messages=msg)
        return response.content 

def check_non_answers(answers: list[str]) -> list[bool]:
    """Checks if answers are a non-answer

    Args:
        answers: list of strings containing the answers

    Returns:
        True if the answer is a non-answer
    """
    #has_not_found = "NOT FOUND" in answer | "not found" in answer

    NONE_ANSWERS = [
        "The given context does not",
        "The passage does not",
        "The given text does not",
        "The context does not"
    ]
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    # crop answers to 100 chars
    cropped_answers = [answer[:100] for answer in answers if len(answer) > 200]

    embeddings = embedder.encode(cropped_answers, normalize_embeddings=True)
    embeddings_none_answers = embedder.encode(NONE_ANSWERS, normalize_embeddings=True)

    # calculate centroid of none answers
    centroid = np.mean(embeddings_none_answers, axis=0)

    # calculate cosine similarity between centroid and embeddings
    similarities = np.dot(embeddings, centroid)

    # if the similarity is above 0.8, it is a non-answer
    return list[similarities > 0.1]


if __name__ == "__main__":
    question = "What is the use case of the app?"
    context = "AI-Powered Presentation Generator which allows you to create presentations in 1 click. Slideforge is an AI-powered presentation generator that simplifies the process of creating impactful presentations. With just one click, Slideforge empowers users to transform their ideas into polished presentations effortlessly. Whether you provide a short prompt or a more detailed one (up to 400 characters), Slideforge swiftly generates a fully-fledged .pptx presentation. In a matter of 15-30 seconds, you'll have a slideshow with informative content, a logical structure, and beautiful images relevant to each slide. Experience the convenience of Slideforge, save valuable time, and enjoy the seamless creation of lovely presentations."
    qa = QAProcessor()
    answer = qa.ask_question_to_txt(question, context)
    print(answer)