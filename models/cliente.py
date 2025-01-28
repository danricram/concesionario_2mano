from odoo import models, fields

class Cliente(models.Model):
    _name = "concesionario.cliente"
    _description = "Cliente"

    nombre = fields.Char(string="Nombre", required=True)
    correo_electronico = fields.Char(string="Correo Electrónico")
    telefono = fields.Char(string="Teléfono")
    vehiculo_preferido = fields.Many2one("concesionario.vehiculo", string="Vehículo Preferido")