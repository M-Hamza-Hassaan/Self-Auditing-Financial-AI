import json
import os
import time

SAVE_FILE = "loan_decisions.json"

def load_decisions():
    """Loads loan decisions from file."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def override_decision():
    """Allows an admin to override decisions in real-time."""
    print("Monitoring loan decisions... Press Ctrl+C to exit.")
    
    seen_applicants = set()  # Keep track of applicants we have seen

    try:
        while True:
            decisions = load_decisions()
            for decision in decisions:
                applicant_id = decision["applicant_id"]
                
                # Skip if already reviewed
                if applicant_id in seen_applicants:
                    continue

                print("\n=== New Loan Decision ===")
                print(f"Applicant ID: {applicant_id}")
                print(f"Demographic: {decision['demographic']}")
                print(f"Loan Status: {decision['loan_status']}")
                print(f"Risk Flag: {decision['risk_flag']}")
                print(f"Final Decision: {decision['final_decision']}")
                
                # Admin Override
                override = input("Override decision? (yes/no): ").strip().lower()
                if override == "yes":
                    decision["final_decision"] = input("Enter new decision (approved/rejected/review): ").strip()
                    print(f"Decision for applicant {applicant_id} updated to: {decision['final_decision']}")

                    # Save updated decisions
                    with open(SAVE_FILE, "w") as file:
                        json.dump(decisions, file, indent=4)

                seen_applicants.add(applicant_id)  # Mark as reviewed
            time.sleep(5)  # Check every 5 seconds
    except KeyboardInterrupt:
        print("\nAdmin monitoring stopped.")

if __name__ == "__main__":
    override_decision()
