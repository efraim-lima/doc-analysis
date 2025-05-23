from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
import os

class Zeev(Resource):
    def __init__(self):
        self.base_url = "https://api.zeev.com" #Este ponto preciso alterar assim que tievr acesso à API
        self.zeev_key = os.getenv('ZEEV_KEY')
    
    def get(self):
        try:
            # Make API call to Zeev pastel/void endpoint
            response = requests.get(
                f'{self.base_url}/2/assignments/user/{username}', 
                headers={self.zeev_key}
            )
            
            if not response.ok:
                raise Exception(f"Failed to retrieve data: {response.status_code}")
            # Implement document retrieval logic here
            
            data = response.json()
            
            return jsonify({
                "status": "Success",
                "message": "Retrieve successful",
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

            # Implement document collection logic here
            return jsonify({
                "status": "Success",
                "message": "Collection successful",
                "data": data
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500 
