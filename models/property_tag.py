from odoo import models, fields

class PropertyTag(models.Model):
  _name = 'real.estate.property.tag'
  _description = 'Real Estate Property tag'

  name = fields.Char(required=True)

  _sql_constraints = [
    ('check_unique_name', 'UNIQUE(name)', 'The name must be unique.')
  ]