# Save this as news_proxy.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NEWSAPI_KEY = "5f9e1ef3deac411d90b22c1faa939733"

@app.route('/news', methods=['GET'])
def get_news():
    topic = request.args.get('topic')
    if not topic:
        return jsonify({"error": "Missing 'topic' parameter"}), 400
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={topic}&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"apiKey={NEWSAPI_KEY}&"
        f"pageSize=3"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        return jsonify({"error": "News API error", "details": resp.text}), 502
    data = resp.json()
    articles = data.get("articles", [])
    result = []
    for a in articles:
        result.append({
            "title": a["title"],
            "source": a["source"]["name"],
            "url": a["url"],
            "publishedAt": a["publishedAt"]
        })
    return jsonify({"news": result})

if __name__ == "__main__":
    app.run(port=8080)
