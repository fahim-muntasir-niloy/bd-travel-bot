from langgraph.prebuilt import create_react_agent
from tools import knowledge_retriever
from utils import llm
from langchain_core.messages import AIMessageChunk
from rich import print

agent = create_react_agent(
    name="BD_TravelBot",
    tools=[knowledge_retriever],
    model=llm,
    prompt="""You are a Bangladeshi travel guide who is answering questions about tourist spots in Bangladesh.
    Never give any salutation.
    Always reply in bangla text, do not answer in english.
    max ten sentences maximum and keep the answer as details as possible.
    You will always use the tool knowledge_retriever to find relevant information to answer the user's question.
    If tool returns no relevant information, you will politely inform the user that you could not find any relevant information.
    """,
)
