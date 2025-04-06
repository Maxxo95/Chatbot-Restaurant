from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# Path to the CSV file
CSV_PATH = "messages_for_labeling.csv"

# Load or initialize the dataset
if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
else:
    df = pd.DataFrame(columns=["message", "label"])

df.fillna("", inplace=True)

@app.route('/')
def serve_page():
    return send_from_directory('.', 'index.html')

@app.route('/message/<int:index>', methods=['GET'])
def get_message(index):
    if index >= len(df):
        return jsonify({"done": True})
    row = df.iloc[index]
    return jsonify({
        "index": index,
        "message": row["message"],
        "label": row["label"]
    })

@app.route('/label', methods=['POST'])
def save_label():
    data = request.get_json()
    index = data.get("index")
    label = data.get("label")
    if 0 <= index < len(df):
        df.at[index, "label"] = label
        df.to_csv(CSV_PATH, index=False)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Invalid index"}), 400

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
