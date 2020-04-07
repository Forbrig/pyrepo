# Implements the model for the website by simulating a database (for test purpose only)

import json

def load_db():
    with open("data_db.json") as f:
        return json.load(f)

def save_db():
    with open("data_db.json", 'w') as f:
        return json.dump(db, f)

db = load_db()