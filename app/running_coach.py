import os
from haystack.agents.memory import ConversationSummaryMemory
from haystack.agents.conversational import ConversationalAgent
from haystack.nodes import PromptNode

model_api_key = os.getenv("HF_API_KEY", None)

prompt_node = PromptNode(
    model_name_or_path="HuggingFaceH4/zephyr-7b-beta",
    api_key=model_api_key,
    max_length=256,
    stop_words=["Human"],
)

summary_memory = ConversationSummaryMemory(prompt_node)

conversational_agent = ConversationalAgent(
    prompt_node=prompt_node, memory=summary_memory
)


def ask_question(question):
    return conversational_agent.run(question)
