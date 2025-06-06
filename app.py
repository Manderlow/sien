from flask import Flask, request, jsonify
import re
import requests
import pandas as pd

app = Flask(__name__)

def sql_to_graphql(sql_query):
    match = re.match(r"SELECT\s+(.*?)\s+FROM\s+(\w+);?", sql_query.strip(), re.IGNORECASE)
    if not match:
        raise ValueError("Only simple SELECT queries are supported")

    columns = [col.strip() for col in match.group(1).split(",")]
    table = match.group(2)

    graphql_query = f"""{{
  {table} {{
    {' '.join(columns)}
  }}
}}"""
    return graphql_query, table

def run_graphql_query(gql_query):
    url = "https://countries.trevorblades.com/"
    response = requests.post(url, json={"query": gql_query})
    return response.json()

@app.route("/query", methods=["POST"])
def handle_query():
    try:
        sql_query = request.json.get("query")
        gql_query, table = sql_to_graphql(sql_query)
        gql_response = run_graphql_query(gql_query)

        # Convert to SQL-style result
        data = gql_response["data"][table]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/")
def home():
    return "GraphQL SQL Proxy is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
