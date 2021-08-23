from odoo import models, fields


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'

    name = fields.Char(string='Title', required=True)
    short_name = fields.Char('Short Title', required=True)
    date_release = fields.Date(string='Release Date')
    author_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='book_partner',
        column1='book_id',
        column2='partner_id',
        string='Authors'
    )
