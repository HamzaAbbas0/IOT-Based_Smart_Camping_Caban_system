from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import datetime
# import Adafruit_DHT
import requests
import time

# Initialize the Flask app
app = Flask(__name__)

# Configure the app with MySQL connection details
app.secret_key = 'Users'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users'

# Initialize the MySQL instance
mysql = MySQL(app)

# DHT11 sensor connected to GPIO 4
# DHT_SENSOR = Adafruit_DHT.DHT11
# DHT_PIN = 4

# Set the WEBAPP_URL variable
WEBAPP_URL = 'http://localhost:5000/receive-data'  # Replace with your desired URL

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT userid, email FROM users WHERE email = %s AND password = %s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['email'] = user['email']
            message = 'Logged in successfully!'
            return render_template('users.html', message=message)
        else:
            message = 'Please enter correct email/password!'
    return render_template('index.html', message=message)


@app.route('/toggle', methods=['POST'])
def toggle():
    if 'state' in request.form:
        state = request.form['state']
        if state == 'on':
            print("LED is on")
            # GPIO.output(LED_PIN, GPIO.HIGH)
        elif state == 'off':
            print("LED is off")
            # GPIO.output(LED_PIN, GPIO.LOW)

        # Store the button state and timestamp in the database
        store_button_state(state, 'led-light')

        return '', 204
    else:
        return 'Invalid request', 400


@app.route('/toggle2', methods=['POST'])
def toggle2():
    if 'state' in request.form:
        state = request.form['state']
        if state == 'on':
            print("Button 2 is on")
            # Code for Button 2 functionality
            # GPIO.output(BUTTON_2_PIN, GPIO.HIGH)
        elif state == 'off':
            print("Button 2 is off")
            # Code for Button 2 functionality
            # GPIO.output(BUTTON_2_PIN, GPIO.LOW)

        # Store the button state and timestamp in the database
        store_button_state(state, 'led-light-1')

        return '', 204
    else:
        return 'Invalid request', 400


@app.route('/toggle3', methods=['POST'])
def toggle3():
    if 'state' in request.form:
        state = request.form['state']
        if state == 'on':
            print("Button 3 is on")
            # Code for Button 3 functionality
            # GPIO.output(BUTTON_3_PIN, GPIO.HIGH)
        elif state == 'off':
            print("Button 3 is off")
            # Code for Button 3 functionality
            # GPIO.output(BUTTON_3_PIN, GPIO.LOW)

        # Store the button state and timestamp in the database
        store_button_state(state, 'Fan')

        return '', 204
    else:
        return 'Invalid request', 400


def store_button_state(state, button_name):
    if 'loggedin' in session and session['loggedin']:
        userid = session['userid']
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        # Store the button state and timestamp in the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO button_states (userid, button_name, state, timestamp) VALUES (%s, %s, %s, %s)',
                       (userid, button_name, state, formatted_time))
        mysql.connection.commit()
        cursor.close()

def read_sensor_data():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print('Temperature: {:.2f}°C, Humidity: {:.2f}%'.format(temperature, humidity))
            send_sensor_data(temperature, humidity)
        else:
            print('Failed to retrieve sensor data')
        time.sleep(5)  # Read sensor data every 5 seconds

def send_sensor_data(temperature, humidity):
    payload = {'temperature': temperature, 'humidity': humidity}
    try:
        response = requests.post(WEBAPP_URL, data=payload)
        if response.status_code == 200:
            print('Sensor data sent successfully')
        else:
            print('Failed to send sensor data. Status code:', response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error sending sensor data:', e)

@app.route('/receive-data', methods=['POST'])
def receive_data():
    temperature = float(request.form['temperature'])
    humidity = float(request.form['humidity'])
    # Process the received sensor data as per your requirements
    # Update the gauge meter or perform any other actions
    print('Received Sensor Data - Temperature: {:.2f}°C, Humidity: {:.2f}%'.format(temperature, humidity))
    return 'Success'

if __name__ == "__main__":
    app.run()
