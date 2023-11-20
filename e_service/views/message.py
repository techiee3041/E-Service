# Inside routes.py

from flask import request, jsonify
from flask_login import current_user
from e_service.models.data import Message, User, Trader
from e_service.app import app, db

# Route for sending a message
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    receiver_id = data.get('receiver_id')
    content = data.get('content')

    # Check if the receiver_id is valid
    if not User.query.get(receiver_id) and not Trader.query.get(receiver_id):
        return jsonify({'error': 'Invalid receiver ID'}), 400

    # Create a new message
    message = Message(sender_id=current_user.get_id(), receiver_id=receiver_id, content=content)
    db.session.add(message)
    db.session.commit()

    return jsonify({'success': 'Message sent successfully'})

# Route for fetching messages
@app.route('/fetch_messages')
def fetch_messages():
    # Fetch both sent and received messages for the current user
    sent_messages = current_user.sent_messages.all()
    received_messages = current_user.received_messages.all()

    # You can format the messages as needed before sending them to the client
    messages = {
        'sent_messages': [{'sender_id': msg.sender_id, 'content': msg.content, 'timestamp': msg.timestamp} for msg in sent_messages],
        'received_messages': [{'sender_id': msg.sender_id, 'content': msg.content, 'timestamp': msg.timestamp} for msg in received_messages]
    }

    return jsonify(messages)