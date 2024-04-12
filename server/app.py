from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder = None  # Use default JSON encoder for Flask
CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at).all()
        return jsonify([message.to_dict() for message in messages]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    if request.method == 'PATCH':
        data = request.get_json()
        for attr, value in data.items():
            setattr(message, attr, value)
        db.session.commit()
        return jsonify(message.to_dict()), 200
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return jsonify({'deleted': True}), 200

if __name__ == '__main__':
    app.run(port=5555)
