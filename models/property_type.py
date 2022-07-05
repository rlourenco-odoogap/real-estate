from odoo import models, fields

class PropertyType(models.Model):
  _name = 'real.estate.property.type'
  _description = 'Real Estate Property Type'

  name = fields.Char(required=True)

  _sql_constraints = [
    ('check_unique_name', 'UNIQUE(name)', 'The name must be unique.')
  ]