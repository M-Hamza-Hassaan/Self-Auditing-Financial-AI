import logging
from fastapi import FastAPI, Request
from pydantic import BaseModel
import asyncio
import traceback

from chat import chat_model_demo, process_submission
from workflows import run_loan_approval_workflow  # Loan approval workflow

# Configure Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("server.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)

app = FastAPI(
    title="Open AI Governance API 1.0",
    description="API for processing loan application submissions through AI Governance",
    version="1.0",
)

class LoanApplication(BaseModel):
    text: str

# Middleware to log every request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Logs all incoming requests."""
    logging.info(f"Incoming request: {request.method} {request.url}")
    body = await request.body()
    logging.info(f"Request Body: {body.decode('utf-8')}")
    
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response

@app.post("/submit")
async def submit_application(application: LoanApplication):
    """Handles loan applications by processing the submission text and running the AI workflow."""
    logging.info(f"Received loan application: {application.text}")

    try:
        # Process submission text using ChatModel (parsing and initial evaluation)
        logging.info("=== Processing Submission ===")
        processed_submission = await process_submission(application.text)
        logging.info(f"Submission Processed: {processed_submission}")

        # Run Loan Approval Workflow with parsed submission
        logging.info("=== Running Loan Approval Workflow ===")
        final_state = await run_loan_approval_workflow(processed_submission)
        logging.info(f"Final Loan Application State: {final_state}")
        return {"status": "success", "final_state": final_state}

    except Exception as e:
        logging.error(f"Error processing loan application: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
