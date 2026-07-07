from flask import Flask, request, redirect, jsonify
import hashlib

app = Flask(__name__)

url_db = {}

def shorten_url(url):
    md5_hash = hashlib.md5(url.encode())
    return md5_hash.hexdigest()[0:7]

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    long_url = data.get('url')

    if not long_url:
        return jsonify({"error": "URL is required"}), 400
    short_code = shorten_url(long_url)
    url_db[short_code] = long_url

    return jsonify({"short_url": f"http://localhost:5000/{short_code}"}), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    long_url = url_db.get(short_code)
    
    if long_url:
        return redirect(long_url)
    else:
        return jsonify({"error": "Short URL not found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

