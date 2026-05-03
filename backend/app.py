from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Club, Event

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------- AUTH ----------------

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    if not data['name'] or not data['email'] or not data['password']:
        return jsonify({'message': 'All fields required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400

    user = User(username=data['name'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Account created successfully'})


@app.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(email=data['email'], password=data['password']).first()

    if user:
        return jsonify({'message': 'Login successful', 'user_id': user.id})
    return jsonify({'message': 'Invalid credentials'}), 401


# ---------------- CLUBS ----------------

@app.route('/clubs', methods=['GET'])
def get_clubs():
    clubs = Club.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "description": c.description
    } for c in clubs])


@app.route('/create_club', methods=['POST'])
def create_club():
    data = request.json

    club = Club(name=data['name'], description=data['description'])
    db.session.add(club)
    db.session.commit()

    return jsonify({"message": "Club created"})


@app.route('/delete_club/<int:id>', methods=['DELETE'])
def delete_club(id):
    club = Club.query.get(id)

    if club:
        db.session.delete(club)
        db.session.commit()

    return jsonify({"message": "Club deleted"})


@app.route('/join_club', methods=['POST'])
def join_club():
    data = request.json
    user = User.query.get(data['user_id'])
    club = Club.query.get(data['club_id'])

    if club not in user.clubs:
        user.clubs.append(club)
        db.session.commit()

    return jsonify({"message": "Joined club"})


@app.route('/leave_club', methods=['POST'])
def leave_club():
    data = request.json
    user = User.query.get(data['user_id'])
    club = Club.query.get(data['club_id'])

    if club in user.clubs:
        user.clubs.remove(club)
        db.session.commit()

    return jsonify({"message": "Left club"})


# ---------------- EVENTS ----------------

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{
        "id": e.id,
        "name": e.name,
        "description": e.description
    } for e in events])


@app.route('/create_event', methods=['POST'])
def create_event():
    data = request.json

    event = Event(name=data['name'], description=data['description'])
    db.session.add(event)
    db.session.commit()

    return jsonify({"message": "Event created"})


@app.route('/update_event/<int:id>', methods=['PUT'])
def update_event(id):
    event = Event.query.get(id)

    if event:
        data = request.json
        event.name = data['name']
        event.description = data['description']
        db.session.commit()

    return jsonify({"message": "Event updated"})


@app.route('/delete_event/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get(id)

    if event:
        db.session.delete(event)
        db.session.commit()

    return jsonify({"message": "Event deleted"})


@app.route('/join_event', methods=['POST'])
def join_event():
    data = request.json
    user = User.query.get(data['user_id'])
    event = Event.query.get(data['event_id'])

    if event not in user.events:
        user.events.append(event)
        db.session.commit()

    return jsonify({"message": "Registered"})


@app.route('/leave_event', methods=['POST'])
def leave_event():
    data = request.json
    user = User.query.get(data['user_id'])
    event = Event.query.get(data['event_id'])

    if event in user.events:
        user.events.remove(event)
        db.session.commit()

    return jsonify({"message": "Cancelled"})


# ---------------- USERS / ADMIN ----------------

@app.route('/members', methods=['GET'])
def members():
    users = User.query.all()

    return jsonify([{
        "id": u.id,
        "username": u.username,
        "clubs": [c.name for c in u.clubs]
    } for u in users])


@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()

    return jsonify([{
        "id": u.id,
        "username": u.username
    } for u in users])


@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if user:
        db.session.delete(user)
        db.session.commit()

    return jsonify({"message": "User deleted"})


if __name__ == "__main__":
    app.run(debug=True)