from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_msg = request.json.get("msg")

    try:
        # Stream responses from Ollama
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",     # faster model than llama3
                "prompt": user_msg,     # user message
                "num_predict": 200      # limit reply length (~faster)
             },
            stream=True
        )

        bot_reply = ""
        for line in resp.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    bot_reply += data["response"]
                if data.get("done", False):
                    break
    except Exception as e:
        bot_reply = "⚠️ Error: " + str(e)

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
