from odoo import api, models, fields
from odoo.exceptions import UserError

class Property(models.Model):
  _name = 'real.estate.property'
  _description = 'Real Estate Property'
  _order = 'id desc'

  name = fields.Char(required=True, string="Title")
  description = fields.Text()
  postcode = fields.Char()
  date_availability = fields.Date(
    copy=False, 
    string="Available From", 
    default=lambda self: fields.Date.add(fields.Date.today(), months=3)
  )
  expected_price = fields.Float(required=True)
  selling_price = fields.Float(readonly=True, copy=False)
  bedrooms = fields.Integer(default=2)
  living_area = fields.Integer(string="Living Area (sqm)")
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
  active = fields.Boolean(default=True)
  state = fields.Selection([
    ('new', 'New'),
    ('offer_received', 'Offer Received'),
    ('offer_accepted', 'Offer Accepted'),
    ('sold', 'Sold'),
    ('canceled', 'Canceled')
  ], required=True, copy=False, default='new', string="Status")
  property_type_id = fields.Many2one('real.estate.property.type', string="Property Type")
  buyer = fields.Many2one('res.partner', copy=False)
  salesperson = fields.Many2one('res.users', default=lambda self: self.env.user, string="Salesman")
  tag_ids = fields.Many2many('real.estate.property.tag', string="Tags")
  offer_ids = fields.One2many('real.estate.property.offer', 'property_id', string="Offers")
  total_area = fields.Integer(compute='_compute_total_area')
  best_price = fields.Float(compute='_compute_best_price', string="Best Offer")

  _sql_constraints = [
    ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
    ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be positive.'),
  ]

  def action_set_property_as_sold(self):
    if self.state == 'canceled':
      raise UserError('Canceled properties cannot be sold.')

    self.state = 'sold'
    return True

  def action_set_property_as_canceled(self):
    if self.state == 'sold':
      raise UserError('Sold properties cannot be canceled.')

    self.state = 'canceled'
    return True

  @api.depends('living_area', 'garden_area')
  def _compute_total_area(self):
    for record in self:
      record.total_area = record.living_area + record.garden_area

  @api.depends('offer_ids')
  def _compute_best_price(self):
    for record in self:
      record.best_price = max(offer.price for offer in record.offer_ids) if len(record.offer_ids) > 0 else 0

  @api.onchange('garden')
  def _onchange_garden(self):
    self.garden_area = 10 if self.garden else 0
    self.garden_orientation = 'north' if self.garden else ''

  @api.constrains('expected_price', 'selling_price')
  def _check_expected_price(self):
    ninety_percent_of_expected_price = self.expected_price * 0.9

    if self.selling_price > 0 and self.selling_price < ninety_percent_of_expected_price:
      raise UserError('The selling price must be at least 90% of the expected price. You must reduce your expected price if you really want to sell.')

  @api.ondelete(at_uninstall=False)
  def _unlink_only_new_or_canceled_properties(self):
    for record in self:
      if record.state not in ('new', 'canceled'):
        raise UserError('Only new and canceled properties can be deleted.')
