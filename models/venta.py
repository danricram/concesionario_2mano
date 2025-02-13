from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Venta(models.Model):
    _name = "concesionario.venta"
    _description = "Venta"

    cliente_id = fields.Many2one("concesionario.cliente", string="Cliente", required=True)
    vehiculo_id = fields.Many2one("concesionario.vehiculo", string="Vehículo", required=True)
    fecha_venta = fields.Date(string="Fecha de Venta", default=fields.Date.today)
    cantidad = fields.Integer(string="Cantidad", default=1, required=True)
    precio_unitario = fields.Float(string="Precio Unitario", related="vehiculo_id.precio", readonly=True)
    precio_total = fields.Float(string="Precio Total", compute="_compute_precio_total", store=True)
    metodo_pago = fields.Selection([
        ("contado", "Pago al Contado"),
        ("financiado", "Financiado"),
        ("leasing", "Leasing")
    ], string="Método de Pago")
    fecha_entrega = fields.Date(string="Fecha de Entrega")

    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado')
    ], string="Estado", default="borrador", tracking=True)

    @api.depends("cantidad", "vehiculo_id")
    def _compute_precio_total(self):
        for venta in self:
            venta.precio_total = venta.cantidad * venta.precio_unitario if venta.vehiculo_id else 0.0

    def action_confirmar(self):
        """Cambia el estado a 'Confirmado' y descuenta el stock."""
        for venta in self:
            # Verificamos si hay suficiente stock
            if venta.vehiculo_id.cantidad < venta.cantidad:
                raise ValidationError("No hay suficientes vehículos en stock para esta venta.")

            # Descontamos del stock
            venta.vehiculo_id.cantidad -= venta.cantidad  
            venta.write({'estado': 'confirmado'})

            # Si el stock llega a 0, marcamos el vehículo como 'vendido'
            if venta.vehiculo_id.cantidad == 0:
                venta.vehiculo_id.estado = 'vendido'

    def action_entregar(self):
        """Cambia el estado a 'Entregado' solo si está confirmado."""
        for venta in self:
            if venta.estado != 'confirmado':
                raise ValidationError("La venta debe estar confirmada antes de ser entregada.")
            
            venta.write({'estado': 'entregado'})

    def action_cancelar(self):
        """Cambia el estado a 'Cancelado' y devuelve el stock si estaba confirmado."""
        for venta in self:
            if venta.estado == 'confirmado':  # Solo si ya estaba confirmado
                # Se devuelve el stock
#                venta.vehiculo_id.cantidad += venta.cantidad
                venta.vehiculo_id.cantidad += self.cantidad  # Aumentar el stock cuando se recibe
                venta.vehiculo_id.estado = 'disponible'  # Lo marcamos como disponible

            # Cambiamos el estado a cancelado
            venta.write({'estado': 'cancelado'})

    @api.model
    def create(self, vals):
        """
        Sobreescribimos el método create para actualizar la cantidad del vehículo vendido y evitar ventas con cantidad 0.
        """
        vehiculo = self.env['concesionario.vehiculo'].browse(vals['vehiculo_id'])

        if vehiculo.cantidad <= 0:
            raise ValidationError("Lo sentimos, ya no nos quedan unidades de este vehículo.")

        venta = super(Venta, self).create(vals)
        
        return venta