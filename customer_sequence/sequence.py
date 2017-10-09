# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp import exceptions
from openerp.tools import amount_to_text_en


class CustomerCode(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'uniqueid'

    uniqueid = fields.Char(string='Code', help="The Unique Sequence no", readonly=True)

    _defaults = {
        'uniqueid': lambda obj, cr, uid, context: '/',
    }

    @api.one
    def custom_code(self):
        company_seq = self.env['res.company'].browse(self.company_id.id)
        sttr = ""
        for i in self.name:
            if i == ']':
                sttr = ""
                continue
            sttr += i
        if self.company_id.next_code:
            self.uniqueid = self.company_id.next_code
            self.name = '[' + str(self.company_id.next_code) + ']' + sttr
            company_seq.write({'next_code': self.company_id.next_code + 1})
        else:
            self.uniqueid = company_seq.supplier_code
            self.name = '[' + str(company_seq.supplier_code) + ']' + str(self.name)
            company_seq.write({'next_code': company_seq.supplier_code + 1})

    def create(self, cr, uid, vals, context=None):
        res = super(CustomerCode, self).create(cr, uid, vals, context=context)
        partner_rec = self.browse(cr, uid, res)
        company_name = self.pool.get('res.company').browse(cr, uid, vals.get('company_id')).name
        if vals.get('company_id'):
            company_seq = self.pool.get('res.company').browse(cr, uid, vals.get('company_id'))
        else:
            company_seq = self.pool.get('res.users').browse(cr, uid, uid).company_id
        count = 0
        obj_partner = self.pool.get('res.partner').search(cr, uid, [('customer', '=', True)])
        for partner_id in obj_partner:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id)
            partner_name = partner.name.split(']')
            if len(partner_name) == 2:
                if vals['name'].strip().lower() == partner_name[1].strip().lower():
                    count += 1
            elif len(partner_name) == 1:
                if vals['name'].strip().lower() == partner_name[0].strip().lower():
                    count += 1
        if count == 2:
            raise exceptions.Warning(_("Warning"), _(
                "There is already a customer with same name"))
        if partner_rec.customer == True and vals.get('uniqueid', '/') == '/':
            if company_seq.next_code:
                partner_rec.uniqueid = company_seq.next_code
                partner_rec.name = '[' + str(company_seq.next_code) + ']' + str(partner_rec.name)
                company_seq.write({'next_code': company_seq.next_code + 1})
            else:
                partner_rec.uniqueid = company_seq.supplier_code
                partner_rec.name = '[' + str(company_seq.supplier_code) + ']' + str(partner_rec.name)
                company_seq.write({'next_code': company_seq.supplier_code + 1})
        if partner_rec.supplier == True and vals.get('uniqueid', '/') == '/':
            if company_seq.supp_code < 10:
                partner_rec.uniqueid = '000' + str(company_seq.supp_code)
                partner_rec.name = '[' + '000' + str(company_seq.supp_code) + ']' + str(partner_rec.name)
                company_seq.write({'supp_code': company_seq.supp_code + 1})
            elif company_seq.supp_code < 100:
                partner_rec.uniqueid = '00' + str(company_seq.supp_code)
                partner_rec.name = '[' + '00' + str(company_seq.supp_code) + ']' + str(partner_rec.name)
                company_seq.write({'supp_code': company_seq.supp_code + 1})
            elif company_seq.supp_code < 1000:
                partner_rec.uniqueid = '0' + str(company_seq.supp_code)
                partner_rec.name = '[' + '0' + str(company_seq.supp_code) + ']' + str(partner_rec.name)
                company_seq.write({'supp_code': company_seq.supp_code + 1})
            elif company_seq.supp_code > 1000:
                partner_rec.uniqueid = company_seq.supp_code
                partner_rec.name = '[' + str(company_seq.supp_code) + ']' + str(partner_rec.name)
                company_seq.write({'supp_code': company_seq.supp_code + 1})
            else:
                partner_rec.uniqueid = company_seq.supp_code
                partner_rec.name = '[' + '0001' + ']' + str(partner_rec.name)
                company_seq.write({'supp_code': 2})
        return res
