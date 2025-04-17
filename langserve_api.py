import os
from fastapi import FastAPI
from langserve import add_routes
from app import retriever, llm, rag_chain
from langchain_core.runnables import RunnableLambda
from exa_py import Exa

from langgraph.prebuilt import create_react_agent
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, AnyMessage
from langchain.tools import tool

from pydantic import BaseModel, Field
from typing import Annotated, TypedDict, Sequence, List, Union
from langgraph.graph.message import add_messages

# === Wrap with LangServe ===
app = FastAPI(
    title="Travel Bot BD",
    description="BD Travel Bot",
    version="0.1.0",
)

@tool
def vec_retriever(query: str) -> str:
    """Retrieve important information from the vector store and provide context to the LLM.
    Always reply in Bangla text, do not answer in English."""
    return retriever.invoke(query)

# Search tool by Exa
exa = Exa(api_key=os.environ["EXA_API_KEY"])

@tool
def search_and_contents(query: str) -> str:
  """Search for webpages based on the query and retrieve their contents.
  This tool is useful for searching for real-time or external data.
  Call it when query is not in the knowledge base and mentions searching or looking for external data."""
  return exa.search_and_contents(query,
                                 include_domains=["https://vromonguide.com/", 
                                                  "https://sundarbantourism.bforest.gov.bd/en/package/75",
                                                  "https://www.tourgroupbd.com/"],
                                 num_results=2, 
                                 text = True,
                                 filter_empty_results=True)
  
tools = [
    vec_retriever,
    search_and_contents
]

llm_with_tools = llm.bind(tools=tools)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent

system_prompt = """
    You are a helpful travel agent.
    Use the "vec_retriever" tool to get the answer to the question from the vector store.
    Use the "search_and_contents" tool to get the answer to the question from the internet.
    Answer the question as truthfully as possible using the provided context, and if the answer is not 
    contained within the text below, say 'I don't know'
    Tell minimum 5 sentances.
    Answer in Bangla.
    """

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        # ("system", "Given the following extracted parts of a long document and a question, create a final answer with references"),
        # ("human", "{messages}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=prompt,
    name="travel_agent"
)

class InputChat(BaseModel):
    """Input for the chat endpoint."""

    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )


class AgentState(TypedDict):
    messages: Annotated[Sequence[AnyMessage], add_messages]


def chat_input_mapper(input_dict):
    # Expects: {"messages": [HumanMessage, ...]}
    return {"messages": input_dict["messages"]}

def chat_output_mapper(output):
    return output['agent']['messages'][0].content

chat_chain = (
    RunnableLambda(chat_input_mapper)
    | agent
    | RunnableLambda(chat_output_mapper)
)

add_routes(
    app,
    chat_chain.with_types(input_type=InputChat),
    path="/chat",
    # playground_type="chat"
)

# === Run with Uvicorn ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8100)