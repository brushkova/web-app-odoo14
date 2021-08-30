import dot_parser
from odoo.addons import decimal_precision as dp
from odoo import models, fields


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'

    name = fields.Char(string='Title', required=True)
    short_name = fields.Char(string='Short Title', required=True)
    notes = fields.Text(string='Internal Notes')
    state = fields.Selection(
        selection=[('draft', 'Not Available'),
                   ('available', 'Available'),
                   ('lost', 'Lost')
                   ],
        string='State'
    )
    description = fields.Html(string='Description')
    cover = fields.Binary(string='Book Cover')
    out_of_print = fields.Boolean(string='Out of Print?')
    date_release = fields.Date(string='Release Date')
    date_update = fields.Datetime(string='Last Update', copy=False)
    pages = fields.Integer(
        string='Number of pages',
        groups='base.group_user',
        states={'lost': [('readonly', True)]},
        help='Total book page count', company_dependent=False
    )
    reader_rating = fields.Float(string='Reader Average Rating', digits=(14, 4))
    author_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='book_partner',
        column1='book_id',
        column2='partner_id',
        string='Authors'
    )
    cost_price = fields.Float(string='Book Cost', digits=dp.get_precision('Book Price'))
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    retail_price = fields.Monetary(string='Retail Price', currency_field='currency_id')
    publisher_id = fields.Many2one(
        comodel_name='res.partner',
        string='Publisher',
        ondelete='set null',
        context={},
        domain=[]
    )
    category_id = fields.Many2one(comodel_name='library.book.category')

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s %s" % (record.name, "(%s)" % record.date_release if record.date_release else '')
            result.append((record.id, rec_name))
        return result
