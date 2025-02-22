# workflows.py
# Contains implementations of workflows for our loan approval system and web search agent.

import traceback
from pydantic import BaseModel, ValidationError
from beeai_framework.workflows.workflow import Workflow, WorkflowError
from beeai_framework.backend.message import UserMessage
from agents import SafetyControlAgent, HumanCollaborationAgent

# Define the state for the loan approval workflow
class LoanApprovalState(BaseModel):
    applicant_id: int
    demographic: str
    loan_status: str = "pending"
    risk_flag: str | None = None
    final_decision: str | None = None

# Workflow step: Monitor application using SafetyControlAgent
async def monitor_application(state: LoanApprovalState) -> str:
    safety_agent = SafetyControlAgent()
    safety_agent.monitor_loan_data([{
        "applicant_id": state.applicant_id,
        "demographic": state.demographic,
        "loan_status": state.loan_status
    }])
    if state.demographic == "group_A":
        state.risk_flag = "Potential bias detected for group A"
    return "review_decision"

# Workflow step: Review decision using HumanCollaborationAgent
async def review_decision(state: LoanApprovalState) -> str:
    human_agent = HumanCollaborationAgent()
    human_agent.facilitate_human_review(
        {"applicant_id": state.applicant_id, "details": "Complex case"},
        state.loan_status
    )
    # For demo purposes, if risk_flag is set, mark as "requires further review"
    state.final_decision = "approved" if state.risk_flag is None else "requires further review"
    return Workflow.END

async def run_loan_approval_workflow():
    try:
        loan_workflow = Workflow(schema=LoanApprovalState, name="LoanApprovalWorkflow")
        loan_workflow.add_step("monitor_application", monitor_application)
        loan_workflow.add_step("review_decision", review_decision)
        # Simulate a loan application (replace with real data in production)
        loan_state = LoanApprovalState(applicant_id=101, demographic="group_A")
        final_response = await loan_workflow.run(loan_state)
        return final_response.state
    except (WorkflowError, ValidationError) as e:
        traceback.print_exc()
        return None
