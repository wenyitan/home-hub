from flask import Flask, request
from home_hub import HomeHub
from flask_cors import CORS
from pathlib import Path
import json
import subprocess
from enum import Enum
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from logging_config import logger


app = Flask(__name__)
CORS(app)
hub = HomeHub()

class OperationMode(Enum):
    Low = 1
    Medium = 2
    High = 3
    Auto = 4

@app.get("/api/v1/home-hub/dht11-reading")
def get_humidity_and_temp():
    humidity_sensor = hub.get_device("dht11")
    try:
        humidity = round(humidity_sensor.humidity, 1)
        temperature = humidity_sensor.temperature
        if humidity > 70:
            work_humidifier("off")
        elif humidity < 50:
            work_humidifier("on")
        return {
            "humidity": humidity,
            "temperature": temperature
        }
    except Exception as e:
        return {"error": f"Something went wrong: {str(e)}"}, 500

@app.get("/api/v1/home-hub/rgbled")
def set_rgb_led():
    try:
        green = float(request.args.get("green", 0))
        red = float(request.args.get("red", 0))
        blue = float(request.args.get("blue", 0))
    except (ValueError, TypeError):
        return {"error": "Please provide the rgb values as numbers"}, 400

    led = hub.get_device("rgb")
    if not led:
        return {"error": "RGB LED Device not found. Please check the key"}, 500
    
    try:
        led.color = (red/3,green/3,blue/3)
        return {"red": red, "green": green, "blue": blue}
    except Exception as e:
        return {"error": f"Something went wrong when setting LED color: {str(e)}"}, 500

@app.get("/api/v1/home-hub/app-health")
def get_app_health():
    config_file = Path(__file__).with_name("apps.json")
    docker_output = subprocess.run(['docker', 'ps', '--format', 'json'], capture_output=True, text=True)
    docker_output = docker_output.stdout.replace('\\"', '\'').replace("\n", ",")
    docker_output = "[" + docker_output[:-1] + "]"

    with config_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    result = []
    for app in data:
        deployment_type = app["deployment_type"]
        if deployment_type == "docker":
            docker = [output for output in json.loads(docker_output) if output['Names'] == app['keyword']]
            if len(docker) == 1:
                result.append({
                    "app": app['name'],
                    "environment": app['environment'],
                    "status": docker[0]["State"] == "running"
                })
            else:
                result.append({
                    "app": app['name'],
                    "environment": app['environment'],
                    "status": "app not found/cannot be found"
                })
            continue
        elif deployment_type == "ps":
            ps = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
            grep = subprocess.Popen(["grep", app['keyword']], stdin=ps.stdout, stdout=subprocess.PIPE)
            ps.stdout.close()  # Allow ps to receive a SIGPIPE if grep exits
            output, _ = grep.communicate()
            outputs = output.decode().split("\n")
            output = [output.strip() for output in outputs if "grep" not in output and app['keyword'] in output]
            if len(output) == 1:
                result.append({
                    "app": app['name'],
                    "environment": app['environment'],
                    "status": True
                })
            else:
                result.append({
                    "app": app['name'],
                    "environment": app['environment'],
                    "status": "app not found/cannot be found"
                })
            continue

    return result

@app.get("/api/v1/home-hub/humidifier/<resource>") ## get_properties_for_mapping gives piid and siid
def work_humidifier(resource):
    humidifier = hub.get_device("humidifier")
    status = humidifier.status().data
    
    if resource in dir(humidifier):
        if resource in ["on", "off"]:
            if status["buzzer"]:
                humidifier.set_buzzer(False)
            if status["led_light"]:
                humidifier.set_light(False)
            power = status["power"]
            if (power and resource == "off") or (not power and resource =="on"):
                getattr(humidifier, resource)()
                now = datetime.datetime.now()
                logger.info(f"Humidifier powered {resource} at {now}.")
                return "Success"
            else:
                return f"Nothing was done as the power is already {resource}."
        elif resource == "status":
            return status
        else:
            try:
                return getattr(humidifier, resource)().__dict__
            except TypeError:
                return {"error": "method not supported", "status_code": 400}, 400
    else:
        return {"error": "method not supported", "status_code": 400}, 400

@app.get("/api/v1/home-hub/humidifier/toggle-mode")
def toggle_humidifier_mode():
    humidifier = hub.get_device("humidifier")
    status = humidifier.status().data
    power = status["power"]
    mode = status["mode"]
    if mode == 4:
        to_set = 1
    else:
        to_set = mode + 1
    if power:
        humidifier.set_mode(OperationMode(to_set))
        return {"message": f"success, mode set to {to_set}"}
    else:
        return {"message": f"Nothing was changed as the power is off"}

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_humidity_and_temp, "cron", hour="0-8,20-23", misfire_grace_time=60)
    scheduler.start()
    app.run(host="0.0.0.0", port=5001)