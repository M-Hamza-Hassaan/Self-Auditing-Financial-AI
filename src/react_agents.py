# react_agents.py
# Contains an example implementation of a ReAct agent using BeeAI.

import asyncio
from typing import Any
from beeai_framework.agents.bee.agent import BeeAgent
from beeai_framework.agents.types import BeeInput, BeeRunInput, BeeRunOutput
from beeai_framework.backend.chat import ChatModel
from beeai_framework.memory.unconstrained_memory import UnconstrainedMemory
from beeai_framework.emitter.emitter import Emitter, EventMeta
from beeai_framework.emitter.types import EmitterOptions

async def run_react_agent():
    # Create a ChatModel instance using IBM Granite (via Ollama)
    chat_model: ChatModel = ChatModel.from_name("ollama:granite3.1-dense:8b")
    memory = UnconstrainedMemory()
    agent = BeeAgent(bee_input=BeeInput(llm=chat_model, tools=[], memory=memory))

    async def process_agent_events(event_data: dict[str, Any], event_meta: EventMeta) -> None:
        if event_meta.name == "error":
            print("Agent 🤖:", event_data["error"])
        elif event_meta.name == "retry":
            print("Agent 🤖: retrying the action...")
        elif event_meta.name == "update":
            print("Agent update:", event_data["update"]["parsedValue"])

    async def observer(emitter: Emitter) -> None:
        emitter.on("*.*", process_agent_events, EmitterOptions(match_nested=True))

    result: BeeRunOutput = await agent.run(
        run_input=BeeRunInput(prompt="What chemical elements make up a water molecule?")
    ).observe(observer)
    print("ReAct Agent Response:", result.state)

# For testing purposes
if __name__ == "__main__":
    asyncio.run(run_react_agent())
