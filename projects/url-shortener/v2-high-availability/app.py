import os
import hashlib
from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configure database connection via environment variable
# in Production, AWS RDS credentials will be injected here,
# Defaulting to local postgres for developmemt testing.

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "url_db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?sslmode=require"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define the Database schema (The URL Table)
class URLMapping(db.Model):
    __tablename__ = "url_mappings"
    short_code = db.Column(db.String(10), primary_key=True)
    long_url = db.Column(db.Text, nullable=False)

# Ensure database tables exist before handling request
with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy"}, 200    

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400
    
    long_url = data['url']

    hash_object = hashlib.md5(long_url.encode('utf-8'))
    short_code  = hash_object.hexdigest()[0:7]

    # check if this short code already exists in the database
    existing = URLMapping.query.filter_by(short_code=short_code).first()

    if not existing:
        # save to PostgreSQl
        new_mapping = URLMapping(short_code=short_code, long_url=long_url)
        db.session.add(new_mapping)
        db.session.commit()
    
    # Use the request's Host header so it matches the ALB DNS name or IP dynamically
    host_header = request.host
    return jsonify({"short_url": f"http://{host_header}/{short_code}"}), 201    

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    mapping = URLMapping.query.filter_by(short_code=short_code).first()
    
    if mapping:
        return redirect(mapping.long_url)
    else:
        return jsonify({"error": "Short URL not found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

