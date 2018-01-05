# -*- coding: utf-8 -*-
from openerp import models, fields


class CustomerCode(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'uniqueid'

    uniqueid = fields.Char(string='Code', help="The Unique Sequence no", readonly=True)

    _defaults = {
        'uniqueid': lambda obj, cr, uid, context: '/',
    }

    def create(self, cr, uid, vals, context=None):
        res = super(CustomerCode, self).create(cr, uid, vals, context=context)
        partner_rec = self.browse(cr, uid, res)
        user_obj = self.pool.get('res.users').browse(cr, uid, 1)
        if vals.get('company_id'):
            company_seq = self.pool.get('res.company').browse(cr, uid, vals.get('company_id'))
        else:
            company_seq = self.pool.get('res.users').browse(cr, uid, uid).company_id
        if partner_rec.customer == True and vals.get('uniqueid', '/') == '/':
            if company_seq.next_code:
                partner_rec.uniqueid = company_seq.next_code
                partner_rec.name = str(partner_rec.name).upper()
                company_seq.write({'next_code': company_seq.next_code + 1})
            else:
                partner_rec.uniqueid = company_seq.supplier_code
                partner_rec.name = str(partner_rec.name).upper()
                company_seq.write({'next_code': company_seq.supplier_code + 1})
        if partner_rec.supplier == True and vals.get('uniqueid', '/') == '/':
            if user_obj.supplier_code < 10:
                partner_rec.uniqueid = '000' + str(user_obj.supplier_code)
                partner_rec.name = str(partner_rec.name).upper()
                user_obj.write({'supplier_code': user_obj.supplier_code + 1})
            elif user_obj.supplier_code < 100:
                partner_rec.uniqueid = '00' + str(user_obj.supplier_code)
                partner_rec.name = str(partner_rec.name).upper()
                user_obj.write({'supplier_code': user_obj.supplier_code + 1})
            elif user_obj.supplier_code < 1000:
                partner_rec.uniqueid = '0' + str(user_obj.supplier_code)
                partner_rec.name = str(partner_rec.name).upper()
                user_obj.sudo().write({'supplier_code': user_obj.supplier_code + 1})
            elif user_obj.supplier_code > 1000:
                partner_rec.uniqueid = user_obj.supplier_code
                partner_rec.name = str(partner_rec.name).upper()
                user_obj.sudo().write({'supplier_code': user_obj.supplier_code + 1})
            else:
                partner_rec.uniqueid = user_obj.supplier_code
                partner_rec.name = str(partner_rec.name).upper()
                user_obj.write({'supplier_code': 2})
        return res


class ResUsers(models.Model):
    _inherit = 'res.users'

    supplier_code = fields.Integer(string='code')
