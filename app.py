from flask import Flask, request, jsonify, render_template
from db_connection import product_collection, user_collection
from utils.jwt_utils import generate_token, validate_token
import bcrypt
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef1234561'

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Product API!"})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password'].encode('utf-8')

    if user_collection.find_one({'username': username}):
        return jsonify({'message': 'User already exists'}), 400

    hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
    user_collection.insert_one({'username': username, 'password': hashed_pw})
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password'].encode('utf-8')

    user = user_collection.find_one({'username': username})
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    if bcrypt.checkpw(password, user['password']):
        token = generate_token(username)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/summary', methods=['GET'])
def summary():
    # Read summary report from CSV
    summary_df = pd.read_csv('summary_report.csv')
    return render_template('summary.html', data=summary_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
