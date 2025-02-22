# governance.py
# Contains additional governance helper functions that utilize our agents.

from agents import SafetyControlAgent, EthicsAgent, ComplianceAgent, HumanCollaborationAgent

def run_governance_checks(loan_application, loan_criteria, loan_decisions):
    print("Running governance checks...")
    
    # Safety check
    safety_agent = SafetyControlAgent()
    safety_agent.monitor_loan_data([loan_application])
    
    # Ethical review
    ethics_agent = EthicsAgent()
    ethics_agent.review_decision_criteria(loan_criteria)
    
    # Regulatory compliance check
    compliance_agent = ComplianceAgent()
    compliance_agent.audit_for_compliance(loan_decisions)
    
    # Optionally, invoke human review if necessary
    human_agent = HumanCollaborationAgent()
    human_agent.facilitate_human_review(loan_application, loan_application.get("loan_status", "pending"))
    
    print("Governance checks completed.")
