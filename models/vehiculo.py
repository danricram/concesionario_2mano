from odoo import models, fields

class Vehiculo(models.Model):
    _name = "concesionario.vehiculo"
    _description = "Vehículo"

    cantidad = fields.Integer(string="Cantidad")
    marca = fields.Char(string="Marca", required=True)
    modelo = fields.Char(string="Modelo", required=True)
    color = fields.Char(string="Color")
    año = fields.Integer(string="Año")
    kilometraje = fields.Float(string="Kilometraje")
    potencia_cv = fields.Float(string="Potencia (CV)")
    precio = fields.Float(string="Precio", required=True)
    estado = fields.Selection([
        ("disponible", "Disponible"),
        ("reservado", "Reservado"),
        ("vendido", "Vendido")
    ], string="Estado", default="disponible")
    tipo_combustible = fields.Selection([
        ("gasolina", "Gasolina"),
        ("diesel", "Diésel"),
        ("hibrido", "Híbrido"),
        ("electrico", "Eléctrico")
    ], string="Tipo de Combustible")
    transmision = fields.Selection([
        ("manual", "Manual"),
        ("automatica", "Automática")
    ], string="Transmisión")
    descripcion = fields.Text(string="Descripción")
    imagen = fields.Binary(string="Imagen")

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.marca} {record.modelo}"
            result.append((record.id, name))
        return result