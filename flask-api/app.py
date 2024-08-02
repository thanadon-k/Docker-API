from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)  

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT')
}

@app.route('/users', methods=['GET'])
def get_users():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute('SELECT * FROM USERS')
        users = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(users)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

@app.route('/user/<uid>', methods=['GET'])
def get_user(uid):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute('SELECT * FROM USERS WHERE uid = %s', (uid,))
        users = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(users)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    
@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    
    if not name or not age:
        return jsonify({'error': 'Name and age are required'}), 400
    
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        cursor.execute('INSERT INTO USERS (name, age) VALUES (%s, %s)', (name, age))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'User added successfully!'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

@app.route('/user/<uid>', methods=['PUT'])
def update_user(uid):
    data = request.json
    name = data.get('name')
    age = data.get('age')
    
    if not name or not age:
        return jsonify({'error': 'Name and age are required'}), 400
    
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        cursor.execute('UPDATE USERS SET name = %s, age = %s WHERE uid = %s', (name, age, uid))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'User updated successfully!'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    
@app.route('/user/<uid>', methods=['DELETE'])
def delete_user(uid):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute('DELETE FROM USERS WHERE uid = %s', (uid,))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({'message':'User deleted successfully!'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
