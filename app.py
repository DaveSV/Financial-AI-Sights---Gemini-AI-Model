from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import os
from dotenv import load_dotenv

model = genai.GenerativeModel('gemma-3-1b-it')

import os
my_api_key_gemini = os.getenv('api_key_gemini')

genai.configure(api_key=my_api_key_gemini)

app = Flask(__name__)

# Define your 404 error handler to redirect to the index page
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            prompt = request.form['prompt']
            question = prompt

            response = model.generate_content(question)

            if response.text:
                print(response.text)
                return response.text
            else:
                return "Sorry, but I think Gemini didn't want to answer that!"
        except Exception as e:
            return "Sorry, but Gemini didn't want to answer that!"

    return render_template('index.html', **locals())

if __name__ == '__main__':
    app.run(debug=True)
