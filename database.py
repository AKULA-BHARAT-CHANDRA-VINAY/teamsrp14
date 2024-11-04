import mysql.connector

def data():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="shopping_mall"
    )

def user_registration():
    name="Bhargava"
    email="yenugulabhargava123@gmail.com"
    pword="123"
    print(name, email, pword)
    con = data()
    cursor = con.cursor()
    sql = "INSERT INTO customers(email, name, password) VALUES (%s, %s, %s)"
    try:
        cursor.execute(sql, (email, name, pword))
        con.commit()
        return {'message': 'Registration successful.'}
    except mysql.connector.Error as err:
        return {'message': 'Registration failed.', 'error': str(err)}
    finally:
        cursor.close()
        con.close()

print(user_registration())
