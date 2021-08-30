from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many(
        comodel_name='library.book',
        inverse_name='publisher_id',
        string='Published Books'
    )
    authored_book_ids = fields.Many2many(
        comodel_name='library.book',
        relation='authored_book',
        column1='author_id',
        column2='book_id',
        string='Authored Book'
    )
