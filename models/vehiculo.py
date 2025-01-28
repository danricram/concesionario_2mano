from odoo import models, fields

class Vehiculo(models.Model):
    _name = "concesionario.vehiculo"
    _description = "Vehículo"

    nombre = fields.Char(string="Nombre", required=True)
    marca = fields.Char(string="Marca", required=True)
    modelo = fields.Char(string="Modelo", required=True)
    año = fields.Integer(string="Año")
    kilometraje = fields.Float(string="Kilometraje")
    precio = fields.Float(string="Precio", required=True)  # Make sure this field is defined correctly
    estado = fields.Selection([
        ("disponible", "Disponible"),
        ("reservado", "Reservado"),
        ("vendido", "Vendido")
    ], string="Estado", default="disponible")
    descripcion = fields.Text(string="Descripción")
    imagen = fields.Binary(string="Imagen")