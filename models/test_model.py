from datetime import datetime, timedelta
from odoo import models, fields, api

class TestModel(models.Model):
    _name='test.model'
    _description='Test Model'

    name=fields.Char(string='Name', required=True)
    description=fields.Char(string='Description')
    active=fields.Boolean(string='Active', default=True)
    reference_code=fields.Char(string='Reference Code', compute='_compute_reference_code', store=True)
    state=fields.Selection([
        ('draft','Draft'),
        ('confirmed','Confirmed'),
        ('done','Done'),
    ], string='State', default='draft')
    confirmation_datetime=fields.Datetime(string='Confirmation Datetime')

    _sql_constraints = [

            ('reference_code_unique', 'unique (reference_code)', "Tag already exists!"),

        ]


    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
            record.confirmation_datetime = fields.Datetime.now()


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

        if values['state'] == 'confirmed':
            values['confirmation_datetime'] = fields.Datetime.now()

        return super(TestModel, self).create(values)
    


    @api.model
    def update_state_to_done(self):
        time_threshold = datetime.now() - timedelta(minutes=30)

        confirmed_records = self.search([
            ('state', '=', 'confirmed'),
            ('confirmation_datetime', '>=', time_threshold)
        ])

        for record in confirmed_records:
            record.state = 'done'

    @api.model
    def reset_reference_codes(self):
        records = self.search([])

        for index, record in enumerate(records, start=1):
            record.reference_code = f"TEST-{index:04d}"
