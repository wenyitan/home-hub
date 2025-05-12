#!/bin/bash

# Navigate to your project directory
cd /home/wenyi/apps/home-hub/homehub_ui

# Run the app in the background using nohup
nohup npm start > homehub.log 2>&1 &