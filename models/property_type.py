from odoo import models, fields

class PropertyType(models.Model):
  _name = 'real.estate.property.type'
  _description = 'Real Estate Property Type'
  _order = 'name'

  name = fields.Char(required=True)
  property_ids = fields.One2many('real.estate.property', 'property_type_id', string="Properties")

  _sql_constraints = [
    ('check_unique_name', 'UNIQUE(name)', 'The name must be unique.')
  ]