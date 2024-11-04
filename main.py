from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
def data():
    return  mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="shopping_mall"
)

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.getcwd(), 'favicon.ico')

@app.route('/user_registration', methods=['POST'])
def user_registration():
    name= request.json['name']
    email=request.json['email']
    pword=request.json['password']
    print(name,email,pword)
    con=data()
    cursor = con.cursor()
    sql = "insert into customers(email,name,password) value(%s,%s,%s)"
    try:
        cursor.execute(sql, (email,name,pword))
        con.commit()
        return jsonify({'message': 'Registration successful.'}), 200
    except mysql.connector.Error as err:
        app.logger.error('Error inserting data: %s', err)
        return jsonify({'message': 'Registration failed.', 'error': str(err)}), 500
    finally:
        cursor.close()
        con.close()

@app.route('/password_reset', methods=['POST'])
def password_reset():
    email=request.json['email']
    pword=request.json['newpword']
    con=data()
    cursor = con.cursor()
    sql = "alter table customers modify password set password=%s where email=%s"
    try:
        cursor.execute(sql, (pword,email))
        data().commit()
        return jsonify({'message': 'password resetting sucefully.'}), 200
    except mysql.connector.Error as err:
        app.logger.error('Error inserting data: %s', err)
        return jsonify({'message': 'Registration failed.', 'error': str(err)}), 500
    finally:
        cursor.close()
        con.close()

@app.route('/user_login', methods=['POST'])
def user_login():
    email = request.json['email']
    pword = request.json['password']
    print(email,pword)
    con=data()
    cursor = con.cursor()
    query = '''SELECT password FROM customers where email= %s'''
    cursor.execute(query,(email,))
    result = cursor.fetchone()
    cursor.close()
    con.close()
    if result and result[0]==pword:
        return jsonify({'message': 'Login successful.'}), 200
    else:
        return jsonify({"message": "Invalied password."}), 401
   
    
@app.route('/scan', methods=['POST'])
def scan():
    barcode = request.json['barcode']
    print(barcode)
    con=data()
    cursor = con.cursor()
    sql = "SELECT name,cost FROM products WHERE product_id = %s"
    cursor.execute(sql, (barcode,))
    result = cursor.fetchone()
    cursor.close()
    con.close()
    if result:
        return jsonify({"name": result[0], "cost": result[1]})
    else:
        return jsonify({"message": "Product not found"})

'''@app.route('/otp_verify', methods=['POST'])
def otp_verify():
    otp = request.json.get('otp_val')
    to = request.json.get('email')
    subject="Smart cart"
    message="Your smart cart otp: "+str(otp)
    print(otp,to)
    email ="yenugulabhargava143@gmail.com"
    sender_password = "hdmq mxvy tiaw dhse" 
    mail.send_email(email, sender_password,to, subject, message)
    return jsonify({'message': 'OTP sent successfully.'}), 200'''

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(os.getcwd(), path)

if __name__== '__main__':
    app.run(port=5000, host='0.0.0.0')