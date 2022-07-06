from odoo import api, models, fields
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
  _name = 'real.estate.property.offer'
  _description = 'Real Estate Property Offer'
  _order = 'price desc'

  price = fields.Float()
  status = fields.Selection([
    ('accepted', 'Accepted'),
    ('refused', 'Refused')
  ], copy=False, readonly=True)
  partner_id = fields.Many2one('res.partner', string="Partner")
  property_id = fields.Many2one('real.estate.property', string="Property")
  property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property type", store=True)
  validity = fields.Integer(default=7, string="Validity (days)")
  date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string="Deadline")

  _sql_constraints = [
    ('check_price', 'CHECK(price >= 0)', 'The price must be strictly positive.')
  ]

  def action_accept_offer(self):
    if self.property_id.state == 'sold':
      raise UserError("You already sold this property.")
    if self.property_id.state == 'canceled':
      raise UserError("This property was canceled.")

    self.property_id.buyer = self.partner_id
    self.property_id.selling_price = self.price
    self.property_id.state = 'offer_accepted'
    self.status = 'accepted'

    return True

  def action_refuse_offer(self):
    if self.property_id.state == 'sold':
      raise UserError("You already sold this property.")
    if self.property_id.state == 'canceled':
      raise UserError("This property was canceled.")

    self.status = 'refused'

    return True

  @api.depends('date_deadline', 'validity')
  def _compute_date_deadline(self):
    for record in self:
      record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

  @api.depends('date_deadline', 'validity')
  def _inverse_date_deadline(self):
    for record in self:
      record.validity = (record.date_deadline - fields.Date.today()).days

  @api.model
  def create(self, vals):
    property_object = self.env['real.estate.property'].browse(vals['property_id'])
    max_offer_price = property_object['best_price']

    if vals['price'] <= max_offer_price:
      raise UserError('The offer must be higher than ' + str(max_offer_price))

    property_object['state'] = 'offer_received'

    return super().create(vals)
