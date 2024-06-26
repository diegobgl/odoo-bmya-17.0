from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_country(self):
        try:
            return self.env.user.company_id.country_id or False
        except:
            return False

    country_id = fields.Many2one("res.country", default=_default_country)
    state_id = fields.Many2one("res.country.state", compute='_change_state_province', store=True, readonly=False,
        string='Ubication', domain="[('country_id', '=', country_id), ('type', '=', 'normal')]")
    real_city = fields.Char(compute='_change_real_city_province', string='City.')
    city = fields.Char(compute='_change_city_province', string='City', store=True, readonly=False)
    country_code = fields.Char(related='country_id.code', string='Country ID')
    company_country_code = fields.Char(compute='_get_company_country_code', string='Country-ID')

    @api.depends('country_id', 'company_id')
    def _get_company_country_code(self):
        for record in self:
            if record.company_id.country_id.code == 'CL' or self.env.company.country_id.code == 'CL':
                record.company_country_code = 'CL'
            else:
                record.company_country_code = ''

    @api.depends('country_id', 'state_id', 'city_id')
    def _change_real_city_province(self):
        for record in self:
            if record.country_id != record.env.ref('base.cl'):
                record.real_city = False
            if record.state_id == record.env.ref('base.state_cl_13'):
                record.real_city = 'Santiago'
            else:
                record.real_city = record.city_id.name

    @api.depends('country_id', 'state_id', 'city_id')
    def _change_city_province(self):
        for record in self:
            if record.country_id != record.env.ref('base.cl'):
                return
            record.city = record.city_id.name

    @api.depends('country_id', 'city_id')
    def _change_state_province(self):
        for record in self:
            if record.country_id != record.env.ref('base.cl'):
                return
            record.state_id = record.city_id.state_id
