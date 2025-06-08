#agents.py
import asyncio
import json
import os
from typing import List, Optional
from pydantic import BaseModel, Field
from beeai_framework.backend.message import SystemMessage, UserMessage
from beeai_framework.backend.chat import ChatModel, ChatModelInput, ChatModelOutput
from beeai_framework.backend.chat import ChatModelStructureInput

# Create a shared global ChatModel instance for all agents.
model = ChatModel.from_name("ollama:granite3.1-dense:8b")

# ================= SafetyControlAgent =================
class SafetyControlAgent:
    async def monitor_loan_data(self, loan_applications):
        """Monitors loan applications for potential bias using a BeeAI LLM evaluation."""
        print("SafetyControlAgent: Extracting demographic data...")
        demographic_data = self._extract_demographic_data(loan_applications)
        red_flag_data = self._extract_red_flag_data(loan_applications)
        print("DEBUG: Extracted risk flag data:", red_flag_data)
        
        # Create a combined message from demographic info and red flag data.
        demographic_data_string = ", ".join(demographic_data["demographics"])
        red_flag_string = ", ".join(red_flag_data["red_flag"])
        user_message_text = f"Demographics: {demographic_data_string}. Red flag info: {red_flag_string}."
        print("DEBUG: user_message SafetyControlAgent:", user_message_text)
        
        # Define the LLM prompt for bias evaluation.
        SafetyControlAgent_prompt = (
            "You are a Safety Agent. Your job is to check for potential bias in loan applications based on demographic groups.\n"
            "Task: Review the provided loan application data. For each demographic group mentioned, decide if there is potential bias against that group.\n"
            "Output: For each demographic group, respond with ONE of these:\n"
            ' "Bias likely for: [Demographic Group Name]" (if you suspect bias)\n'
            ' "No bias for: [Demographic Group Name]" (if you see no bias)\n'
        )
        system_message = SystemMessage(content=SafetyControlAgent_prompt)
        user_message = UserMessage(content=user_message_text)
        
        # Use the shared global model.
        print("DEBUG: Sending SafetyControlAgent request to LLM...")
        output: ChatModelOutput = await model.create(ChatModelInput(messages=[system_message, user_message]))
        result = output.get_text_content().strip()
        print("DEBUG: SafetyControlAgent LLM response:", result)
        
        if "Bias likely" in result:
            self._trigger_alert(result)
        else:
            print("SafetyControlAgent: No bias detected in loan approvals.")
        return result

    def _extract_demographic_data(self, loan_applications):
        return {"demographics": [app.get("demographic", "unknown") for app in loan_applications]}
    
    def _extract_red_flag_data(self, loan_applications):
        """Extracts the initial risk flag (or red flag) information from the loan applications."""
        return {"red_flag": [app.get("risk_flag", "unknown") for app in loan_applications]}

    def _trigger_alert(self, message):
        print(f"SafetyControlAgent ALERT: {message}")

# ================= EthicsAgent =================
# Load Acme Bank's ethical guidelines from file.

base_dir = os.path.dirname(os.path.abspath(__file__))  # gets the path to src/
full_ethics_path = os.path.join(base_dir, "acme_bank_ethics_guidelines.txt")

with open(full_ethics_path, "r") as f:
    acme_ethics_context = f.read()


EthicsAgent_prompt = f"""You are an Ethics Agent for Acme Bank. Your role is to evaluate loan applications against **Acme Bank's ethical guidelines** to ensure they align with our company's ethical standards.

**Context: Acme Bank Ethical Guidelines**

```
{acme_ethics_context}
```

**Task:** Analyze the loan application data provided and determine if the loan application and its criteria are ETHICAL or UNETHICAL according to the **Acme Bank Ethical Guidelines** provided above.

**Instructions:**

1.  Carefully read and understand the **Acme Bank Ethical Guidelines** provided in the **Context** section.
2.  Examine the loan application data and pay close attention to the "loan criteria" and other application details.
3.  For each loan criterion in the application, evaluate whether it aligns with or violates any of the principles and guidelines outlined in the **Acme Bank Ethical Guidelines**. Consider the *spirit* of the guidelines as well as the literal wording.
4.  Assess the overall ethical implications of the *entire* loan application, considering all criteria and any other relevant information provided in the data.
5.  Determine if, based on your analysis and the **Acme Bank Ethical Guidelines**, the loan application and its criteria should be considered ETHICAL or UNETHICAL.
6.  **Output Format:** State your conclusion clearly as either:

    *   **"ETHICAL"**: If the loan application and its criteria are fully aligned with the Acme Bank Ethical Guidelines and do not violate any principles.
    *   **"UNETHICAL"**: If the loan application or any of its criteria violate one or more principles of the Acme Bank Ethical Guidelines.  If you determine the application is UNETHICAL, also **briefly specify which specific guideline(s) from the Acme Bank Ethical Guidelines are potentially violated.**

**Begin!**
"""
system_message_ethics = SystemMessage(content=EthicsAgent_prompt)

