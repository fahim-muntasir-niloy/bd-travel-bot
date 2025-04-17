
import os

# import streamlit as st

from fastapi import FastAPI
from langserve import add_routes


from langchain_astradb import AstraDBVectorStore

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace, HuggingFaceEmbeddings

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI


from dotenv import load_dotenv
load_dotenv()
# credentials
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

os.environ['LANGSMITH_TRACING_V2']="true"
os.environ['LANGSMITH_ENDPOINT']="https://api.smith.langchain.com"
os.environ['LANGCHAIN_API_KEY']=os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGSMITH_PROJECT']="travel_bot_bd"



hf_embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    show_progress=True,
)

# as the vector data is already stored in Astra DB
vector_store = AstraDBVectorStore(
    embedding = hf_embedding_model,
    collection_name="test_travel_kb",
    autodetect_collection=True,
    api_endpoint=ASTRA_DB_API_ENDPOINT, 
    token=ASTRA_DB_APPLICATION_TOKEN,
    namespace="default_keyspace"
)   

retriever = vector_store.as_retriever(search_type="similarity", 
                                     search_kwargs={"k": 10, 
                                                    "score_threshold": 0.5,
                                                    # "filter": {"user_name": company_name}
                                    }
                                )

@tool
def vec_retriever(query:str):
    """Retrive the important information from vector store, and provide context to the LLM"""
        # Always reply in bangla text, do not answer in english."""
    return retriever.invoke(query)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

# format context
def format_docs(docs):
    """Format the documents to be used in the context."""
    return "\n\n".join(doc.page_content for doc in docs)


# RAG-Chain
template = """You are a Bangladeshi travel guide who is answering questions about tourist spots in Bangladesh.
Use the following pieces of context to answer the question at the end.
Always reply in bangla text, do not answer in english. No need to translate in english too.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use ten sentences maximum and keep the answer as details as possible.
End the answer on a single । punctuation.

{context}

Question: {question}

Helpful Answer:"""

custom_rag_prompt = PromptTemplate.from_template(template)

rag_chain = (
    {"context": vec_retriever | format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

# print(rag_chain.invoke("ঢাকায় ঘোরার মত কি আছে?"))



# streamlit
# st.title("Bangladesh Travel Bot 🌍")

# def response_generator(qstn):
#     res = rag_chain.invoke(qstn)
#     ans = res.split("।।")[0]
#     return ans

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

    
# # React to user input
# if prompt := st.chat_input("আমি ঘুরি সারা বাংলাদেশ। কোথায় যাবেন?"):
#     # Display user message in chat message container
#     st.chat_message("user").markdown(prompt)
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     response = response_generator(prompt)
#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         st.markdown(response)
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})
