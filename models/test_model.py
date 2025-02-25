from datetime import datetime, timedelta
from odoo import models, fields, api

class TestModel(models.Model):
    """
    A model representing a test entity, with features such as automatic generation of 
    unique reference codes, state management, and handling of confirmation timestamps.
    """
    
    _name = 'test.model'
    _description = 'Test Model'

    name = fields.Char(string='Name', required=True)
    """
    The name of the test record. This field is mandatory.
    """

    description = fields.Char(string='Description')
    """
    A description of the test record. This field is optional.
    """

    active = fields.Boolean(string='Active', default=True)
    """
    Boolean indicating whether the record is active. Defaults to True.
    """

    reference_code = fields.Char(string='Reference Code', compute='_compute_reference_code', store=True)
    """
    A unique reference code automatically generated for each record, based on the last generated reference code.
    This field is stored in the database.
    """

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], string='State', default='draft')
    """
    The state of the record. Possible states are 'draft', 'confirmed', and 'done'.
    Defaults to 'draft'.
    """

    confirmation_datetime = fields.Datetime(string='Confirmation Datetime')
    """
    The timestamp when the record was confirmed. Only populated when the state is 'confirmed'.
    """

    _sql_constraints = [
        ('reference_code_unique', 'unique (reference_code)', "Tag already exists!")
    ]
    """
    SQL constraint ensuring that the reference code is unique across all records.
    """

    def action_confirm(self):
        """
        Confirms the current record by setting its state to 'confirmed' and recording the 
        current date and time as the confirmation timestamp.
        """
        for record in self:
            record.state = 'confirmed'
            record.confirmation_datetime = fields.Datetime.now()

    def _compute_reference_code(self):
        """
        Computes the reference code for the record. If no reference code is set, 
        it calls the _generate_reference_code method to generate one.
        """
        for record in self:
            if not record.reference_code:
                record.reference_code = self._generate_reference_code()

    def _generate_reference_code(self):
        """
        Generates a unique reference code for the current record based on the last reference code in the database.
        The reference code is incremented by 1 (e.g., TEST-0001, TEST-0002).
        
        Returns:
            string: The newly generated reference code (e.g., 'TEST-0002').
        """
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

    @api.model_create_multi
    def create(self, values):
        """
        Creates new Test Model records with the provided values. If a reference code is not provided, 
        it generates a new reference code. If the state is 'confirmed', it sets the confirmation datetime.
        
        Args:
            values (dict or list): A dictionary or list of dictionaries containing the values for the new record(s).
        
        Returns:
            record(s): The newly created record(s).
        """
        if isinstance(values, list):
            for value in values:
                if 'reference_code' not in value:
                    value['reference_code'] = self._generate_reference_code()

                if value['state'] == 'confirmed':
                    value['confirmation_datetime'] = fields.Datetime.now()
        else:
            if 'reference_code' not in values:
                values['reference_code'] = self._generate_reference_code()

            if values['state'] == 'confirmed':
                values['confirmation_datetime'] = fields.Datetime.now()

        return super(TestModel, self).create(values)

    @api.model
    def update_state_to_done(self):
        """
        Updates the state of all records with the state 'confirmed' and a confirmation 
        timestamp older than 30 minutes to 'done'.
        """
        time_threshold = datetime.now() - timedelta(minutes=30)

        confirmed_records = self.search([
            ('state', '=', 'confirmed'),
            ('confirmation_datetime', '<', time_threshold)
        ])

        for record in confirmed_records:
            record.state = 'done'

    @api.model
    def reset_reference_codes(self):
        """
        Resets the reference codes for all records in the database, reassigning them 
        sequentially starting from 'TEST-0001'.
        """
        records = self.search([])

        for index, record in enumerate(records, start=1):
            record.reference_code = f"TEST-{index:04d}"
