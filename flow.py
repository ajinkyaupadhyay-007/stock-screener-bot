from typing import Annotated
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from colorama import Fore
from langgraph.prebuilt import ToolNode
from tool import simple_screener
llm = ChatOllama(model="llama3.2")
tools=[simple_screener]
llm_with=llm.bind_tools(tools)
tool_node=ToolNode(tools)

class State(dict):
  messages:Annotated[list,add_messages]

def chatbot(state:State):
  return {"messages":[llm_with.invoke(state['messages'])]}
def router(state:State):
  last_message=state['messages'][-1]
  if hasattr(last_message,'tool_calls') and  last_message.tool_calls:
    return "tools"
  else:
    return END

graph_builder=StateGraph(State)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("tools","chatbot")
graph_builder.add_conditional_edges("chatbot",router)

memory=InMemorySaver()
graph=graph_builder.compile(checkpointer=memory)
if __name__=="__main__":
  while True:
    prompt=input("enter your prompt here :)")
    if prompt.lower() in ['quit','exit','q']:
      print("exiting...")
      break
    res=graph.invoke({"messages":[{"role":"user","content":prompt}]},config={"configurable":{"thread_id":1234}})
    print(Fore.LIGHTYELLOW_EX+res["messages"][-1].content+Fore.RESET)
