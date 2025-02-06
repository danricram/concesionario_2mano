from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Venta(models.Model):
    _name = "concesionario.venta"
    _description = "Venta"

    cliente_id = fields.Many2one("concesionario.cliente", string="Cliente", required=True)
    vehiculo_id = fields.Many2one("concesionario.vehiculo", string="Vehículo", required=True)
    fecha_venta = fields.Date(string="Fecha de Venta", default=fields.Date.today)
    precio = fields.Float(string="Precio de Venta", related="vehiculo_id.precio")
    metodo_pago = fields.Selection([
        ("contado", "Pago al Contado"),
        ("financiado", "Financiado"),
        ("leasing", "Leasing")
    ], string="Método de Pago")
    fecha_entrega = fields.Date(string="Fecha de Entrega")

    @api.model
    def create(self, vals):
        """
        Sobreescribimos el método create para actualizar la cantidad del vehículo vendido y evitar ventas con cantidad 0.
        """
        vehiculo = self.env['concesionario.vehiculo'].browse(vals['vehiculo_id'])

        if vehiculo.cantidad <= 0:
            raise ValidationError("Lo sentimos, ya no nos quedan unidades de este vehículo.")

        venta = super(Venta, self).create(vals)
        
        if vehiculo.cantidad > 0:
            vehiculo.cantidad -= 1  # Restamos 1 a la cantidad de vehículos

        # Opcional: Cambiar el estado del vehículo si ya no hay unidades disponibles
        if vehiculo.cantidad == 0:
            vehiculo.estado = 'vendido'
        
        return venta