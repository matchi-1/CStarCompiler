@echo off

cd /d "./backend"
start cmd /k "python app.py"

cd /d "../frontend"
start cmd /k "npm start"


pause
