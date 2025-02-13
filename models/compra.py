from odoo import models, fields, api

class Compra(models.Model):
    _name = 'concesionario.compra'
    _description = 'Registro de Compras'

    proveedor_id = fields.Many2one('concesionario.proveedor', string="Proveedor", required=True)
    vehiculo_id = fields.Many2one('concesionario.vehiculo', string="Vehículo", required=True)
    fecha_compra = fields.Date(string="Fecha de Compra", default=fields.Date.today, required=True)
    cantidad = fields.Integer(string="Cantidad", default=1, required=True)
    precio_unitario = fields.Float(string="Precio Unitario", related="vehiculo_id.precio", readonly=True)
    precio_total = fields.Float(string="Precio Total", compute="_compute_precio_total", store=True)
    metodo_pago = fields.Selection([
        ("transferencia", "Transferencia Bancaria"),
        ("tarjeta", "Tarjeta de Crédito"),
        ("efectivo", "Efectivo")
    ], string="Método de Pago Preferido", default="transferencia")
    notas = fields.Text(string="Notas")

    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('reservado', 'Reservado'),
        ('confirmado', 'Confirmado'),
        ('recibido', 'Recibido'),
        ('cancelado', 'Cancelado')
    ], string="Estado", default="borrador", tracking=True)

    @api.depends('cantidad', 'precio_unitario')
    def _compute_precio_total(self):
        """ Calcula el precio total basado en la cantidad y el precio unitario. """
        for record in self:
            record.precio_total = record.cantidad * record.precio_unitario if record.vehiculo_id else 0

    def action_reservar(self):
        """ Cambia el estado a 'Reservado' y recarga la vista. """
        self.write({'estado': 'reservado'})
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def action_confirmar(self):
        """ Cambia el estado a 'Confirmado' y recarga la vista. """
        self.write({'estado': 'confirmado'})
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def action_recibir(self):
        """ Cambia el estado a 'Recibido', aumenta el stock del vehículo y recarga la vista. """
        self.write({'estado': 'recibido'})
        if self.vehiculo_id:
            self.vehiculo_id.cantidad += self.cantidad  # Aumentar el stock cuando se recibe
            self.vehiculo_id.estado = 'disponible'
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def action_cancelar(self):
        """Cambia el estado a 'Cancelado', devuelve el stock y recarga la vista."""
        if self.estado == 'confirmado':  # Solo si la compra estaba confirmada
            self.vehiculo_id.cantidad -= self.cantidad  # Revertir la compra (quitar del stock)

        self.write({'estado': 'cancelado'})
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    @api.model
    def create(self, vals):
        """
        Sobreescribimos el método create para agregar un nuevo vehículo
        a la gestión de vehículos si no existe previamente.
        """
        compra = super(Compra, self).create(vals)

        vehiculo_existente = self.env['concesionario.vehiculo'].search([
            ('marca', '=', compra.vehiculo_id.marca),
            ('modelo', '=', compra.vehiculo_id.modelo)
        ], limit=1)

        if not vehiculo_existente:
            vehiculo = self.env['concesionario.vehiculo'].create({
                'marca': compra.vehiculo_id.marca,
                'modelo': compra.vehiculo_id.modelo,
                'matricula': compra.vehiculo_id.matricula,
                'color': compra.vehiculo_id.color,
                'año': compra.vehiculo_id.año,
                'kilometraje': compra.vehiculo_id.kilometraje,
                'potencia_cv': compra.vehiculo_id.potencia_cv,
                'precio': compra.vehiculo_id.precio_unitario,
                'estado': 'disponible',
                'tipo_combustible': compra.vehiculo_id.tipo_combustible,
                'transmision': compra.vehiculo_id.transmision,
                'descripcion': compra.vehiculo_id.descripcion,
                'imagen': compra.vehiculo_id.imagen,
                'cantidad': 0  # No aumentamos la cantidad
            })
            compra.write({'vehiculo_id': vehiculo.id})
        
        return compra