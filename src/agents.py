# agents.py
# Contains definitions for core governance agents.

class SafetyControlAgent:
    def monitor_loan_data(self, loan_applications):
        """Monitors loan applications for potential bias."""
        demographic_data = self._extract_demographic_data(loan_applications)
        bias_detected = self._analyze_for_bias(demographic_data)
        if bias_detected:
            self._trigger_alert(f"Potential bias detected: {bias_detected}")
        else:
            print("SafetyControlAgent: No bias detected in loan approvals.")

    def _extract_demographic_data(self, loan_applications):
        print("SafetyControlAgent: Extracting demographic data...")
        return {"demographics": [app["demographic"] for app in loan_applications]}

    def _analyze_for_bias(self, demographic_data):
        print("SafetyControlAgent: Analyzing for bias...")
        if demographic_data["demographics"].count("group_A") > 2:
            return "Disproportionate rejection rate for group A"
        return None

    def _trigger_alert(self, message):
        print(f"SafetyControlAgent ALERT: {message}")


class EthicsAgent:
    def review_decision_criteria(self, loan_criteria):
        """Reviews loan decision criteria for ethical alignment."""
        ethical_guidelines = self._load_ethical_guidelines()
        unethical_criteria = self._identify_unethical_criteria(loan_criteria, ethical_guidelines)
        if unethical_criteria:
            self._flag_criteria(unethical_criteria)
        else:
            print("EthicsAgent: Loan criteria align with ethical guidelines.")

    def _load_ethical_guidelines(self):
        print("EthicsAgent: Loading ethical guidelines...")
        return [
            "Do not discriminate based on protected characteristics",
            "Ensure transparency",
            "Promote fairness"
        ]

    def _identify_unethical_criteria(self, loan_criteria, ethical_guidelines):
        print("EthicsAgent: Identifying unethical criteria...")
        unethical = []
        for criterion in loan_criteria:
            if criterion in ["Zip Code Risk Score", "Name Ethnicity Score"]:
                unethical.append(criterion)
        return unethical

    def _flag_criteria(self, unethical_criteria):
        print(f"EthicsAgent ALERT: Unethical criteria identified: {unethical_criteria}")


class ComplianceAgent:
    def audit_for_compliance(self, loan_decisions):
        """Audits loan decisions for regulatory compliance."""
        regulations = self._load_regulations()
        non_compliant_decisions = self._check_compliance(loan_decisions, regulations)
        if non_compliant_decisions:
            self._generate_report(non_compliant_decisions)
        else:
            print("ComplianceAgent: Loan decisions are compliant with regulations.")

    def _load_regulations(self):
        print("ComplianceAgent: Loading financial regulations...")
        return {"Consumer Protection Law": "Rule X", "Anti-Discrimination Act": "Rule Y"}

    def _check_compliance(self, loan_decisions, regulations):
        print("ComplianceAgent: Checking compliance...")
        non_compliant = []
        for decision in loan_decisions:
            if decision.get("reason") == "discriminatory_criterion":
                non_compliant.append(decision)
        return non_compliant

    def _generate_report(self, non_compliant_decisions):
        print(f"ComplianceAgent ALERT: Compliance Report generated for non-compliant decisions: {non_compliant_decisions}")


class HumanCollaborationAgent:
    def facilitate_human_review(self, loan_application, ai_decision):
        """Facilitates human review and potential override of AI decisions."""
        print("HumanCollaborationAgent: Loan application flagged for human review.")
        human_override = self._get_human_override_decision(loan_application, ai_decision)
        if human_override:
            final_decision = human_override
            print("HumanCollaborationAgent: Human override applied.")
        else:
            final_decision = ai_decision
            print("HumanCollaborationAgent: AI decision confirmed.")
        self._record_final_decision(loan_application, final_decision)

    def _get_human_override_decision(self, loan_application, ai_decision):
        print("HumanCollaborationAgent: Initiating human loan officer review process...")
        user_input = input(f"Review loan application for applicant {loan_application['applicant_id']} (AI decision: {ai_decision}). Override? (yes/no): ")
        if user_input.lower() == 'yes':
            return "approved"
        return None

    def _record_final_decision(self, loan_application, final_decision):
        print(f"HumanCollaborationAgent: Final loan decision for applicant {loan_application['applicant_id']} recorded as: {final_decision}")
