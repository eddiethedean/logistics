#!/bin/bash
# Run the Logistics COP Streamlit app on port 8080

echo "Starting Logistics COP on port 8080..."
echo "Access the app at: http://localhost:8080"
echo "Press Ctrl+C to stop the server"

cd "$(dirname "$0")"
streamlit run app.py --server.port 8080 --server.address 0.0.0.0
