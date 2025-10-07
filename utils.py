import os
from dotenv import load_dotenv
from langchain.text_splitter import MarkdownTextSplitter
from langchain_postgres import PGVector
from langchain.schema import Document
import os
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from typing import List
from langchain_core.embeddings import Embeddings
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


llm = init_chat_model(
    model="gemini-2.5-flash-lite", model_provider="google_genai", temperature=0.5
)


class CustomGoogleGenAIEmbeddings(Embeddings):
    def __init__(
        self, model: str = "gemini-embedding-001", output_dimensionality: int = 768
    ):
        self.client = genai.Client()
        self.model = model
        self.output_dimensionality = output_dimensionality

    def embed_query(self, text: str) -> list[float]:
        result = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=self.output_dimensionality
            ),
        )
        [embedding_obj] = result.embeddings
        return embedding_obj.values

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        result = self.client.models.embed_content(
            model=self.model,
            contents=texts,
            config=types.EmbedContentConfig(
                output_dimensionality=self.output_dimensionality
            ),
        )
        return [embedding.values for embedding in result.embeddings]


embedding_engine = CustomGoogleGenAIEmbeddings(
    model="gemini-embedding-001", output_dimensionality=768
)
