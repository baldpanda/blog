import os
from haystack.agents.memory import ConversationSummaryMemory
from haystack.agents.conversational import ConversationalAgent
from haystack.nodes import PromptNode

model_api_key = os.getenv("HF_API_KEY", None)

running_coach_prompt_template = """
In the following conversation, a human user interacts with an Running Coach AI Agent.

The following is the previous conversation between a human and an AI:
{memory}

AI Agent responses must start with one of the following:

Not Running Related: "the question is not running related" if the query is not running related
Thought: [AI Agent's reasoning process]
Final Answer: [final answer to the human user's question only if it is running related]

The AI Agent should not ask the human user for additional information, clarification, or context.

Question: {query}
"""

prompt_node = PromptNode(
    model_name_or_path="HuggingFaceH4/zephyr-7b-beta",
    api_key=model_api_key,
    max_length=256,
    stop_words=["Human"],
    default_prompt_template=running_coach_prompt_template,
)

summary_memory = ConversationSummaryMemory(prompt_node)

conversational_agent = ConversationalAgent(
    prompt_node=prompt_node,
    memory=summary_memory,
    prompt_template=running_coach_prompt_template
    )


def ask_question(question):
    return conversational_agent.run(question)
