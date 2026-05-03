from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Club, Event

app = Flask(__name__)

# ✅ VERY IMPORTANT: proper CORS config
CORS(app, supports_credentials=True)

# ✅ HANDLE PREFLIGHT (this fixes your exact error)
@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        return response

# ✅ ALSO ADD HEADERS TO EVERY RESPONSE
@app.after_request
def add_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response

# ---------------- CONFIG ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------------- INIT DB ----------------
with app.app_context():
    db.create_all()

    if Event.query.count() == 0:
        db.session.add_all([
            Event(name="Hackathon", description="Coding competition"),
            Event(name="Workshop", description="Learning session"),
            Event(name="Seminar", description="Guest speaker event")
        ])
        db.session.commit()

    if Club.query.count() == 0:
        db.session.add_all([
            Club(name="Coding Club", description="Learn programming"),
            Club(name="Robotics Club", description="Build robots"),
            Club(name="Art Club", description="Creative activities")
        ])
        db.session.commit()

# ---------------- AUTH ----------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'message': 'All fields are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    user = User(username=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Account created successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(
        email=data['email'],
        password=data['password']
    ).first()

    if user:
        return jsonify({"message": "Login successful", "user_id": user.id})
    return jsonify({"message": "Invalid credentials"}), 401

# ---------------- CLUBS ----------------
@app.route('/clubs', methods=['GET'])
def get_clubs():
    clubs = Club.query.all()
    return jsonify([
        {"id": c.id, "name": c.name, "description": c.description}
        for c in clubs
    ])

@app.route('/join_club', methods=['POST'])
def join_club():
    data = request.json
    user = User.query.get(data['user_id'])
    club = Club.query.get(data['club_id'])

    if club in user.clubs:
        return jsonify({"message": "Already joined"}), 400

    user.clubs.append(club)
    db.session.commit()
    return jsonify({"message": "Joined club"})

@app.route('/leave_club', methods=['POST'])
def leave_club():
    data = request.json
    user = User.query.get(data['user_id'])
    club = Club.query.get(data['club_id'])

    if club not in user.clubs:
        return jsonify({"message": "Not a member"}), 400

    user.clubs.remove(club)
    db.session.commit()
    return jsonify({"message": "Left club"})

# ---------------- EVENTS ----------------
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([
        {"id": e.id, "name": e.name, "description": e.description}
        for e in events
    ])

@app.route('/join_event', methods=['POST'])
def join_event():
    data = request.json
    user = User.query.get(data['user_id'])
    event = Event.query.get(data['event_id'])

    if event in user.events:
        return jsonify({"message": "Already registered"}), 400

    user.events.append(event)
    db.session.commit()
    return jsonify({"message": "Registered"})

@app.route('/leave_event', methods=['POST'])
def leave_event():
    data = request.json
    user = User.query.get(data['user_id'])
    event = Event.query.get(data['event_id'])

    if event not in user.events:
        return jsonify({"message": "Not registered"}), 400

    user.events.remove(event)
    db.session.commit()
    return jsonify({"message": "Cancelled"})

# ---------------- ADMIN ----------------
@app.route('/members', methods=['GET'])
def get_members():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "clubs": [c.name for c in u.clubs]
        }
        for u in users
    ])

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "username": u.username}
        for u in users
    ])

@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)