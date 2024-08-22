from flask import Flask, jsonify, request
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define paths for the JSON files
nodes_file_path = os.path.join(os.path.dirname(__file__), 'data', 'nodes.json')

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # Load nodes data
        with open(nodes_file_path, 'r') as nodes_file:
            nodes_data = json.load(nodes_file)
        
        return jsonify(nodes_data)
    
    except FileNotFoundError as e:
        return jsonify({"error": f"File not found: {e.filename}"}), 404
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Error decoding JSON: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/data', methods=['POST'])
def save_data():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Split the data into nodes
        nodes_data = data.get("nodes", [])

        # Write nodes data to file
        with open(nodes_file_path, 'w') as nodes_file:
            json.dump(nodes_data, nodes_file, indent=4)

        return jsonify({"message": "Data saved successfully"}), 200

    except (json.JSONDecodeError, TypeError) as e:
        return jsonify({"error": f"Invalid JSON data: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
