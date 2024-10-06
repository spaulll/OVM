from flask import Flask, app, request, render_template, jsonify
from flask_cors import CORS
from index import *
from dotenv import load_dotenv
import os



app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/kyc', methods=['POST'])
def get_kyc_data():
    try:
        # Extract form data
        name = request.form.get('name')
        aadhar_number = request.form.get('documentNumber')
        area = request.form.get('area')
        voter_number = request.form.get('phoneNumber')
        wallet_address = request.form.get('walletAddress')
        doc_image = request.files.get('documentImage') 
        human_image = request.files.get('faceImage')
        D_O_B = request.form.get('DOB')
        

        # Validate input fields
        if not name or not aadhar_number or not area or not voter_number or not wallet_address or not D_O_B:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Validate images
        if not doc_image:
            return jsonify({"error": "Document image is required."}), 400
        if not human_image:
            return jsonify({"error": "Human image is required."}), 400
        
        doc_image_data = doc_image.read()  # Read the file content
        human_image_data = human_image.read()
        # Issue SBT and get hash value
        tx_hash = issue_sbt(wallet_address, area)
        print(f"Transaction hash: {tx_hash}")
        
        if not tx_hash:
            return jsonify({"error": "Some error occurred while issuing SBT. Please try again later."}), 500

        # Insert the data into the database
        result = insert_data(name, aadhar_number, area, voter_number, wallet_address, doc_image_data, human_image_data, D_O_B)
        if result == "Duplicate":
            return jsonify({"error": "A KYC record already exists for this wallet address."}), 400
        elif result == False:
            return jsonify({"error": "An error occurred while inserting data into the database."}), 500

        # Handle the transaction hash logic
        if tx_hash == "Minted":
            return jsonify({"error": "SBT already minted by this address."}), 400
        elif tx_hash:
            return jsonify({"status": "success","tx_hash": str(tx_hash), "message": "Your KYC is done, you can now vote."}), 200
        else:
            return jsonify({"error": "Some error occurred while issuing SBT. Please try again later."}), 500

    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid value: {str(e)}"}), 400
    except TypeError as e:
        return jsonify({"error": f"Type error: {str(e)}"}), 400
    except Exception as e:
        print("An unexpected error occurred:", e)
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.route('/api/get_abi/<contract>', methods=['GET'])
def get_abi(contract):
    if contract == "VoterID":
        data = get_abi_voterID()
    elif contract == "VotingSystem":
        data = get_abi_votingSystem()
    else:
        data = {"error": "Contract not found"}
    return data

# API endpoint to get candidate details based on the address
@app.route('/api/get-candidates', methods=['POST'])
def get_candidates():
    try:
        # Get the JSON data from the request
        data = request.json
        print("Received address:", data.get('address'))  

        # Extract the address from the JSON data
        address = data.get('address').lower()
        
        if not address:
            return jsonify({'status': 'error', 'message': 'Address is required'}), 400
        # Fetch the candidate details using the area
        candidates = get_candidates_by_area(address)
        print("Candidates:", candidates)  
        # Check if the area was found
        if not candidates:
            return jsonify({'status': 'error', 'message': 'Area not found for the given address'}), 404



        # Return the candidate details
        return jsonify({'status': 'success', 'candidates': candidates}), 200

    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/get-users', methods=['POST'])
def get_users():
    try:
        # Get the JSON data from the request
        data = request.json
        print("Received address:", data.get('address'))  

        # Extract the address from the JSON data
        address = data.get('address').lower()
        
        if not address:
            return jsonify({'status': 'error', 'message': 'Address is required'}), 400
        # Fetch the user details using the area
        users = get_users_by_area(address)
        print("Users:", users)  
        # Check if the area was found
        if not users:
            return jsonify({'status': 'error', 'message': 'Area not found for the given address'}), 404



        # Return the user details
        return jsonify({'status': 'success', 'users': users}), 200

    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

@app.route('/api/execute-meta-tx', methods=['POST'])
def execute_meta_transaction():
    try:
        data = request.json
        
        # Execute the meta transaction and capture the result
        result = execute_meta_tx(data)
    
        # Check if the transaction was successful
        if result.get('success'):
            # On success, return the transaction hash
            return jsonify({'status': 'success', 'txHash': result.get('tx_hash')}), 200
        else:
            # On failure, return the error message
            return jsonify({'status': 'error', 'message': result.get('error')}), 400
    
    except Exception as e:
        # Catch any other exceptions and return an internal server error
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
    



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)