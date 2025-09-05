# app.py
import json

import google.generativeai as genai
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Configure the Gemini API key
# IMPORTANT: Set your API key as an environment variable or in a config file.
# For this example, we'll assume it's set as an environment variable.
# from dotenv import load_dotenv
# import os
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)

# A simple fallback if the API key is not set
try:
    # Replace with your actual API key or use environment variables
    from config import GOOGLE_API_KEY

    genai.configure(api_key=GOOGLE_API_KEY)
except (ImportError, AttributeError):
    print("Warning: config.py with GOOGLE_API_KEY not found. Using a placeholder.")
    # This will likely fail if you don't have a key, but allows the app to run.
    genai.configure(api_key="YOUR_API_KEY_HERE")


@app.route("/")
def index():
    return render_template("index.html")  # Single-page UI


@app.route("/explain", methods=["POST"])
def explain_architecture():
    data = request.get_json()
    table_data = data.get("table")

    if not table_data:
        return jsonify({"error": "No table data provided"}), 400

    # Create a prompt for the Gemini API
    prompt = f"""
    Explain the following CNN architecture table. For each layer, describe what the values for 'k / s / p / d', 'Parameters', 'Out Shape', 'RF', and 'Jump' mean in the context of a Convolutional Neural Network.

    Table Data:
    {json.dumps(table_data, indent=2)}
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        explanation = response.text
        return jsonify({"explanation": explanation})
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": "Failed to get explanation from Gemini API."}), 500


if __name__ == "__main__":
    app.run(debug=True)
