from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import json
import os
import re  # Import regex module
import datetime  # Import datetime module

app = Flask(__name__)
app.secret_key = 'some_secret_key'

# --- Configuration ---
SERVER_URL = "http://localhost:8000/submit"
USE_EXAMPLE_SELECTOR = True  # Set to False to hide example selector

def get_full_file_path(filename):
    """Gets the full path to a file in the current directory."""
    current_directory = os.getcwd()
    return os.path.join(current_directory, filename)

# Function to load example data from JSON file, now takes filename as argument
def load_example_data(filename):
    example_json_path = get_full_file_path(filename)
    try:
        if os.path.exists(example_json_path):
            with open(example_json_path, 'r') as f:
                return json.load(f)
        else:
            return None  # Return None if file does not exist
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

@app.route("/example_data")
def example_data():
    example_data = load_example_data("example.json")  # Explicitly pass the filename
    return jsonify(example_data if example_data else None)

@app.route("/", methods=["GET", "POST"])
def index():
    example_data_form = None  # Initialize to None
    example_type = request.args.get('example_type')  # Get selected example type
    loading = False # Initialize loading state

    # On GET request, try to load example data based on selector
    if request.method == "GET":
        if example_type == 'positive':
            example_data_form = load_example_data("example_positive.json")
        elif example_type == 'negative':
            example_data_form = load_example_data("example_negative.json")
            if example_data_form:
                example_data_form["demographic"] = ""  # Clear demographic for negative case
        else:
            example_data_form = load_example_data("example.json")  # Default file

    if request.method == "POST":
        loading = True # Set loading to True when form is submitted
        # Gather input fields from the form
        applicant_id = request.form.get("applicant_id")
        demographic = request.form.get("demographic")
        loan_amount = request.form.get("loan_amount")
        loan_purpose = request.form.get("loan_purpose")
        description = request.form.get("description")
        credit_score = request.form.get("credit_score")
        annual_income = request.form.get("annual_income")
        employment_status = request.form.get("employment_status")
        loan_criteria_raw = request.form.get("loan_criteria", "")

        # Validate required fields
        if not all([applicant_id, demographic, loan_amount, loan_purpose, description, credit_score, annual_income, employment_status]):
            flash("Please fill in all required fields.", "error")
            return render_template('application.html', example_data=example_data_form, USE_EXAMPLE_SELECTOR=USE_EXAMPLE_SELECTOR, loading=loading) # Pass loading state to template

        # Generate time suffix
        now = datetime.datetime.now()
        time_suffix = now.strftime("%Y-%m-%d-%H-%M") # YYYY-MM-DD-HH-minute format
        modified_applicant_id = f"{applicant_id}+{time_suffix}" # Append suffix using +

        # Build loan application dictionary
        try:
            loan_application = {
                "applicant_id": modified_applicant_id, # Use modified applicant_id here
                "demographic": demographic,
                "loan_amount": float(loan_amount),
                "loan_purpose": loan_purpose,
                "description": description,
                "credit_score": int(credit_score),
                "annual_income": float(annual_income),
                "employment_status": employment_status,
                "loan_criteria": [crit.strip() for crit in loan_criteria_raw.split(",") if crit.strip()]
            }
        except ValueError:
            flash("Invalid input: Ensure numerical fields contain valid numbers.", "error")
            return render_template('application.html', example_data=example_data_form, USE_EXAMPLE_SELECTOR=USE_EXAMPLE_SELECTOR, loading=loading) # Pass loading state to template


        # Convert to JSON
        application_json = json.dumps(loan_application)

        try:
            # Send JSON data to server
            response = requests.post(SERVER_URL, json={"text": application_json})
            print(f"Response content: {response.text}")  # Debugging output

            if response.status_code == 200:
                try:
                    server_response = response.json()
                    final_state = server_response.get("final_state", "")
                    # Check if final_state is a dict or a string
                    if isinstance(final_state, dict):
                        final_decision = final_state.get("final_decision", "unknown")
                    elif isinstance(final_state, str):
                        # Extract final_decision from the string using regex
                        match = re.search(r"final_decision='([^']+)'", final_state)
                        final_decision = match.group(1) if match else "unknown"
                    else:
                        final_decision = "unknown"

                    if final_decision == 'requires further review':
                        flash("Application Flagged for Review.", "warning")
                    elif final_decision == 'approved':
                        flash("Application submitted successfully!", "success")
                    else:
                        flash("Application submitted, but decision is unclear.", "info")

                except json.JSONDecodeError:
                    flash("Server response is not valid JSON.", "error")
            else:
                flash(f"Failed to submit application. Server responded with status {response.status_code}.", "error")

        except requests.exceptions.ConnectionError:
            flash("Error connecting to the server. Please ensure the server is running.", "error")
        except Exception as e:
            flash(f"Unexpected error during request: {e}", "error")
        loading = False # Set loading back to false after response (or error) for next submission, though page redirects

        return redirect(url_for("index"))

    return render_template('application.html', example_data=example_data_form, USE_EXAMPLE_SELECTOR=USE_EXAMPLE_SELECTOR, loading=loading) # Pass loading state to template


if __name__ == '__main__':
    app.run(debug=True, port=5000)