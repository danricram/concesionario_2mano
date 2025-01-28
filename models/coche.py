from odoo import models, fields

class Coche(models.Model):
    _name = "concesionario.coche"
    _description = "Vehículo"

    nombre = fields.Char(string="Nombre", required=True)
    marca = fields.Char(string="Marca", required=True)
    modelo = fields.Char(string="Modelo", required=True)
    anio = fields.Integer(string="Año")
    km = fields.Float(string="Kilometraje")
    precio = fields.Float(string="Precio", required=True)
    stado = fields.Selection([
        ("available", "Disponible"),
        ("reserved", "Reservado"),
        ("sold", "Vendido")
    ], string="Estado", default="available")
    descripcion = fields.Text(string="Descripción")
    imagen = fields.Binary(string="Imagen")