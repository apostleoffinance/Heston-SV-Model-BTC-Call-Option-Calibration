#!/bin/bash

# Start the Heston Model Dashboard
# This script starts both the backend API and frontend dev server

echo "🚀 Starting Heston Model BTC Options Dashboard..."
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Please run this script from the Heston_model_btc directory"
    exit 1
fi

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

# Start backend
echo "📡 Starting FastAPI backend on http://localhost:8000..."
cd backend
pip install -q -r requirements.txt 2>/dev/null
cd ..
python -m uvicorn backend.app.main:app --reload --port 8000 &
BACKEND_PID=$!
sleep 2

# Check if backend started
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Failed to start backend"
    exit 1
fi
echo "✓ Backend running (PID: $BACKEND_PID)"

# Start frontend
echo ""
echo "🎨 Starting React frontend on http://localhost:5173..."
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
sleep 3

# Check if frontend started
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Failed to start frontend"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
echo "✓ Frontend running (PID: $FRONTEND_PID)"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  🎯 Dashboard ready!"
echo ""
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop all servers"
echo "════════════════════════════════════════════════════════════"
echo ""

# Wait for both processes
wait
