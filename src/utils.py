import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DECISION_FILE = "loan_decisions.json"
PENDING_FILE = "pending_reviews.json"

def save(data):
    """Saves loan application decision state to a JSON file."""
    try:
        # Read existing data if the file exists
        if os.path.exists(DECISION_FILE):
            with open(DECISION_FILE, "r") as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        # Append new entry
        existing_data.append(data)

        # Save back to file
        with open(DECISION_FILE, "w") as file:
            json.dump(existing_data, file, indent=4)

        logging.info(f"Saved loan decision for applicant {data.get('applicant_id', 'N/A')}")
    except Exception as e:
        logging.error(f"Error saving loan decision: {e}")

def save_pending_review(data):
    """Saves pending human review requests for admin intervention."""
    try:
        if os.path.exists(PENDING_FILE):
            with open(PENDING_FILE, "r") as file:
                try:
                    pending_reviews = json.load(file)
                except json.JSONDecodeError:
                    pending_reviews = []
        else:
            pending_reviews = []

        pending_reviews.append(data)

        with open(PENDING_FILE, "w") as file:
            json.dump(pending_reviews, file, indent=4)

        logging.info(f"Saved pending review for applicant {data.get('applicant_id', 'N/A')}")
    except Exception as e:
        logging.error(f"Error saving pending review: {e}")

def load_pending_reviews():
    """Loads pending human review requests."""
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def update_decision(applicant_id, final_decision):
    """Updates the decision for an applicant after admin override."""
    if os.path.exists(DECISION_FILE):
        with open(DECISION_FILE, "r") as file:
            try:
                decisions = json.load(file)
            except json.JSONDecodeError:
                decisions = []
    else:
        decisions = []

    for decision in decisions:
        if decision.get("applicant_id") == applicant_id:
            decision["final_decision"] = final_decision

    with open(DECISION_FILE, "w") as file:
        json.dump(decisions, file, indent=4)

    logging.info(f"Admin updated decision for applicant {applicant_id} to: {final_decision}")
