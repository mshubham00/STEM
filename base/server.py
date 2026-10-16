from flask import Flask, request, jsonify, send_file
import pandas as pd
import os

CSV_FILE = "matrix.csv"

REQUIRED_FIELDS = [
    "concept_id",
    "source",
    "target",
    "relationship",
    "domain",
    "scale",
]


app = Flask(__name__)


@app.route("/")
def index():
    return send_file("knowledge.html")


@app.route("/add_entry", methods=["POST"])
def add_entry():
    data = request.json

    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

    df = pd.read_csv(CSV_FILE)

    if data["concept_id"] in df["concept_id"].values:
        return jsonify({
            "error": "concept_id already exists"
        }), 400

    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    return jsonify({"status": "success"})
    

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/edit_entry", methods=["POST"])
def edit_entry():
    data = request.json
    if "concept_id" not in data:
        return jsonify({"error":"Missing concept_id"}), 400

    df = pd.read_csv(CSV_FILE)

    # Find row
    idx = df.index[df["concept_id"]==data["concept_id"]]
    if len(idx)==0:
        return jsonify({"error":"concept_id not found"}), 404

    idx = idx[0]

    # Update allowed fields
    for field in ["domain","scale"]:
        if field in data:
            df.at[idx, field] = data[field]

    df.to_csv(CSV_FILE,index=False)
    return jsonify({"status":"success"})

