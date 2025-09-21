from langchain_postgres import PGVector
from langchain_core.tools import tool
from rich import print
from dotenv import load_dotenv
import os
load_dotenv()

from utils import embedding_engine


SUPABASE_PG_CONN_URL = os.getenv("DB_URI")
vector_store = PGVector(
    embeddings=embedding_engine,
    collection_name="bd_travel_bot",
    connection=SUPABASE_PG_CONN_URL,
    use_jsonb=True,
)

@tool()
def knowledge_retriever(query: str):
    """Create a knowledge retriever from the vector store."""
    
    vec_retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 5}
    )
    
    docs = vec_retriever.invoke(query)

    return [doc.page_content for doc in docs]