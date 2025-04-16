#!/bin/bash

# Optional: set display variable for headless Chrome
export DISPLAY=:99

# Start the FastAPI app
uvicorn main:app --host 0.0.0.0 --port ${PORT:-5000}

