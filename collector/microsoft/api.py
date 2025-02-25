from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from msgraph.generated.sites.sites_request_builder import SitesRequestBuilder
from msgraph.core import RequestConfiguration
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient

class Microsoft(Resource, enterprise):
    def __init__(self):
        self.base_url = "https://graph.microsoft.com/v1.0"  # Update this URL when API access is granted
        
        # Load credentials from environment variables
        self.api_key = os.getenv('MS_API_KEY')
        self.client_id = os.getenv('MS_CLIENT_ID') 
        self.client_secret = os.getenv('MS_CLIENT_SECRET')
        self.tenant_id = os.getenv('MS_TENANT_ID')
        self.enterprise = enterprise
        
        # if not all([self.api_key, self.client_id, self.client_secret, self.tenant_id]):
        #     raise ValueError("Missing required Microsoft API credentials")
            
        # Set up auth headers
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        # Initialize the Graph client
        credential = ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.graph_client = GraphServiceClient(credential)

        # Set up query parameters for site search
        param = SitesRequestBuilder.SitesRequestBuilderGetQueryParameters(
            search = enterprise
        )

        # Configure the request
        configuration = RequestConfiguration(
            query_parameters = param
        )
    
    async def get(self, enterprise):
        try:
            # Need create a logic for get site ID
            # Execute the search query
            result = await graph_client.sites.by_site_id('site-id').pages.graph_site_page.get()

            return jsonify({
                "status": "Success",
                "message": "Sites retrieved successfully",
                "data": result.value
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


    # # Async method to get pages with canvas layout for a specific site
    # async def get_pages(self, site_id):
    #     try:
    #         # Get pages from Microsoft Graph API with canvas layout expanded
    #         # Uses the site_id parameter to identify the specific site
    #         # The expand parameter includes the canvas layout in the response
    #         result = await self.graph_client.sites.by_site_id(site_id).pages.graph_site_page.get(
    #             expand=['canvasLayout']
    #         )

    #         # Return success response with retrieved pages data
    #         return jsonify({
    #             "status": "Success",
    #             "message": "Pages retrieved successfully", 
    #             "data": result.value
    #         }), 200

    #     except Exception as e:
    #         # Return error response if any exception occurs
    #         return jsonify({
    #             "status": "Error",
    #             "message": str(e)
    #         }), 500

    # # Async method to create a new page in the root site
    # async def create_page(self, title, description=None):
    #     try:
    #         # Prepare the request body for creating a new page
    #         # Required fields: name, title, and pageLayout
    #         page = {
    #             "name": title,
    #             "title": title,
    #             "pageLayout": "Article",
    #         }
            
    #         # Add description to the page if provided
    #         if description:
    #             page["description"] = description

    #         # Send POST request to create new page in the root site
    #         # Uses the Microsoft Graph client to handle the request
    #         result = await self.graph_client.sites.by_site_id('root').pages.post(
    #             body=page
    #         )

    #         # Return success response with the created page data
    #         return jsonify({
    #             "status": "Success",
    #             "message": "Page created successfully",
    #             "data": result
    #         }), 201

    #     except Exception as e:
    #         # Return error response if any exception occurs
    #         return jsonify({
    #             "status": "Error", 
    #             "message": str(e)
    #         }), 500

