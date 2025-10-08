from flask import Flask, render_template, request, jsonify
import requests, json, os

app = Flask(__name__)

DATA_FILE = "collections/collections.json"
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)


def convert_to_simple(json_data):
    if isinstance(json_data, dict) and "collections" in json_data:
        return json_data
    if not isinstance(json_data, dict) or "item" not in json_data:
        raise ValueError("Collection is neither simplified or a postman formtt.")
    collections = []
    collection_id = 1

    def flatten_items(items):
        requests = []
        request_id = 1
        for item in items:
            if "request" in item:
                req = item["request"]
                headers = {h["key"]: h["value"] for h in req.get("header", [])}
                body = ""
                if "body" in req and "raw" in req["body"]:
                    body = req["body"]["raw"]
                url = ""
                if isinstance(req.get("url"), dict):
                    url = req["url"].get("raw", "")
                requests.append({
                    "id": request_id,
                    "name": item.get("name", f"request_{request_id}"),
                    "url": url,
                    "method": req.get("method", "GET"),
                    "headers": headers,
                    "body": body
                })
                request_id += 1
            elif "item" in item:
                nested_requests = flatten_items(item["item"])
                for r in nested_requests:
                    r["id"] = request_id
                    request_id += 1
                requests.extend(nested_requests)
        return requests
    collection_name = json_data.get("info", {}).get("name", f"collection_{collection_id}")
    requests = flatten_items(json_data["item"])
    collections.append({
        "id": collection_id,
        "name": collection_name,
        "requests": requests
    })
    return {"collections": collections}


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"collections": []}    
    with open(DATA_FILE) as f:
        data = json.load(f)
    return data


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/collections/upload", methods=["POST"])
def upload_collection():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if not file.filename.endswith(".json"):
        return jsonify({"error": "File must be JSON"}), 400
    try:
        postman_data = json.load(file)
        simple_data = convert_to_simple(postman_data)
        data = load_data()
        next_cid = max([c["id"] for c in data["collections"]], default=0) + 1
        for coll in simple_data["collections"]:
            coll["id"] = next_cid
            next_cid += 1
            data["collections"].append(coll)
        save_data(data)
        return jsonify({"message": "Collection uploaded successfully", "collections": simple_data["collections"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
