from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def graphql_proxy():
    print(">>> METHOD:", request.method)
    print(">>> HEADERS:", dict(request.headers))
    print(">>> BODY:", request.get_data())

    if request.method == "POST":
        data = request.get_json()
        print(">>> JSON:", data)

        if not data or "query" not in data:
            return jsonify({"error": "Missing GraphQL query"}), 400

        # Forward the query to the Countries GraphQL API
        r = requests.post("https://countries.trevorblades.com/", json={"query": data["query"]})
        return jsonify(r.json())

    return "GraphQL proxy is alive!", 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # use Render-assigned port if present
    app.run(host="0.0.0.0", port=port)
