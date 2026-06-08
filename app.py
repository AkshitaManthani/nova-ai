from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
# Memory for the conversation
messages = [
    {
        "role": "system",
        "content": "You are Nova, a smart and friendly AI assistant."
    }
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global messages

    user_input = request.json["message"]

    # Store user message in memory
    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    bot_reply = response.choices[0].message.content

    # Store bot reply in memory
    messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)