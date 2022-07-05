from odoo import api, models, fields

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
  validity = fields.Integer(default=7, string="Validity (days)")
  date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string="Deadline")

  @api.depends('date_deadline', 'validity')
  def _compute_date_deadline(self):
    for record in self:
      record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

  @api.depends('date_deadline', 'validity')
  def _inverse_date_deadline(self):
    for record in self:
      record.validity = (record.date_deadline - fields.Date.today()).days
