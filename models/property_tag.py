from odoo import models, fields

class PropertyTag(models.Model):
  _name = 'real.estate.property.tag'
  _description = 'Real Estate Property tag'
  _order = 'name'

  name = fields.Char(required=True)
  color = fields.Integer()

  _sql_constraints = [
    ('check_unique_name', 'UNIQUE(name)', 'The name must be unique.')
  ]