#!/bin/bash

# Navigate to your project directory
cd /home/wenyi/apps/home-hub

# Activate your virtual environment
source venv/bin/activate

# Run the app in the background using nohup
nohup python3 main.py > app.log 2>&1 &