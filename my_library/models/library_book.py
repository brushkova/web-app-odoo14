from datetime import timedelta

from odoo import _
from odoo import api, models, fields
from odoo.exceptions import ValidationError

from odoo.addons import decimal_precision as dp
from . import const


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    _order = 'date_release desc, name'
    _rec_name = 'short_name'

    name = fields.Char(string='Title', required=True)
    short_name = fields.Char(string='Short Title', required=True)
    notes = fields.Text(string='Internal Notes')
    state = fields.Selection(selection=const.STATE_LIST, default=const.STATE_DRAFT, string='State')
    description = fields.Html(string='Description')
    cover = fields.Binary(string='Book Cover')
    out_of_print = fields.Boolean(string='Out of Print?')
    date_release = fields.Date(string='Release Date')
    date_update = fields.Datetime(string='Last Update', copy=False)
    pages = fields.Integer(
        string='Number of pages',
        groups='base.group_user',
        states={const.STATE_LOST: [('readonly', True)]},
        help='Total book page count',
        company_dependent=False
    )
    reader_rating = fields.Float(string='Reader Average Rating', digits=(14, 4))
    cost_price = fields.Float(string='Book Cost', digits=dp.get_precision('Book Price'))
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    retail_price = fields.Monetary(string='Retail Price', currency_field='currency_id')
    publisher_id = fields.Many2one(
        comodel_name='res.partner',
        string='Publisher',
        ondelete='set null'
    )
    publisher_city = fields.Char(string='Publisher City', related='publisher_id.city', readonly=True)
    category_id = fields.Many2one(comodel_name='library.book.category')
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_days',
        inverse='_inverse_age',
        search='_search_age',
        store=False,  # optional
        compute_sudo=True  # optional
    )
    ref_doc_id = fields.Reference(selection='_referencable_models', string='Reference Document')
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'Book title must be unique.'),
        ('positive_page', 'CHECK(pages>0)', 'No of pages must be positive')
    ]

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s %s" % (record.name, "(%s)" % record.date_release if record.date_release else '')
            result.append((record.id, rec_name))

        return result

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release > fields.Date.today():
                raise ValidationError(_('Release date must be in the past'))

    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self:
            if book.date_release:
                delta = today - book.date_release
                book.age_days = delta.days
            else:
                book.age_days = 0

    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered('date_release'):
            book.write({
                'date_release': today - timedelta(days=book.age_days)
            })

    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        # convert the operator:
        # book with age > value have a date < value_date
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]

    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([])
        return [(x.model, x.name) for x in models]
