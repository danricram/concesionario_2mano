from odoo import models, fields

class Cliente(models.Model):
    _name = "concesionario.customer"
    _description = "Cliente"

    nombre = fields.Char(string="Nombre", required=True)
    email = fields.Char(string="Correo Electrónico")
    telefono = fields.Char(string="Teléfono")
    coche_pref = fields.Many2one("concesionario.vehicle", string="Vehículo Preferido")