from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ------------------ ASSOCIATION TABLES ------------------

membership = db.Table('membership',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)

event_registration = db.Table('event_registration',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

# ------------------ MODELS ------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    clubs = db.relationship('Club', secondary=membership, backref='members')
    events = db.relationship('Event', secondary=event_registration, backref='participants')


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))


# ------------------ AUTH ------------------

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    new_user = User(
        username=data['username'],
        password=data['password']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"})


@app.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(
        username=data['username'],
        password=data['password']
    ).first()

    if user:
        return jsonify({
            "message": "Login successful",
            "user_id": user.id
        })
    else:
        return jsonify({"message": "Invalid credentials"}), 401


# ------------------ CLUBS ------------------

@app.route('/clubs', methods=['GET'])
def get_clubs():
    clubs = Club.query.all()

    result = []
    for club in clubs:
        result.append({
            "id": club.id,
            "name": club.name,
            "description": club.description
        })

    return jsonify(result)


@app.route('/create_club', methods=['POST'])
def create_club():
    data = request.json

    club = Club(name=data['name'], description=data['description'])
    db.session.add(club)
    db.session.commit()

    return jsonify({"message": "Club created successfully"})


@app.route('/delete_club/<int:id>', methods=['DELETE'])
def delete_club(id):
    club = Club.query.get(id)

    if not club:
        return jsonify({"message": "Club not found"}), 404

    db.session.delete(club)
    db.session.commit()

    return jsonify({"message": "Club deleted successfully"})


@app.route('/join_club', methods=['POST'])
def join_club():
    data = request.json

    user = User.query.get(data['user_id'])
    club = Club.query.get(data['club_id'])

    if not user or not club:
        return jsonify({"message": "User or Club not found"}), 404

    if club not in user.clubs:
        user.clubs.append(club)
        db.session.commit()

    return jsonify({"message": "Joined club"})


@app.route('/leave_club', methods=['POST'])
def leave_club():
    data = request.json

    user = User.query.get(data['user_id'])
    club = Club.query.get(data['club_id'])

    if not user or not club:
        return jsonify({"message": "User or Club not found"}), 404

    if club in user.clubs:
        user.clubs.remove(club)
        db.session.commit()

    return jsonify({"message": "Left club"})


# ------------------ EVENTS ------------------

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()

    result = []
    for event in events:
        result.append({
            "id": event.id,
            "name": event.name,
            "description": event.description
        })

    return jsonify(result)


@app.route('/create_event', methods=['POST'])
def create_event():
    data = request.json

    event = Event(name=data['name'], description=data['description'])
    db.session.add(event)
    db.session.commit()

    return jsonify({"message": "Event created successfully"})


@app.route('/update_event/<int:id>', methods=['PUT'])
def update_event(id):
    event = Event.query.get(id)

    if not event:
        return jsonify({"message": "Event not found"}), 404

    data = request.json
    event.name = data['name']
    event.description = data['description']

    db.session.commit()

    return jsonify({"message": "Event updated successfully"})


@app.route('/delete_event/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get(id)

    if not event:
        return jsonify({"message": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({"message": "Event deleted successfully"})


@app.route('/join_event', methods=['POST'])
def join_event():
    data = request.json

    user = User.query.get(data['user_id'])
    event = Event.query.get(data['event_id'])

    if not user or not event:
        return jsonify({"message": "User or Event not found"}), 404

    if event not in user.events:
        user.events.append(event)
        db.session.commit()

    return jsonify({"message": "Registered for event"})


@app.route('/leave_event', methods=['POST'])
def leave_event():
    data = request.json

    user = User.query.get(data['user_id'])
    event = Event.query.get(data['event_id'])

    if not user or not event:
        return jsonify({"message": "User or Event not found"}), 404

    if event in user.events:
        user.events.remove(event)
        db.session.commit()

    return jsonify({"message": "Event registration cancelled"})


# ------------------ ADMIN ------------------

@app.route('/members', methods=['GET'])
def get_members():
    users = User.query.all()

    result = []
    for user in users:
        result.append({
            "username": user.username,
            "clubs": [club.name for club in user.clubs]
        })

    return jsonify(result)


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    return jsonify([
        {"id": user.id, "username": user.username}
        for user in users
    ])


@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"})


# ------------------ RUN ------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)