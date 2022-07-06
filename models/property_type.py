from odoo import models, fields, api

class PropertyType(models.Model):
  _name = 'real.estate.property.type'
  _description = 'Real Estate Property Type'
  _order = 'name'

  name = fields.Char(required=True)
  property_ids = fields.One2many('real.estate.property', 'property_type_id', string="Properties")
  sequence = fields.Integer()
  offer_ids = fields.One2many('real.estate.property.offer', 'property_type_id', 'Offers')
  offer_count = fields.Integer(compute='_compute_offer_count')

  _sql_constraints = [
    ('check_unique_name', 'UNIQUE(name)', 'The name must be unique.')
  ]

  @api.depends('offer_count', 'offer_ids')
  def _compute_offer_count(self):
    for record in self:
      record.offer_count = len(record.offer_ids)