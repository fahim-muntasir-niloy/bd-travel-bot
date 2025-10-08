import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from typing import List
from langchain_postgres import PGVector
from rich import print

load_dotenv()

from utils import embedding_engine

folder_path = "web_scraping"

# Get all .txt files recursively from folder and subfolders
txt_files = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".txt"):
            txt_files.append(os.path.join(root, file))

all_pages = []  # To store pages from all files

for txt_file_path in txt_files:
    # print(f"Processing {txt_file_path}...")
    loader = TextLoader(file_path=txt_file_path, encoding="utf-8")

    # Load the documents for this file and append to `all_pages`
    for doc in loader.lazy_load():
        all_pages.append(doc)
    # print(f"Processing {txt_file_path}...")
    loader = TextLoader(file_path=txt_file_path, encoding="utf-8")

    # Load the documents for this file and append to `all_pages`
    for doc in loader.lazy_load():
        all_pages.append(doc)

# Output all collected pages
print(f"Total pages loaded: {len(all_pages)}")

# Splitting document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000, chunk_overlap=300, separators=["\n"]
)

splits = text_splitter.split_documents(all_pages)
print(f"Total chunks created: {len(splits)}")

SUPABASE_PG_CONN_URL = os.getenv("DB_URI")

vector_store = PGVector(
    embeddings=embedding_engine,
    collection_name="bd_travel_bot",
    connection=SUPABASE_PG_CONN_URL,
    use_jsonb=True,
)
print("PGVector Store is loaded.")

# push embedding to collection
print("Adding documents to vector store...")
for i in range(0, len(splits), 200):
    chunk = splits[i : i + 200]
    try:
        # Add the chunk to the vector store
        vector_store.add_documents(documents=chunk)
        print(f"Chunk {i // 200 + 1}/{(len(splits) + 200) // 200} added successfully")
    except Exception as e:
        print(f"Error adding chunk {i // 200}: {e}")
        continue


# vec_retriever = vector_store.as_retriever(
#     search_type="similarity", search_kwargs={"k": 5}
# )

# docs = vec_retriever.invoke("khulnay ki ghure dekha jay?")
# # print(docs)
# for doc in docs:
#     print(f"Document metadata: {doc.metadata}\n")
#     print(f"Document Content: {doc.page_content}")
#     print("---------------------------------------------------------------\n")
