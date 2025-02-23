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


    def _compute_reference_code(self):
        for record in self:
            if not record.reference_code:
                record.reference_code = self._generate_reference_code()

    def _generate_reference_code(self):
        last_record = self.search([], order='reference_code desc', limit=1)
        
        if last_record and last_record.reference_code:
            reference_code_number = last_record.reference_code.split('-')[-1]
            
            try:
                last_number = int(reference_code_number)
            except ValueError:
                last_number = 0
        else:
            last_number = 0


        new_number = last_number + 1
        return f"TEST-{new_number:04d}"

    @api.model
    def create(self, values):
        if 'reference_code' not in values:
            values['reference_code'] = self._generate_reference_code()

        return super(TestModel, self).create(values)
