from flask import Flask, request, jsonify
import graphene
import requests

app = Flask(__name__)

# Root proxy endpoint
@app.route("/", methods=["POST", "GET"])
def graphql_proxy():
    if request.method == "POST":
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "Missing GraphQL query"}), 400

        # Forward the query to the real GraphQL endpoint
        r = requests.post("https://countries.trevorblades.com/", json={"query": data["query"]})
        return jsonify(r.json())

    # Optionally allow GET for testing
    return "GraphQL proxy is alive!", 200

if __name__ == "__main__":
    app.run()
