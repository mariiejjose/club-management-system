from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Club, Event

app = Flask(__name__)
CORS(app)

@app.after_request
def fix_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

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
    try:
        data = request.get_json()
        print("DATA RECEIVED:", data)

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        print(name, email, password)

        if not name or not email or not password:
            return jsonify({'message': 'All fields are required'}), 400

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return jsonify({'message': 'User already exists'}), 400

        new_user = User(username=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Account created successfully'})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({'message': 'Server error'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(
        email=data['email'],
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

    if club in user.clubs:
        return jsonify({"message": "Already joined this club"}), 400

    if club not in user.clubs:
        user.clubs.append(club)
        db.session.commit()

    return jsonify({"message": "Joined club"})


@app.route('/leave_club', methods=['POST'])
def leave_club():
    data = request.json

    user = User.query.get(data.get('user_id'))
    club = Club.query.get(data.get('club_id'))

    if not user:
        return jsonify({"message": "User not found"}), 400

    if not club:
        return jsonify({"message": "Club not found"}), 400

    if club not in user.clubs:
        return jsonify({"message": "You are not a member of this club"}), 400

    user.clubs.remove(club)
    db.session.commit()

    return jsonify({"message": "Left club successfully"})

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

    if event in user.events:
        return jsonify({"message": "Already registered"}), 400

    if event not in user.events:
        user.events.append(event)
        db.session.commit()

    return jsonify({"message": "Registered for event"})

@app.route('/leave_event', methods=['POST'])
def leave_event():
    data = request.json

    user = User.query.get(data.get('user_id'))
    event = Event.query.get(data.get('event_id'))

    if not user:
        return jsonify({"message": "User not found"}), 400

    if not event:
        return jsonify({"message": "Event not found"}), 400

    if event not in user.events:
        return jsonify({"message": "You are not registered for this event"}), 400

    user.events.remove(event)
    db.session.commit()

    return jsonify({"message": "Cancelled registration"})

@app.route('/create_club', methods=['POST'])
def create_club():
    data = request.json

    new_club = Club(
        name=data['name'],
        description=data['description']
    )

    db.session.add(new_club)
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

@app.route('/create_event', methods=['POST'])
def create_event():
    data = request.json

    new_event = Event(
        name=data['name'],
        description=data['description']
    )

    db.session.add(new_event)
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

@app.route('/members', methods=['GET'])
def get_members():
    users = User.query.all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "clubs": [club.name for club in user.clubs]
        })

    return jsonify(result)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username
        })

    return jsonify(result)

@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

