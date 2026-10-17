"""Landing page e acesso ao dashboard local."""

import json
from pathlib import Path

from flask import Flask, render_template


app = Flask(__name__)
CONTENT_PATH = Path(__file__).with_name("content.json")

# Altere esta URL para apontar ao seu dashboard Streamlit.
DASHBOARD_URL = "http://localhost:8501"


def load_content():
    """Lê os textos em UTF-8 a cada acesso para facilitar a edição."""
    with CONTENT_PATH.open(encoding="utf-8") as source:
        return json.load(source)


@app.get("/")
def index():
    return render_template("index.html", content=load_content())


@app.get("/dashboard")
def dashboard():
    return render_template(
        "redirect.html", content=load_content(), dashboard_url=DASHBOARD_URL
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
