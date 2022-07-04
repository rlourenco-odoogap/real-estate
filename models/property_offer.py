from odoo import models, fields

class PropertyOffer(models.Model):
  _name = 'real.estate.property.offer'
  _description = 'Real Estate Property Offer'

  price = fields.Float()
  status = fields.Selection([
    ('accepted', 'Accepted'),
    ('refused', 'Refused')
  ], copy=False)
  partner_id = fields.Many2one('res.partner', string="Partner")
  property_id = fields.Many2one('real.estate.property', string="Property")