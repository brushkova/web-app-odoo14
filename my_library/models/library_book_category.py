from odoo import _
from odoo import api, models, fields
from odoo.exceptions import ValidationError


class BookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'
    _parent_store = True
    _parent_name = "parent_id"  # optional if field is 'parent_id'

    name = fields.Char(string='Category')
    parent_id = fields.Many2one(
        comodel_name='library.book.category',
        string='Parent Category',
        ondelete='restrict',
        index=True
    )
    child_ids = fields.One2many(
        comodel_name='library.book.category',
        inverse_name='parent_id',
        string='Child Categories'
    )
    parent_path = fields.Char(index=True)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise ValidationError(_('Error! You cannot create recursive categories.'))
