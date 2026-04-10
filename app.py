# app.py
from flask import Flask, request, jsonify
import pickle
import pandas as pd
from flask_cors import CORS  # Allow frontend requests

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Load your trained model
import os

model_path = os.path.join(os.path.dirname(__file__), "ipl_model.pkl")
model = pickle.load(open(model_path, "rb"))
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    df = pd.DataFrame([data])
    
    # Get the probability scores
    # [Probability of Loss, Probability of Win]
    probabilities = model.predict_proba(df)[0]
    
    win_percentage = round(probabilities[1] * 100, 1)
    loss_percentage = round(probabilities[0] * 100, 1)
    
    return jsonify({
        "win_percentage": win_percentage,
        "loss_percentage": loss_percentage,
        "batting_team": data['batting_team'],
        "bowling_team": data['bowling_team']
    })
# Only used for local testing
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860) 