from flask import Flask, render_template, request, jsonify
import requests, json, os

app = Flask(__name__)

DATA_FILE = "collections/collections.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"collections": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send_request():
    url = request.form["url"]
    method = request.form["method"].upper()
    body = request.form.get("body", "")

    try:
        if method in ["GET", "DELETE"] and not body.strip():
            resp = requests.request(method, url)
        else:
            resp = requests.request(method, url, data=body)

        try:
            body_data = resp.json()
        except ValueError:
            body_data = resp.text

        return jsonify({
            "status": resp.status_code,
            "headers": dict(resp.headers),
            "body": body_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Collections API ---
@app.route("/collections", methods=["GET"])
def list_collections():
    data = load_data()
    return jsonify(data["collections"])

@app.route("/collections", methods=["POST"])
def create_collection():
    data = load_data()
    new_id = max([c["id"] for c in data["collections"]], default=0) + 1
    new_collection = {"id": new_id, "name": request.json["name"], "requests": []}
    data["collections"].append(new_collection)
    save_data(data)
    return jsonify(new_collection)

@app.route("/collections/<int:cid>/requests", methods=["POST"])
def add_request(cid):
    data = load_data()
    collection = next((c for c in data["collections"] if c["id"] == cid), None)
    if not collection:
        return jsonify({"error": "Collection not found"}), 404
    new_id = max([r["id"] for r in collection["requests"]], default=0) + 1
    new_req = {
        "id": new_id,
        "name": request.json["name"],
        "url": request.json["url"],
        "method": request.json["method"],
        "headers": request.json.get("headers", {}),
        "body": request.json.get("body", "")
    }
    collection["requests"].append(new_req)
    save_data(data)
    return jsonify(new_req)

@app.route("/collections/<int:cid>/requests", methods=["GET"])
def get_requests(cid):
    data = load_data()
    collection = next((c for c in data["collections"] if c["id"] == cid), None)
    if not collection:
        return jsonify({"error": "Collection not found"}), 404
    return jsonify(collection["requests"])

if __name__ == '__main__':
    app.run(debug=True)
