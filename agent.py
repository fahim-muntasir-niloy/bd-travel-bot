from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessageChunk
from tools import knowledge_retriever
from utils import llm
from rich import print


agent = create_react_agent(
    name="BD_TravelBot",
    tools=[knowledge_retriever],
    model=llm,
    prompt="""You are a Bangladeshi travel guide who is answering questions about tourist spots in Bangladesh. Always reply in bangla text, do not answer in english.
    max ten sentences maximum and keep the answer as details as possible.
    You will always use the tool knowledge_retriever to find relevant information to answer the user's question.
    """,
)

# for m, metadata in agent.stream({"messages": "khulnay ঘোরার মত কি আছে?"},
#                                 stream_mode="messages"):
#     if isinstance(m, AIMessageChunk):
#         print(m.content, flush=True)
