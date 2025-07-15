import os
from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def market_scope_agent(startup_idea):
    prompt = (
        f"Analyze the current market landscape for '{startup_idea}'. "
        "Summarize the major trends and opportunities in 10-15 concise sentences."
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def competitor_agent(startup_idea):
    prompt = (
        f"Identify the top competitors for '{startup_idea}'. "
        "Compare their strengths and weaknesses in 10-15 sentences."
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def pitch_deck_agent(startup_idea, pitch_summary):
    prompt = (
        f"Review this pitch deck summary for '{startup_idea}': {pitch_summary} "
        "Provide feedback and suggestions for improvement in 10-15 sentences."
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        idea = request.form['idea']
        pitch = request.form.get('pitch', '')
        result['market'] = market_scope_agent(idea)
        result['competitor'] = competitor_agent(idea)
        result['pitchdeck'] = pitch_deck_agent(idea, pitch)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
