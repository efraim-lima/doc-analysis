from flask import Flask, request, jsonify
from flask_restful import Resource, Api

class Microsoft(Resource):
    def __init__(self):
        self.base_url = "https://api.microsoft.com"  # Update this URL when API access is granted
        self.api_key = None
        self.client_id = None
        self.client_secret = None
        self.tenant_id = None
        
        # Load credentials from environment variables
        self.api_key = os.getenv('MS_API_KEY')
        self.client_id = os.getenv('MS_CLIENT_ID') 
        self.client_secret = os.getenv('MS_CLIENT_SECRET')
        self.tenant_id = os.getenv('MS_TENANT_ID')
        
        if not all([self.api_key, self.client_id, self.client_secret, self.tenant_id]):
            raise ValueError("Missing required Microsoft API credentials")
            
        # Set up auth headers
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    def get(self):
        try:
            # Implement document retrieval logic here
            return jsonify({
                "status": "Success",
                "message": "Retrieved successfully",
                "data": []
            }), 200
        except Exception as e:
            return jsonify({
                "status": "Error",
                "message": str(e)
            }), 500
    
    def post(self):
        try:  
            response = requests.get(f"{self.base_url}/pastel/void")
            if not response.ok:
                raise Exception(f"Failed to retrieve data: {response.status_code}")

            data = response.json()
            
            return jsonify({
                "status": "Success", 
                "message": "Teams equipment data retrieved and processed",
                "data": data
            }), 200
        except Exception as e:
            return jsonify({
                "status": "Error",
                "message": str(e)
            }), 500