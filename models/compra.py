from odoo import models, fields

class Compra(models.Model):
    _name = 'concesionario.compra'
    _description = 'Registro de Compras'

    proveedor_id = fields.Many2one('concesionario.proveedor', string="Proveedor", required=True)
    vehiculo_id = fields.Many2one('concesionario.vehiculo', string="Vehículo", required=True)
    fecha_compra = fields.Date(string="Fecha de Compra", default=fields.Date.today, required=True)
    vehiculos_comprados = fields.Many2many("concesionario.vehiculo", string="Vehículos Comprados")
    cantidad = fields.Integer(string="Cantidad", default=1, required=True)
    precio_unitario = fields.Float(string="Precio Unitario", required=True)
    precio_total = fields.Float(string="Precio Total",  required=True)
    metodo_pago = fields.Selection([
        ("transferencia", "Transferencia Bancaria"),
        ("tarjeta", "Tarjeta de Crédito"),
        ("efectivo", "Efectivo")
    ], string="Método de Pago Preferido", default="transferencia")
    estado = fields.Selection(
        [
            ('nuevo', 'Nuevo'),
            ('usado', 'Usado'),
            ('reparado', 'Reparado'),
        ], string="Estado", default='nuevo')
    notas = fields.Text(string="Notas")
    vehiculo_id = fields.Many2one("concesionario.vehiculo", string="Vehículo", required=True)

    def action_compra(self):
        for compra in self:
            # Comprobamos si el vehículo ya está en la gestión de vehículos
            if not compra.vehiculo_id:
                # Si no existe, creamos el vehículo en la gestión
                vehiculo = self.env['concesionario.vehiculo'].create({
                    'matricula': compra.vehiculo_id.matricula,  # Asignamos la matrícula
                    'marca': compra.vehiculo_id.marca,  # Asignamos la marca
                    'modelo': compra.vehiculo_id.modelo,  # Asignamos el modelo
                    'color': compra.vehiculo_id.color,  # Asignamos el color
                    'año': compra.vehiculo_id.año,  # Asignamos el año
                    'kilometraje': compra.vehiculo_id.kilometraje,  # Asignamos kilometraje
                    'potencia_cv': compra.vehiculo_id.potencia_cv,  # Asignamos potencia
                    'precio': compra.precio_unitario,  # Asignamos precio unitario
                    'estado': 'disponible',  # Marcamos el vehículo como disponible
                    'tipo_combustible': compra.vehiculo_id.tipo_combustible,  # Tipo de combustible
                    'transmision': compra.vehiculo_id.transmision,  # Transmisión
                    'descripcion': compra.vehiculo_id.descripcion,  # Descripción
                    'imagen': compra.vehiculo_id.imagen,  # Imagen
                })
                compra.vehiculo_id = vehiculo  # Asignamos el vehículo creado a la compra
            else:
                # Si el vehículo ya existe, solo cambiamos su estado a disponible
                compra.vehiculo_id.estado = 'disponible'

#    @api.depends('cantidad', 'precio_unitario')
#    def _compute_total(self):
#        for record in self:
#            record.precio_total = record.cantidad * record.precio_unitario