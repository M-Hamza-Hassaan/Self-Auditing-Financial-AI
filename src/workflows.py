import asyncio
import json
from agents import SafetyControlAgent, EthicsAgent, ComplianceAgent, HumanCollaborationAgent
from utils import save

async def run_loan_approval_workflow(processed_submission: dict):
    """
    Executes the full loan approval workflow:
      - Safety analysis via LLM evaluation (with demographic and initial risk flag data)
      - Ethics review using the Acme Bank guidelines
      - Compliance audit using structured LLM output
      - Final decision:
          - If AI decision is "approved", final decision is automatically approved.
          - If AI decision is "requires further review", the decision is flagged for later override.
          - Otherwise, human override is prompted.
    Saves the final decision and returns a summary string.
    """
    # Create a copy of the processed submission and set defaults.
    loan_application = processed_submission.copy()
    loan_application.setdefault("loan_criteria", ["Standard Risk Assessment", "Income Verification"])

    # Run Safety Control Agent with LLM evaluation for bias detection.
    safety_agent = SafetyControlAgent()
    bias_result = await safety_agent.monitor_loan_data([loan_application])
    loan_application["risk_flag"] = bias_result

    # Run Ethics Agent: pass full loan application data as JSON string.
    ethics_agent = EthicsAgent()
    ethics_review_result = await ethics_agent.review_decision_criteria(json.dumps(loan_application))
    ethics_agent._flag_criteria(ethics_review_result)
    loan_application["ethics_review"] = ethics_review_result

    # Run Compliance Agent: pass loan decision data as JSON string.
    compliance_agent = ComplianceAgent()
    # Determine AI decision: if bias is suspected or ethics review is not positive, mark as "requires further review"
    ai_decision = "requires further review" if ("Bias likely" in bias_result or not ethics_review_result.get("ethical", True)) else "approved"
    loan_decision = {
        "decision_id": "LD-" + str(loan_application.get("applicant_id", "unknown")),
        "applicant_id": loan_application.get("applicant_id"),
        "decision": ai_decision,
        "reason": "discriminatory_criterion" if ai_decision != "approved" else "",
        "criteria": loan_application.get("loan_criteria")
    }
    compliance_report = await compliance_agent.audit_for_compliance(json.dumps(loan_decision))
    loan_application["compliance_report"] = compliance_report

    # Final decision: if AI decision is "approved", then final decision is automatically "approved".
    # If AI decision is "requires further review", flag it for later override without prompting immediately.
    if ai_decision.lower() == "approved":
        final_decision = "approved"
    elif ai_decision.lower() == "requires further review":
        print("Workflow: AI decision requires further review; flagging for later human override.")
        final_decision = "requires further review"
    else:
        human_agent = HumanCollaborationAgent()
        final_decision = human_agent.facilitate_human_review(loan_application, ai_decision)
    loan_application["final_decision"] = final_decision

    # Save final decision using utils.
    save(loan_application)

    # Build and return a summary string of the final state.
    final_state_str = (
        f"applicant_id={loan_application.get('applicant_id')} "
        f"demographic='{loan_application.get('demographic')}' "
        f"loan_status='{loan_application.get('loan_status', 'pending')}' "
        f"risk_flag='{loan_application.get('risk_flag')}' "
        f"final_decision='{loan_application.get('final_decision')}'"
    )
    return final_state_str