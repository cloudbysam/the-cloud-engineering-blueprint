import os
import random
import string
import redis
from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- Database Configuration (PostgreSQL) ---
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "url_db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- Redis Configuration ---
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Initialize Redis connection client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

# --- KGS Settings ---
BASE62_CHARACTERS = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
KGS_REDIS_KEY = "kgs_pool"
MIN_KGS_POOL_SIZE = 20
PREFILL_BATCH_SIZE = 50

# --- Database Schema ---
class URLMapping(db.Model):
    __tablename__ = "url_mappings"
    short_code = db.Column(db.String(10), primary_key=True)
    long_url = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

# --- Helper Function: KGS Pool Manager ---
def generate_random_code(length=7):
    """Generates a random 7-character Base62 string."""
    return ''.join(random.choices(BASE62_CHARACTERS, k=length))

def prefill_kgs_pool():
    """Ensures Redis always has pre-generated unique keys ready for assignement."""
    try:
        current_size = redis_client.scard(KGS_REDIS_KEY)
        if current_size < MIN_KGS_POOL_SIZE:
            new_keys = set()
            while len(new_keys) < PREFILL_BATCH_SIZE:
                new_keys.add(generate_random_code(7))
            
            # Sadd adds the batch of unique keys to the Redis set
            redis_client.sadd(KGS_REDIS_KEY, *new_keys)
            print(f"[KGS Log] Added {len(new_keys)} new keys to pool. Total pool count: {redis_client.scard(KGS_REDIS_KEY)}")
    except redis.RedisError as e:
        print(f"[KGS Warning] Redis unavailable for pool check: {e}")

# --- Routes ---

@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy"}, 200    

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400
    
    long_url = data['url']

    # 1. Ensure Redis KGS pool is full
    prefill_kgs_pool()

    # 2. Pop a pre-generated key from Redis
    try:
        short_code = redis_client.spop(KGS_REDIS_KEY)
    except redis.RedisError:
        # Fallback to local generation if Redis error occurs
        short_code = generate_random_code(7)

    # 3. Save mapping to PostgreSQL (Persistent storage)
    new_mapping = URLMapping(short_code=short_code, long_url=long_url)
    db.session.add(new_mapping)
    db.session.commit()

    # 4. Save mapping to Redis (Read cache with 1-hour expiration)
    try:
        redis_client.setex(name=short_code, time=3600, value=long_url)
    except redis.RedisError as e:
        print(f"[Cache Warning] Failed to write key to Redis cache: {e}")

    host_header = request.host
    return jsonify({"short_url": f"http://{host_header}/{short_code}"}), 201    

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    # STEP 1: Check Redis Read Cache first
    try:
        cached_url = redis_client.get(short_code)
        if cached_url:
            print(f"[Cache HIT] Found {short_code} in Redis!")
            return redirect(cached_url)
    except redis.RedisError as e:
        print(f"[Cache Warning] Redis read error: {e}")

    # STEP 2: Cache Miss -> Fall back to PostgreSQL database query
    print(f"[Cache MISS] Searching PostgreSQL database for {short_code}...")
    mapping = URLMapping.query.filter_by(short_code=short_code).first()
    
    if mapping:
        # Store in Redis so next request becomes a Cache Hit
        try:
            redis_client.setex(name=short_code, time=3600, value=mapping.long_url)
        except redis.RedisError:
            pass
        return redirect(mapping.long_url)
    else:
        return jsonify({"error": "Short URL not found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)