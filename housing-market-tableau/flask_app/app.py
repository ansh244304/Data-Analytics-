"""
app.py
------
Flask web application to embed the Tableau dashboard and story.

Run:
    cd flask_app
    python app.py

Then open: http://localhost:5000
"""

from flask import Flask, render_template

app = Flask(__name__)

# ── Replace these with your actual Tableau Public embed URLs ────────────────
TABLEAU_DASHBOARD_URL = "https://public.tableau.com/views/YourDashboardName/Dashboard1"
TABLEAU_STORY_URL     = "https://public.tableau.com/views/YourDashboardName/Story1"

@app.route("/")
def index():
    return render_template(
        "index.html",
        dashboard_url=TABLEAU_DASHBOARD_URL,
        story_url=TABLEAU_STORY_URL,
    )

@app.route("/dashboard")
def dashboard():
    return render_template(
        "index.html",
        active_tab="dashboard",
        dashboard_url=TABLEAU_DASHBOARD_URL,
        story_url=TABLEAU_STORY_URL,
    )

@app.route("/story")
def story():
    return render_template(
        "index.html",
        active_tab="story",
        dashboard_url=TABLEAU_DASHBOARD_URL,
        story_url=TABLEAU_STORY_URL,
    )

if __name__ == "__main__":
    app.run(debug=True)
