import asyncio
import json
from beeai_framework.backend.message import UserMessage, AssistantMessage
from beeai_framework.backend.chat import ChatModel, ChatModelInput, ChatModelOutput
from beeai_framework.memory.unconstrained_memory import UnconstrainedMemory

# Initialize the chat model globally to avoid recreating it for each request
model = ChatModel.from_name("ollama:granite3.1-dense:8b")

async def chat_model_demo():
    """Demonstrates simple chat interactions with memory usage."""
    user_message = UserMessage(content="Hello! What is the capital of France?")
    output: ChatModelOutput = await model.create(ChatModelInput(messages=[user_message]))
    print("ChatModel Response:", output.get_text_content())

    # Demonstrate memory usage by preserving conversation history
    memory = UnconstrainedMemory()
    await memory.add_many([
        user_message,
        AssistantMessage(content=output.get_text_content()),
        UserMessage(content="Can you recommend one thing to do in Paris?")
    ])
    memory_output: ChatModelOutput = await model.create(ChatModelInput(messages=memory.messages))
    print("Memory-based Response:", memory_output.get_text_content())

async def process_submission(text: str) -> dict:
    """
    Processes loan application submission text using the ChatModel.
    Attempts to parse JSON data from the submission.
    If parsing fails, uses default values and sends the raw text to the model.
    """
    try:
        # Try to parse the text as JSON for structured data.
        data = json.loads(text)
    except Exception:
        data = {"applicant_id": "unknown", "demographic": "unknown", "raw_text": text}

    # Use the ChatModel to process the submission text.
    user_message = UserMessage(content=text)
    try:
        output: ChatModelOutput = await model.create(ChatModelInput(messages=[user_message]))
        response_text = output.get_text_content()
    except Exception as e:
        response_text = f"Error processing submission: {str(e)}"

    # Build the processed submission dictionary.
    result = {
        "applicant_id": data.get("applicant_id", "unknown"),
        "demographic": data.get("demographic", "unknown"),
        "loan_status": "pending",  # initial status
        "risk_flag": response_text  # initial evaluation from the model
    }
    return result

# Ensuring the script does not execute chat_model_demo when imported in FastAPI
if __name__ == "__main__":
    asyncio.run(chat_model_demo())