class EthicsAgent:
    async def review_decision_criteria(self, loan_application_data_json):  # Expecting JSON string as input
        print("DEBUG: EthicsAgent: Starting ethical review using LLM...")
        user_message_ethics = UserMessage(content=loan_application_data_json)
        print("DEBUG: EthicsAgent: Loan application JSON sent to LLM:", loan_application_data_json)

        try:
            output_ethics: ChatModelOutput = await model.create(
                ChatModelInput(messages=[system_message_ethics, user_message_ethics])
            )
            ethics_assessment_text = output_ethics.get_text_content()
            print("DEBUG: EthicsAgent: Raw LLM response:", ethics_assessment_text)
            return self._process_ethics_assessment(ethics_assessment_text)
        except Exception as e:
            print(f"EthicsAgent Error during LLM processing: {e}")
            return {"ethical": False, "reasons": ["Error during ethical review processing."]}

    def _process_ethics_assessment(self, assessment_text):
        print("DEBUG: EthicsAgent: Processing ethical assessment...")
        print(f"DEBUG: EthicsAgent Raw Assessment: {assessment_text}")

        if "ETHICAL" in assessment_text.upper():
            print("EthicsAgent: Loan application deemed ETHICAL by LLM.")
            return {"ethical": True, "reasons": []}
        elif "UNETHICAL" in assessment_text.upper():
            unethical_reasons = []
            if "Violates Guideline" in assessment_text:
                reasons_start_index = assessment_text.find("Violates Guideline")
                unethical_reasons_text = assessment_text[reasons_start_index:]
                unethical_reasons = [reason.strip() for reason in unethical_reasons_text.split("Guideline") if reason.strip()]
            print(f"EthicsAgent ALERT: Loan application deemed UNETHICAL by LLM. Reasons: {unethical_reasons}")
            return {"ethical": False, "reasons": unethical_reasons}
        else:
            print("EthicsAgent: Inconclusive ethical assessment from LLM.")
            return {"ethical": None, "reasons": ["Inconclusive ethical assessment from LLM. Review manually."]}

    def _flag_criteria(self, unethical_assessment_result):
        if not unethical_assessment_result["ethical"]:
            reasons = unethical_assessment_result["reasons"]
            if reasons:
                print(f"EthicsAgent ALERT: Loan application deemed UNETHICAL. Violations: {', '.join(reasons)}")
            else:
                print("EthicsAgent ALERT: Loan application deemed UNETHICAL. Reasons not specified by LLM.")
        else:
            print("EthicsAgent: Loan application deemed ETHICAL.")

# ================= ComplianceAgent =================
# --- Define Structured Output Schema for Compliance Report ---
class ComplianceReportSchema(BaseModel):
    is_compliant: bool = Field(description="Indicates whether the loan decision is compliant with financial regulations.")
    non_compliant_regulations: Optional[List[str]] = Field(default=None, description="List of names of financial regulations that are violated, if any. Empty list if compliant.")
    reasons: Optional[List[str]] = Field(default=None, description="Detailed reasons for non-compliance, referencing specific regulations and rules. Empty list if compliant.")

# --- Load Financial Regulations from Text File (RAG Context) ---
current_directory = os.getcwd()
regulations_file_path = os.path.join(current_directory, "financial_regulations.txt") # Path to your regulations text file
full_regulations_path = os.path.join(os.getcwd(), regulations_file_path)
try:
    with open(full_regulations_path, 'r') as f:
        financial_regulations_context = f.read()
    print("DEBUG: ComplianceAgent: Financial regulations loaded from text file.")
except FileNotFoundError:
    financial_regulations_context = "Financial regulations context not found. Please ensure financial_regulations.txt exists."
    print(f"Warning: {regulations_file_path} not found. ComplianceAgent will run without regulation context.")

# --- System Prompt for ComplianceAgent (using RAG context) ---
ComplianceAgent_prompt = f"""You are a Compliance Agent for Acme Bank, specialized in auditing loan decisions for regulatory compliance. Your primary task is to review loan decision details and assess whether they comply with the financial regulations provided below.

**Context: Financial Regulations**
```
{financial_regulations_context}
```

**Task:** Analyze the provided loan decision data and determine if it is compliant with the **Financial Regulations** outlined in the **Context** section above.

**Instructions:**

1.  Carefully read and understand the **Financial Regulations** provided in the **Context** section. Treat this as your rulebook for compliance.
2.  Examine the **Loan Decision Data** provided in the User Message. Pay close attention to the decision, reasons, and criteria used for the loan decision.
3.  Compare the **Loan Decision Data** against the **Financial Regulations**. For each relevant regulation, determine if the loan decision adheres to the rules and principles described.
4.  Focus on identifying any potential violations of the regulations. Consider both direct and indirect violations based on the decision details.
5.  Assess the overall compliance of the **Loan Decision**.
6.  **Output Format:**  You MUST respond with a structured JSON object conforming to the `ComplianceReportSchema` schema.
    -  Set `is_compliant` to `true` if the loan decision fully complies with all relevant regulations. Set it to `false` otherwise.
    -  If `is_compliant` is `false`, provide a list of `non_compliant_regulations` (regulation names from the context that are violated) and detailed `reasons` for non-compliance.
    
**Begin! Provide your response in JSON format according to the `ComplianceReportSchema`.**
"""
system_message_compliance = SystemMessage(content=ComplianceAgent_prompt)

