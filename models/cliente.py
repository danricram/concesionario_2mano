from odoo import models, fields

class Cliente(models.Model):
    _name = "concesionario.cliente"
    _description = "Cliente"

    dni = fields.Char(string="DNI/NIE/Pasaporte", unique=True)
    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos")
    correo_electronico = fields.Char(string="Correo Electrónico")
    telefono = fields.Char(string="Teléfono")
    direccion = fields.Text(string="Dirección")
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    comentarios = fields.Text(string="Comentarios")
    vehiculo_preferido = fields.Many2one("concesionario.vehiculo", string="Vehículo Preferido")
    tipo_cliente = fields.Selection([
        ("particular", "Particular"),
        ("empresa", "Empresa")
    ], string="Tipo de Cliente", default="particular")
    historial_compras = fields.One2many("concesionario.venta", "cliente_id", string="Historial de Compras")

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.nombre} {record.apellidos}" if record.apellidos else record.nombre
            result.append((record.id, name))
        return result