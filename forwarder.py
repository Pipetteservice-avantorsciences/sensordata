from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def forward_webhook():
    try:
        # Get the incoming JSON payload
        data = request.get_json()

        # Forward it to your local endpoint
        response = requests.post('http://localhost:8501/webhook', json=data)

        # Return status
        return f"Forwarded with status {response.status_code}", response.status_code
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)