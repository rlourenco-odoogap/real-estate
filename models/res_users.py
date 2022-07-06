from odoo import models, fields

class ResUsers(models.Model):
  _inherit = 'res.users'

  property_ids = fields.One2many(
    'real.estate.property', 
    'salesperson', 
    string="Properties", 
    domain="['|', ('state', '=', 'new'), ('state', '=', 'offer_received')]"
  )