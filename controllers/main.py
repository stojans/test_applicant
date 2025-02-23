from odoo import http
from odoo.http import request, Response
import json


class TestModelController(http.Controller):
    @http.route('/api/test-model', auth='public', methods=['GET'], csrf=False)
    def get_test_model(self):


        records = request.env['test.model'].search([])

        result = []
        for record in records:
            result.append({
                'id': record.id,
                'name': record.name,
                'description': record.description,
                'state': record.state,
                'confirmation_datetime': record.confirmation_datetime.strftime('%Y-%m-%dT%H:%M:%S') if record.confirmation_datetime else None,
            })


        headers = {'Content-Type': 'application/json'}

        return Response(json.dumps(result),headers=headers)


    @http.route('/api/test-model', type='json', auth='user', methods=['POST'], csrf=False)
    def create_test_model(self, **post):
        post = request.httprequest.get_json()
        name = post.get('name', None)
        description = post.get('description', None)
        state = post.get('state', 'draft')

        if not name:
            return {"error": "Name is required."}

        new_record = request.env['test.model'].create({
            'name': name,
            'state': state,
            'description': description,

        })

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