class ComplianceAgent:
    async def audit_for_compliance(self, loan_decision_json):  # Expecting JSON string input of a SINGLE decision
        print("DEBUG: ComplianceAgent: Starting compliance audit using RAG and LLM...")
        print("DEBUG: ComplianceAgent: Loan decision JSON sent to LLM:", loan_decision_json)
        user_message_compliance = UserMessage(content=loan_decision_json)
        try:
            output_compliance: ChatModelOutput = await model.create_structure(
                ChatModelStructureInput(
                    schema=ComplianceReportSchema,
                    messages=[system_message_compliance, user_message_compliance]
                )
            )
            print("DEBUG: ComplianceAgent: Raw output from model.create_structure:", output_compliance)
            compliance_report_data = output_compliance.object
            print("DEBUG: ComplianceAgent: Raw compliance report data:", compliance_report_data)
            # Convert dict output into ComplianceReportSchema object.
            compliance_report = ComplianceReportSchema.parse_obj(compliance_report_data)
            print("DEBUG: ComplianceAgent: Parsed compliance report:", compliance_report)
            return self._process_compliance_report(compliance_report)
        except Exception as e:
            print(f"ComplianceAgent Error during LLM structured output processing: {e}")
            return {"is_compliant": False, "non_compliant_regulations": ["Error during compliance check"], "reasons": [f"Error during LLM processing: {e}"]}

    def _process_compliance_report(self, compliance_report: ComplianceReportSchema):
        print("DEBUG: ComplianceAgent: Processing compliance report...")
        print(f"DEBUG: ComplianceAgent LLM Report: Compliant: {compliance_report.is_compliant}, Violations: {compliance_report.non_compliant_regulations or []}, Reasons: {compliance_report.reasons or []}")
        if compliance_report.is_compliant:
            print("ComplianceAgent: Loan decision deemed COMPLIANT by LLM.")
            return {"is_compliant": True, "non_compliant_regulations": [], "reasons": []}
        else:
            print(f"ComplianceAgent ALERT: Loan decision deemed NON-COMPLIANT by LLM. Violations: {compliance_report.non_compliant_regulations or []}, Reasons: {compliance_report.reasons or []}")
            return {"is_compliant": False, "non_compliant_regulations": compliance_report.non_compliant_regulations or [], "reasons": compliance_report.reasons or []}

    def _generate_report(self, non_compliant_decisions):
        print("DEBUG: ComplianceAgent: Generating compliance report for non-compliant decisions:")
        for decision in non_compliant_decisions:
            regulation_violated = decision.get("regulation_violated", "Unknown Regulation")
            print(f" - Decision ID: {decision.get('decision_id', 'N/A')}, Reason: {decision.get('reason', 'N/A')}, Regulation Violated: {regulation_violated}")

# ================= HumanCollaborationAgent =================
class HumanCollaborationAgent:
    def facilitate_human_review(self, loan_application, ai_decision):
        # If AI decision is approved, bypass human review.
        if ai_decision.lower() == "approved":
            print("HumanCollaborationAgent: AI decision is approved; bypassing human review.")
            return "approved"
        print("HumanCollaborationAgent: Loan application flagged for human review.")
        human_override = self._get_human_override_decision(loan_application, ai_decision)
        if human_override:
            final_decision = human_override
            print("HumanCollaborationAgent: Human override applied.")
        else:
            final_decision = ai_decision
            print("HumanCollaborationAgent: AI decision confirmed.")
        self._record_final_decision(loan_application, final_decision)
        return final_decision

    def _get_human_override_decision(self, loan_application, ai_decision):
        print("DEBUG: HumanCollaborationAgent: Initiating human loan officer review process...")
        try:
            user_input = input(
                f"Review loan application for applicant {loan_application.get('applicant_id', 'N/A')} "
                f"(AI decision: {ai_decision}). Override? (yes/no): "
            )
            print("DEBUG: HumanCollaborationAgent: User input received:", user_input)
        except Exception as e:
            print("ERROR: HumanCollaborationAgent: Exception during user input:", e)
            user_input = "no"
        if user_input.lower() == 'yes':
            return "approved"
        return None

    def _record_final_decision(self, loan_application, final_decision):
        print(f"HumanCollaborationAgent: Final loan decision for applicant {loan_application.get('applicant_id', 'N/A')} recorded as: {final_decision}")
