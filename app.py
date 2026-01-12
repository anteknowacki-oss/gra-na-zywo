from flask import Flask
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

teams = {
    "1": {"name": "Orły", "balance": 5000},
    "2": {"name": "Wilki", "balance": 7000}
}

categories = [
    "Historia", "Sport", "Muzyka",
    "Film", "Geografia", "Nauka"
]

current_category = None

@socketio.on("get_state")
def get_state():
    emit("update_state", {
        "teams": teams,
        "category": current_category
    })

@socketio.on("spin_wheel")
def spin_wheel():
    global current_category
    current_category = random.choice(categories)
    emit("wheel_result", current_category, broadcast=True)

@socketio.on("update_balance")
def update_balance(data):
    team_id = data["id"]
    amount = data["amount"]
    teams[team_id]["balance"] += amount
    emit("update_state", {
        "teams": teams,
        "category": current_category
    }, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)


