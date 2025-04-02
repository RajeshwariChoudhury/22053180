from flask import Flask, request, jsonify
import requests
from collections import deque
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
TIMEOUT = 0.5  # 500ms
NUMBER_TYPES = {
    'p': 'primes',
    'f': 'fibo',
    'e': 'even',
    'r': 'rand'
}
BASE_API_URL = "http://20.244.56.144/evaluation-service/"

# Store numbers in memory (in production, use a database)
number_window = deque(maxlen=WINDOW_SIZE)

# Add this above the fetch_numbers() function
TEST_SERVER_MOCK_DATA = {
    'even': [2,4,6,8],
    'primes': [2,3,5,7],
    'fibo': [1,2,3,5,8],
    'rand': [7,11,4,9]
}

def fetch_numbers(number_type):
    if os.getenv('USE_MOCK') == 'true':  # Add USE_MOCK=true to .env
        return TEST_SERVER_MOCK_DATA[NUMBER_TYPES[number_type]]
    # ... rest of original function ...

def fetch_numbers(number_type):
    """Fetch numbers from the test server API with better error handling"""
    try:
        url = f"{BASE_API_URL}{NUMBER_TYPES[number_type]}"
        print(f"Attempting to fetch from: {url}")  # Debug log
        response = requests.get(url, timeout=TIMEOUT)
        print(f"Response status: {response.status_code}")  # Debug log
        print(f"Response content: {response.text}")  # Debug log
        
        if response.status_code == 200:
            numbers = response.json().get('numbers', [])
            print(f"Fetched numbers: {numbers}")  # Debug log
            return numbers
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
    return []

def calculate_average(numbers):
    """Calculate average of numbers"""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

@app.route('/numbers/<string:number_id>', methods=['GET'])
def handle_numbers(number_id):
    start_time = time.time()
    
    if number_id not in NUMBER_TYPES:
        return jsonify({"error": "Invalid number type"}), 400
    
    # Store previous state before processing
    prev_state = list(number_window)
    
    # Fetch new numbers
    new_numbers = fetch_numbers(number_id)
    
    # Process new numbers (ensure uniqueness and window size)
    for num in new_numbers:
        if num not in number_window:
            number_window.append(num)
    
    # Prepare response
    current_state = list(number_window)
    avg = calculate_average(current_state)
    
    response = {
        "windowPrevState": prev_state,
        "windowCurrState": current_state,
        "numbers": new_numbers,
        "avg": round(avg, 2)
    }
    
    # Ensure total response time < 500ms
    elapsed_time = time.time() - start_time
    if elapsed_time >= TIMEOUT:
        return jsonify({"error": "Processing timeout"}), 500
    
    return jsonify(response)

@app.route('/')
def home():
    return """
    <h1>Average Calculator Microservice</h1>
    <p>Available endpoints:</p>
    <ul>
        <li>/numbers/e - Even numbers</li>
        <li>/numbers/p - Prime numbers</li>
        <li>/numbers/f - Fibonacci numbers</li>
        <li>/numbers/r - Random numbers</li>
    </ul>
    """

if __name__ == '__main__':
    app.run(port=9876, debug=True)