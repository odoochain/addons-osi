from odoo import models, fields


class NewApplication(models.Model):
    _name = 'new.application'
    _description = 'create a new loan application in the system'

    applicant = fields.Many2one('new.applicant', 'email', string='Applicant')
    loan_type = fields.Many2one('loan.options', 'name', string='Loan type')

    loan_term = fields.Selection([('2', '2 years'), ('5', '5 years'),
                                  ('10', '10 years')], string='Loan term')

    state = fields.Selection([('Draft', 'Draft'), ('Submitted', 'Submitted'),
                              ('Reviewed', 'Reviewed')], required=True, default='Draft')
