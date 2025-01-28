from odoo import models, fields

class Venta(models.Model):
    _name = "concesionario.venta"
    _description = "Venta"

    cliente_id = fields.Many2one("concesionario.cliente", string="Cliente", required=True)
    vehiculo_id = fields.Many2one("concesionario.vehiculo", string="Vehículo", required=True)
    fecha_venta = fields.Date(string="Fecha de Venta", default=fields.Date.today)
    precio = fields.Float(string="Precio de Venta", related="vehiculo_id.precio")