#!/bin/bash
# Start frontend
cd frontend/
npm start &
cd ../

# Detect OS and activate virtual environment accordingly
if [[ -d "venv/Scripts" ]]; then
	# Windows (Git Bash, MSYS, Cygwin)
	source venv/Scripts/activate
elif [[ -d "venv/bin" ]]; then
	# Linux/macOS
	source venv/bin/activate
else
	echo "No valid virtual environment found."
	exit 1
fi

# Start backend
uvicorn app.main:app --reload &
