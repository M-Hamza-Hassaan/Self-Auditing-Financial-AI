# chat_model_examples.py
# Contains examples for interacting with the ChatModel (IBM Granite integration).
import asyncio
from beeai_framework.backend.message import UserMessage, AssistantMessage
from beeai_framework.backend.chat import ChatModel, ChatModelInput, ChatModelOutput
from beeai_framework.memory.unconstrained_memory import UnconstrainedMemory

async def chat_model_demo():
    # Create a ChatModel instance using IBM Granite (via Ollama provider)
    model = ChatModel.from_name("ollama:granite3.1-dense:8b")
    
    # Simple message exchange
    user_message = UserMessage(content="Hello! What is the capital of France?")
    output: ChatModelOutput = await model.create(ChatModelInput(messages=[user_message]))
    print("ChatModel Response:", output.get_text_content())
    
    # Demonstrate memory usage by preserving conversation history
    memory = UnconstrainedMemory()
    await memory.add(user_message)
    await memory.add(AssistantMessage(content=output.get_text_content()))
    await memory.add(UserMessage(content="Can you recommend one thing to do in Paris?"))
    memory_output: ChatModelOutput = await model.create(ChatModelInput(messages=memory.messages))
    print("Memory-based Response:", memory_output.get_text_content())

if __name__ == "__main__":
    asyncio.run(chat_model_demo())
