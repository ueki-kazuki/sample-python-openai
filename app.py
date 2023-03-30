import json
from flask import Flask, render_template, request, jsonify, session
import openai
from openai.error import RateLimitError
import os

app = Flask(__name__)
app.secret_key = 'super secret key'
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gpt3', methods=['GET', 'POST'])
def gpt3():
    user_input = request.args.get('user_input') if request.method == 'GET' else request.form['user_input']

    if 'messages' in session:
        messages = session['messages']
    else:
        messages = []

    messages.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        content = response.choices[0].message["content"]

        messages.append({"role": "assistant", "content": content})
        session['messages'] = messages
    except RateLimitError:
        content = "The server is experiencing a high volume of requests. Please try again later."

    return jsonify(content=content)

@app.route('/reset', methods=['GET'])
def reset():
    session.clear()
    content = {'message': 'success!'}
    return jsonify(content=content)


if __name__ == '__main__':
    app.run(debug=True)
