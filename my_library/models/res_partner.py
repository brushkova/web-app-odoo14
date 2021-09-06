from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'

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
    count_books = fields.Integer(string='Number of Authored Books', compute='_compute_count_books')

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)
