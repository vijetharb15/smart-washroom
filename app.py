from flask import Flask, jsonify
from flask_cors import CORS
import sensors
import cloudinary
import cloudinary.uploader
import json
import time
from twilio.rest import Client

app = Flask(__name__)
CORS(app)

# Configure Cloudinary
cloudinary.config(
    cloud_name="VSM",
    api_key="958442858159867",
    api_secret="AE__eF9uBJjD3AWCjHoDm2vMuY4"
)

# Configure Twilio
twilio_client = Client("AC33c03d8fdc315d430b585eb0017d88c8", "b0c8b1d7f5e571a03de271d1fc6f2da8")
TWILIO_PHONE = "+18572292585"
TO_PHONE = "+916363760493"

# Track motion frequency for crowding
motion_count = 0
last_notification_time = 0
NOTIFICATION_COOLDOWN = 300  # 5 minutes in seconds

def send_notification(message):
    """Send SMS notification via Twilio."""
    global last_notification_time
    current_time = time.time()
    if current_time - last_notification_time < NOTIFICATION_COOLDOWN:
        return
    try:
        twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=TO_PHONE
        )
        last_notification_time = current_time
        print(f"Sent notification: {message}")
    except Exception as e:
        print(f"Twilio error: {e}")

def upload_sensor_data_to_cloudinary(data):
    """Upload sensor data as a JSON file to Cloudinary."""
    try:
        json_data = json.dumps(data)
        response = cloudinary.uploader.upload(
            json_data,
            resource_type="raw",
            public_id=f"sensor_data_{int(time.time())}",
            folder="smart_washroom_data"
        )
        print(f"Uploaded to Cloudinary: {response['url']}")
        return response['url']
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None

@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    """Fetch sensor readings, upload to Cloudinary, and send notifications."""
    global motion_count
    data = sensors.read_sensors()
    upload_sensor_data_to_cloudinary(data)

    if data["odorLevel"] < 50:
        send_notification("Alert: Bad odor detected in washroom!")
    if data["motionDetected"]:
        motion_count += 1
        if motion_count > 3:
            send_notification("Alert: Washroom is crowded!")
            motion_count = 0
    else:
        motion_count = max(0, motion_count - 1)
    if data["soapLevel"] < 10 and data["soapLevel"] != -1:
        send_notification("Alert: Soap level is low!")

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # Changed port to 5000