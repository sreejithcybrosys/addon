# -*- coding: utf-8 -*-
from openerp import models, fields


class CompanySequence(models.Model):
    _inherit = 'res.company'

    supplier_code = fields.Integer('Customer code start from', required=True)
    supp_code = fields.Integer('Supplier code')
    next_code = fields.Integer('Next code')
