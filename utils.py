import os
from dotenv import load_dotenv
from langchain.text_splitter import MarkdownTextSplitter
from langchain_postgres import PGVector
from langchain.schema import Document
import os
from langchain.chat_models import init_chat_model
from typing import List
from langchain_core.embeddings import Embeddings
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm = init_chat_model(
    model="gemini-2.5-flash-lite", model_provider="google_genai", temperature=0.5
)


class NvidiaOpenAIEmbeddings_BGE_M3(Embeddings):
    def __init__(self, api_key: str, base_url: str, model: str = "baai/bge-m3"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            input=texts,
            model=self.model,
            encoding_format="float",
            extra_body={"truncate": "NONE"},
        )
        return [data.embedding for data in response.data]

    def embed_query(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            input=[text],
            model=self.model,
            encoding_format="float",
            extra_body={"truncate": "NONE"},
        )
        return response.data[0].embedding



embedding_engine = NvidiaOpenAIEmbeddings_BGE_M3(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1",
    model="baai/bge-m3",
)
