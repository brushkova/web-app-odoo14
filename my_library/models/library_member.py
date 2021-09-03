from odoo import models, fields


class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}

    _description = 'Library Member'

    partner_id = fields.Many2one(comodel_name='res.partner', required=True, ondelete='cascade')
    date_start = fields.Date(string='Member Since')
    date_end = fields.Date(string='Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date(string='Date of birth')
