from odoo import http
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)

class TestModelController(http.Controller):
    """
    Controller for managing 'test.model' records through an API. 
    Supports GET and POST requests for fetching and creating records.
    """
    
    @http.route('/api/test-model', auth='public', methods=['GET'], csrf=False)
    def get_test_model(self):
        """
        Handles GET requests to fetch all 'test.model' records.
        Returns a list of records with details such as 'id', 'name', 'description', 
        'state', and 'confirmation_datetime' (if available) in JSON format.

        Returns:
            Response: A JSON response containing the list of 'test.model' records.
        """
        _logger.info("GET request received")

        # Fetch all records from the 'test.model' model
        records = request.env['test.model'].search([])

        # Prepare the response data
        result = []
        for record in records:
            result.append({
                'id': record.id,
                'name': record.name,
                'description': record.description,
                'state': record.state,
                'confirmation_datetime': record.confirmation_datetime.strftime('%Y-%m-%dT%H:%M:%S') if record.confirmation_datetime else None,
            })

        # Set response headers and return the result as JSON
        headers = {'Content-Type': 'application/json'}
        return Response(json.dumps(result), headers=headers)

    @http.route('/api/test-model', type='json', auth='user', methods=['POST'], csrf=False)
    def create_test_model(self, **post):
        """
        Handles POST requests to create a new 'test.model' record. The request body
        should contain 'name', 'description', and optionally 'state'. The 'state' 
        defaults to 'draft' if not provided.

        Args:
            post (dict): A dictionary containing the POST data with fields 'name', 'description', and 'state'.

        Returns:
            Response: A JSON response indicating the success of the operation and the details of the created record.
        """
        # Parse the JSON request data
        post = request.httprequest.get_json()
        name = post.get('name', None)
        description = post.get('description', None)
        state = post.get('state', 'draft')

        # Validate that 'name' is provided
        if not name:
            return {"error": "Name is required."}

        # Create a new 'test.model' record
        new_record = request.env['test.model'].create({
            'name': name,
            'state': state,
            'description': description,
        })

        # Prepare and return a success response with the created record details
        headers = {'Content-Type': 'application/json'}
        return Response(
            json.dumps({
                'status': 'success',
                'id': new_record.id,
                'name': new_record.name,
                'state': new_record.state,
            }),
            headers=headers,
        )
