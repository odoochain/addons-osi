from odoo import models, fields


class NewApplicant(models.Model):
    _name = 'new.applicant'
    _description = 'create a new applicant in the system'

    fname = fields.Char('First name', required=True)
    lname = fields.Char('Last name', required=True)
    dob = fields.Date('Date of Birth')
    phone = fields.Char('Phone number', required=True)
    email = fields.Char('Email', required=True)
    street_address = fields.Text('Street Address', required=True)
    street_address2 = fields.Text('Street Address Line 2 (Optional)', required=False)
    state = fields.Selection([
        ('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'),
        ('DC', 'DC'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'),
        ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'),
        ('MS', 'MS'), ('MO', 'MO'), ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'),
        ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'),
        ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'),
        ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY')
    ], string="State")

    zip = fields.Integer('Zip code')
    ssn = fields.Integer('SSN #')
    employment_status = fields.Selection([('Employed', 'Employed'), ('Unemployed', 'Unemployed'),
                                          ('Fixed Income (SSI, Retirement Income)',
                                           'Fixed Income (SSI, Retirement Income)')
                                          ], string='Employment Status')
    monthly_income = fields.Integer('Monthly income')
    employer = fields.Char('Employer')
    employer_number = fields.Char('Employer contact number')
