from flask import Flask, request, jsonify
from bardapi import Bard
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve Bard API token from environment variable
bard_api_token = os.environ.get('BARD_API_TOKEN')

@app.route('/get-chat', methods=['POST'])
def get_chat():
    try:
        data = request.json

        if 'message' in data:
            user_message = data.get('message')
            if bard_api_token:
                response = Bard(token=bard_api_token).get_answer(user_message)
                if 'content' in response:
                    return jsonify({'response': response['content']}), 200
                else:
                    return jsonify({'error': 'No content in response'}), 500
            else:
                return jsonify({'error': 'Bard API token not provided'}), 500
        else:
            return jsonify({'error': 'Message not provided'}), 400

    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
