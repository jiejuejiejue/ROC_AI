from flask import Flask, request, jsonify, send_from_directory
import torch
from utils import load_models_and_predict, Model, MultiHeadAttention 
from flask_cors import CORS
app = Flask(__name__, static_folder='static')
device = 'cuda' if torch.cuda.is_available() else 'cpu'
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text')
    print(text)
    prediction = load_models_and_predict(text, device)
    return jsonify({'prediction': prediction})
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')
if __name__ == '__main__':
    app.run(debug=True)