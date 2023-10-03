from flask import Flask, request, render_template, jsonify
import openai
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config['API']['api_key']

conversation = []
system_message = "You are a helpful assistant."

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_text', methods=['POST'])
def process_text():
    if request.method == 'POST':
        data = request.get_json()
        input_text = data.get('text', '')
        conversation.append({"role": "user", "content": input_text})

        messages = [
            {"role": "system", "content": system_message}] + conversation

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        if response["choices"][0]["message"]["content"]:
            assistant_reply = response["choices"][0]["message"]["content"]
            result = assistant_reply
            conversation.append(
                {"role": "assistant", "content": assistant_reply})
        else:
            result = "Failed to get a response from the ChatGPT API."

        response = {"output_text": result}
        return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
