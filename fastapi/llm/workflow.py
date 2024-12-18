from langgraph.graph import StateGraph, START, END

from llm.node import (
    State,
    generation_node,
    insert_message_history
)


workflow = StateGraph(State)

workflow.add_node("generation_node", generation_node)
workflow.add_node("insert_message_history", insert_message_history)

workflow.add_edge(START, "generation_node")
workflow.add_edge("generation_node", "insert_message_history")
workflow.add_edge("insert_message_history", END)