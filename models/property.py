from odoo import models, fields

class Property(models.Model):
  _name = 'real.estate.property'
  _description = 'Real Estate Property'

  name = fields.Char()
  description = fields.Text()
  postcode = fields.Char()
  date_availability = fields.Date()
  expected_price = fields.Float()
  selling_price = fields.Float()
  bedrooms = fields.Integer()
  living_area = fields.Integer()
  facades = fields.Integer()
  garage = fields.Boolean()
  garden = fields.Boolean()
  garden_area = fields.Integer()
  garden_orientation = fields.Selection([
    ('north', 'North'),
    ('south', 'South'),
    ('east', 'East'),
    ('west', 'West')
  ])