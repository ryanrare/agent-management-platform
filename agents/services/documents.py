from langchain_openai import OpenAIEmbeddings
import numpy as np
from agents.models import Document
from django.conf import settings


class DocumentRetriever:
    def __init__(self, agent=None):
        self.agent = agent
        self.embedder = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

    def search(self, query, top_k=5):
        query_vector = self.embedder.embed_query(query)

        docs_qs = Document.objects.all()

        results = []
        for doc in docs_qs:
            if not doc.embedding:
                continue
            sim = self.cosine_similarity(query_vector, doc.embedding)
            results.append((sim, doc))

        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for sim, doc in results[:top_k]]

    @staticmethod
    def cosine_similarity(a, b):
        a, b = np.array(a), np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
