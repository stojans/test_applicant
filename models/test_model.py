from odoo import models, fields, api

class TestModel(models.Model):
    _name='test.model'
    _description='Test Model'

    name=fields.Char(string='Name', required=True)
    description=fields.Char(string='Description')
    active=fields.Boolean(string='Active', default=True)
    reference_code=fields.Char(string='Reference Code', compute='_compute_reference_code', store=True, unique=True)
    state=fields.Selection([
        ('draft','Draft'),
        ('confirmed','Confirmed'),
        ('done','Done'),
    ], string='State', default='draft')

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'