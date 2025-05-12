from flask import Flask, request
from home_hub import HomeHub
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
hub = HomeHub()

@app.get("/api/v1/home-hub/dht11-reading")
def get_humidity_and_temp():
    humidity_sensor = hub.get_device("dht11")
    print(humidity_sensor.__dict__)
    try:
        humidity = round(humidity_sensor.humidity, 1)
        temperature = humidity_sensor.temperature
        return {
            "humidity": humidity,
            "temperature": temperature
        }
    except Exception as e:
        return e

@app.get("/api/v1/home-hub/rgbled")
def set_rgb_led():
    green = float(request.args.get("green", 0))
    red = float(request.args.get("red", 0))
    blue = float(request.args.get("blue", 0))
    led = hub.get_device("rgb")
    led.color = (red/3,green/3,blue/3)
    return {"red": red, "green": green, "blue": blue}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)