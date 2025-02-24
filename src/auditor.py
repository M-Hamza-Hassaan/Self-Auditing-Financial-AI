import os
import json
import logging
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "some_secret_key"

# Path to the decisions file
DECISION_FILE = "loan_decisions.json"

# ---------------------------
# Helper Functions
# ---------------------------
def load_decisions():
    """Load the loan decisions from the JSON file."""
    if os.path.exists(DECISION_FILE):
        with open(DECISION_FILE, "r") as f:
            try:
                decisions = json.load(f)
            except json.JSONDecodeError:
                decisions = []
    else:
        decisions = []
    return decisions

def save_decisions(decisions):
    """Save the loan decisions to the JSON file."""
    with open(DECISION_FILE, "w") as f:
        json.dump(decisions, f, indent=4)

def update_auditor_decision(applicant_id, final_decision, auditor_comments):
    """
    Update the decision for a given applicant.
    If auditor_comments is provided, the comment will be prefixed with "Auditor:".
    """
    decisions = load_decisions()
    updated = False
    for decision in decisions:
        if decision.get("applicant_id") == applicant_id:
            decision["final_decision"] = final_decision
            # Add/update auditor_comments field if provided
            if auditor_comments and auditor_comments.strip():
                decision["auditor_comments"] = "Auditor: " + auditor_comments.strip()
            else:
                decision["auditor_comments"] = ""
            updated = True
            break
    if updated:
        save_decisions(decisions)
    return updated

def get_pending_reviews():
    """Return a list of decisions that require further review."""
    decisions = load_decisions()
    pending = [d for d in decisions if d.get("final_decision") == "requires further review"]
    return pending

def get_decision_by_applicant(applicant_id):
    """Return the decision dictionary for a given applicant ID."""
    decisions = load_decisions()
    for d in decisions:
        if d.get("applicant_id") == applicant_id:
            return d
    return None

# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def dashboard():
    """Dashboard view showing the count of pending review cases."""
    pending = get_pending_reviews()
    return render_template("auditor.html", page="dashboard", pending_count=len(pending))

@app.route("/review")
def review_list():
    """List all applications that require further review."""
    pending = get_pending_reviews()
    return render_template("auditor.html", page="review_list", reviews=pending)

@app.route("/review/<applicant_id>", methods=["GET", "POST"])
def review_detail(applicant_id):
    """
    Display details for a specific application pending review.
    On POST, update the decision based on auditor input.
    """
    decision = get_decision_by_applicant(applicant_id)
    if not decision:
        flash("Application not found.", "error")
        return redirect(url_for("review_list"))
    
    # Only allow pending review cases to be edited
    if decision.get("final_decision") != "requires further review":
        flash("This application is no longer pending review.", "warning")
        return redirect(url_for("review_list"))

    if request.method == "POST":
        final_decision = request.form.get("final_decision")
        auditor_comments = request.form.get("auditor_comments")
        if not final_decision:
            flash("Please select a final decision.", "error")
            return redirect(url_for("review_detail", applicant_id=applicant_id))
        updated = update_auditor_decision(applicant_id, final_decision, auditor_comments)
        if updated:
            flash("Decision updated successfully.", "success")
        else:
            flash("Error updating decision.", "error")
        return redirect(url_for("review_list"))

    return render_template("auditor.html", page="review_detail", review=decision)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    app.run(debug=True, port=5001)
