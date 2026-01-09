# Daily-Headline-Explainer-Agent
The Daily Headline Explainer Agent is an AI-powered system that helps users quickly understand news headlines from a large newspaper dataset. It identifies the topic, key entities, and generates a simple summary along with brief historical context.


##  Problem Statement
Modern news platforms publish thousands of articles daily, making it difficult for readers to interpret and contextualize headlines efficiently. Many users do not have the time or background knowledge to read full articles. This project addresses this challenge by transforming raw news headlines into clear, structured explanations.



## Solution Overview
The agent analyzes headlines along with their descriptions and links to:
- Identify the topic of the news
- Extract key entities involved
- Generate a simple summary
- Provide brief historical background for context

The system uses a **multi-layer prompt design** to ensure structured reasoning and consistent output quality.



##  Key Features
- Works on a large BBC News dataset
- Generates topic, entity, summary, and background
- Neutral and factual tone (no opinions or predictions)
- Supports custom user-entered headlines
- Interactive web-based interface
- Fast inference using a free LLM API
- Modular and scalable agent design

---

##  System Architecture
The agent is built using a **4-layer prompt architecture**:

1. **Input Understanding**  
   Interprets the headline, description, and link to extract core information.

2. **State Tracker**  
   Maintains short-term context such as topic and entity across prompt layers.

3. **Task Planner**  
   Guides the reasoning process step by step while avoiding bias.

4. **Output Generator**  
   Produces a structured and readable explanation for the user.

Prompt chaining is used so that each layer builds upon the output of the previous one.


## 🖥️ Tech Stack
- **Backend:** Python
- **AI Model:** Groq API 
- **Frontend:** HTML, CSS, JavaScript
- **Web Framework:** Flask
- **Dataset:** BBC News Dataset

## How to Run the Project

1.Install Dependencies
   pip install pandas groq flask
2.Set the Groq API Key
   setx GROQ_API_KEY "your_api_key_here"
3.Run the Application
   python app.py
4️.Open in Browser
   http://127.0.0.1:5000
