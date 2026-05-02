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

    if Event.query.count() == 0:
        db.session.add(Event(name="Hackathon", description="Coding competition"))
        db.session.add(Event(name="Workshop", description="Learning session"))
        db.session.add(Event(name="Seminar", description="Guest speaker event"))
        db.session.commit()

    if Club.query.count() == 0:
        db.session.add(Club(name="Coding Club", description="Learn programming"))
        db.session.add(Club(name="Robotics Club", description="Build robots"))
        db.session.add(Club(name="Art Club", description="Creative activities"))
        db.session.commit()

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(
        username=data['username'],
        password=data['password']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully"})

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

@app.route('/join_event', methods=['POST'])
def join_event():
    data = request.json

    user = User.query.get(data['user_id'])
    event = Event.query.get(data['event_id'])

    if event not in user.events:
        user.events.append(event)
        db.session.commit()

    return jsonify({"message": "Registered for event"})

@app.route('/leave_event', methods=['POST'])
def leave_event():
    data = request.json

    user = User.query.get(data['user_id'])
    event = Event.query.get(data['event_id'])

    if event in user.events:
        user.events.remove(event)
        db.session.commit()

    return jsonify({"message": "Cancelled registration"})

if __name__ == '__main__':
    app.run(debug=True)

