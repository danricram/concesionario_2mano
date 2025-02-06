from odoo import models, fields

class Proveedor(models.Model):
    _name = "concesionario.proveedor"
    _description = "Proveedor"

    cif = fields.Char(string="CIF/NIF", unique=True, help="Número de Identificación Fiscal del proveedor")
    nombre = fields.Char(string="Nombre", required=True)
    contacto = fields.Char(string="Persona de Contacto")
    telefono = fields.Char(string="Teléfono")
    correo_electronico = fields.Char(string="Correo Electrónico")
    direccion = fields.Text(string="Dirección")
    tipo_proveedor = fields.Selection([
        ("nacional", "Nacional"),
        ("internacional", "Internacional")
    ], string="Tipo de Proveedor", default="nacional")
    historial_compras = fields.One2many("concesionario.compra", "proveedor_id", string="Historial de Compras")
    productos_suministrados = fields.Many2many("concesionario.vehiculo", string="Vehículos Suministrados")

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.nombre} ({record.cif})" if record.cif else record.nombre
            result.append((record.id, name))
        return result