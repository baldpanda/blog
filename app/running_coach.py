import os
from haystack.agents.memory import ConversationSummaryMemory
from haystack.agents.conversational import ConversationalAgent
from haystack.nodes import PromptNode

LLM_MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"
MAX_MODEL_OUTPUT_LENGTH = 512
model_api_key = os.getenv("HF_API_KEY", None)

running_coach_prompt_template = """
In the following, a human asks a question user to an Running Coach AI Agent who responds with an answer.

The following is the previous question between a human and an AI:
{memory}

AI Agent responses must start with one of the following:

Not Running Related: "the question is not running related" if the query is not running related
Thought: [AI Agent's reasoning process]\n
Final Answer: [final answer to the human user's question only if it is running related]\n

The AI Agent should not ask the human user for additional information, clarification, or context.

Question: {query}
"""

prompt_node = PromptNode(
    model_name_or_path=LLM_MODEL_NAME,
    api_key=model_api_key,
    max_length=MAX_MODEL_OUTPUT_LENGTH,
    stop_words=["Human"],
)

summary_memory = ConversationSummaryMemory(prompt_node)

conversational_agent = ConversationalAgent(
    prompt_node=prompt_node,
    memory=summary_memory,
    prompt_template=running_coach_prompt_template,
)


def ask_question(question):
    return conversational_agent.run(question)
