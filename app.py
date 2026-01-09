# =========================
# headline_agent_api.py
# Daily Headline Explainer Agent (FREE API VERSION - FULL DATASET)
# =========================

import os
import sys
import pandas as pd
from groq import Groq
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# -------------------------
# CONFIG
# -------------------------
DATA_PATH = r"E:\inten\bbc_news.csv"
MODEL_NAME = "llama-3.1-8b-instant"
PAGE_SIZE = 10   # headlines per page

# -------------------------
# LOAD API KEY (ROBUST)
# -------------------------
def get_groq_client():
    API_KEY = os.getenv("GROQ_API_KEY")
    if not API_KEY:
        print("⚠️  GROQ_API_KEY not found in environment.")
        print('👉 Set it permanently using: setx GROQ_API_KEY "your_api_key_here"\n')
        API_KEY = input("🔑 Paste your Groq API key here (will NOT be saved): ").strip()
        if not API_KEY:
            raise ValueError("No API key provided.")
    return Groq(api_key=API_KEY)

# -------------------------
# LOAD DATASET
# -------------------------
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"❌ Dataset not found at {DATA_PATH}")
    sys.exit(1)

required_cols = {"title", "description", "link"}
if not required_cols.issubset(df.columns):
    print(f"❌ Dataset must contain columns: {required_cols}")
    sys.exit(1)

df = df.dropna(subset=["title", "description", "link"])
RECORDS = df[["title", "description", "link"]].to_dict(orient="records")
TOTAL = len(RECORDS)

# -------------------------
# FLASK APP
# -------------------------
app = Flask(__name__)
CORS(app)

@app.route('/headlines', methods=['GET'])
def get_headlines():
    titles = [r['title'] for r in RECORDS]
    return jsonify(titles)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    headline = data.get('headline')
    if not headline:
        return jsonify({'error': 'No headline provided'}), 400
    # Find record by title
    record = next((r for r in RECORDS if r['title'] == headline), None)
    if not record:
        return jsonify({'error': 'Headline not found'}), 404
    result = run_agent(record)
    return jsonify({'result': result})

@app.route('/')
def index():
    return send_from_directory(r'E:\inten', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(r'E:\inten', filename)

# -------------------------
# 4-LAYER PROMPTS
# -------------------------

def input_understanding_prompt(title, description, link):
    return f"""
You are an AI agent that analyzes a news article.

Headline:
"{title}"

Short Description:
"{description}"

Article Link:
{link}

Identify:
1. Topic (economy, politics, sports, etc.)
2. Key entity involved
3. Country (if applicable)
"""

def task_planner_prompt():
    return """
Before answering, follow these steps internally:
1. Understand what happened in the news
2. Use the description and link as context
3. Recall prior background related to this issue
4. Keep the tone neutral and factual
"""

def output_generator_prompt(title):
    return f"""
Generate the final answer strictly in the format below.

Headline:
{title}

Topic:
(one word or short phrase)

Key Entity:
(name)

Summary:
(3–4 lines in very simple language)

Background / History:
(2–3 lines explaining the past context or ongoing situation related to this news)
"""

# -------------------------
# AGENT EXECUTION (API)
# -------------------------
def run_agent(record):
    prompt = (
        input_understanding_prompt(
            record["title"],
            record["description"],
            record["link"]
        )
        + task_planner_prompt()
        + output_generator_prompt(record["title"])
    )

    client = get_groq_client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a neutral news explanation agent."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=350,
    )

    return response.choices[0].message.content.strip()

# -------------------------
# DATASET BROWSER
# -------------------------
def browse_dataset():
    page = 0
    max_page = (TOTAL - 1) // PAGE_SIZE

    while True:
        start = page * PAGE_SIZE
        end = min(start + PAGE_SIZE, TOTAL)

        print(f"\n📄 Headlines {start + 1}–{end} of {TOTAL}\n")
        for i in range(start, end):
            print(f"{i + 1}. {RECORDS[i]['title']}")

        print("\nCommands:")
        print("[number] → select headline")
        print("n → next page | p → previous page")
        print("s → search keyword")
        print("q → quit")

        cmd = input("\nEnter command: ").strip().lower()

        if cmd == "n" and page < max_page:
            page += 1
        elif cmd == "p" and page > 0:
            page -= 1
        elif cmd == "s":
            keyword = input("Enter keyword to search: ").lower()
            matches = [
                (i, r) for i, r in enumerate(RECORDS)
                if keyword in r["title"].lower()
            ]
            if not matches:
                print("❌ No matches found.")
            else:
                print(f"\n🔎 Found {len(matches)} matches (showing first 10):\n")
                for i, r in matches[:10]:
                    print(f"{i + 1}. {r['title']}")
        elif cmd == "q":
            sys.exit(0)
        else:
            try:
                idx = int(cmd) - 1
                if 0 <= idx < TOTAL:
                    return RECORDS[idx]
                else:
                    print("❌ Invalid number.")
            except ValueError:
                print("❌ Invalid command.")

# -------------------------
# MAIN EXECUTION
# -------------------------
if __name__ == "__main__":
    print(f"\n📰 Daily Headline Explainer Agent")
    print(f"📊 Total headlines loaded: {TOTAL}")
    print("🌐 Starting Flask server at http://localhost:5000")
    app.run(debug=True)
