from odoo import models, fields, api

class Compra(models.Model):
    _name = 'concesionario.compra'
    _description = 'Registro de Compras'

    proveedor_id = fields.Many2one('concesionario.proveedor', string="Proveedor", required=True)
    vehiculo_id = fields.Many2one('concesionario.vehiculo', string="Vehículo", required=True)
    fecha_compra = fields.Date(string="Fecha de Compra", default=fields.Date.today, required=True)
    precio = fields.Float(string="Precio Total", required=True)
    metodo_pago = fields.Selection([
        ("transferencia", "Transferencia Bancaria"),
        ("tarjeta", "Tarjeta de Crédito"),
        ("efectivo", "Efectivo")
    ], string="Método de Pago Preferido", default="transferencia")
    notas = fields.Text(string="Notas")

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
                'precio': compra.vehiculo_id.precio,
                'estado': 'disponible',
                'tipo_combustible': compra.vehiculo_id.tipo_combustible,
                'transmision': compra.vehiculo_id.transmision,
                'descripcion': compra.vehiculo_id.descripcion,
                'imagen': compra.vehiculo_id.imagen,
                'cantidad': 1  # Inicializamos la cantidad en 1
            })
            compra.write({'vehiculo_id': vehiculo.id})
        else:
            vehiculo_existente.estado = 'disponible'
            vehiculo_existente.cantidad += 1  # Aumentamos la cantidad en 1
        return compra








#    def action_compra(self):
#        for compra in self:
#            for vehiculo_comprado in compra.vehiculos_comprados:
                # Comprobamos si el vehículo ya está en la gestión de vehículos
#                if not vehiculo_comprado.vehiculo_id:
                    # Si no existe, creamos el vehículo en la gestión
#                    vehiculo = self.env['concesionario.vehiculo'].create({
#                        'matricula': vehiculo_comprado.vehiculo_id.matricula,  # Asignamos la matrícula
#                        'marca': vehiculo_comprado.vehiculo_id.marca,  # Asignamos la marca
#                        'modelo': vehiculo_comprado.vehiculo_id.modelo,  # Asignamos el modelo
#                        'color': vehiculo_comprado.vehiculo_id.color,  # Asignamos el color
#                        'año': vehiculo_comprado.vehiculo_id.año,  # Asignamos el año
#                        'kilometraje': vehiculo_comprado.vehiculo_id.kilometraje,  # Asignamos kilometraje
#                        'potencia_cv': vehiculo_comprado.vehiculo_id.potencia_cv,  # Asignamos potencia
#                        'precio': vehiculo_comprado.precio_unitario,  # Asignamos precio unitario
#                        'estado': 'disponible',  # Marcamos el vehículo como disponible
#                        'tipo_combustible': vehiculo_comprado.vehiculo_id.tipo_combustible,  # Tipo de combustible
#                        'transmision': vehiculo_comprado.vehiculo_id.transmision,  # Transmisión
#                        'descripcion': vehiculo_comprado.vehiculo_id.descripcion,  # Descripción
#                        'imagen': vehiculo_comprado.vehiculo_id.imagen,  # Imagen
#                    })
#                    vehiculo_comprado.vehiculo_id = vehiculo  # Asignamos el vehículo creado a la compra
#                else:
                    # Si el vehículo ya existe, solo cambiamos su estado a disponible
#                    vehiculo_comprado.vehiculo_id.estado = 'disponible'


#    def action_compra(self):
#        for compra in self:
            # Comprobamos si el vehículo ya está en la gestión de vehículos
#            if not compra.vehiculo_id:
                # Si no existe, creamos el vehículo en la gestión
#                vehiculo = self.env['concesionario.vehiculo'].create({
#                    'matricula': compra.vehiculo_id.matricula,  # Asignamos la matrícula
#                    'marca': compra.vehiculo_id.marca,  # Asignamos la marca
#                    'modelo': compra.vehiculo_id.modelo,  # Asignamos el modelo
#                    'color': compra.vehiculo_id.color,  # Asignamos el color
#                    'año': compra.vehiculo_id.año,  # Asignamos el año
#                    'kilometraje': compra.vehiculo_id.kilometraje,  # Asignamos kilometraje
#                    'potencia_cv': compra.vehiculo_id.potencia_cv,  # Asignamos potencia
#                    'precio': compra.precio_unitario,  # Asignamos precio unitario
#                    'estado': 'disponible',  # Marcamos el vehículo como disponible
#                    'tipo_combustible': compra.vehiculo_id.tipo_combustible,  # Tipo de combustible
#                    'transmision': compra.vehiculo_id.transmision,  # Transmisión
#                    'descripcion': compra.vehiculo_id.descripcion,  # Descripción
#                    'imagen': compra.vehiculo_id.imagen,  # Imagen
#                })
#                compra.vehiculo_id = vehiculo  # Asignamos el vehículo creado a la compra
#            else:
                # Si el vehículo ya existe, solo cambiamos su estado a disponible
#                compra.vehiculo_id.estado = 'disponible'

#    def create(self, vals):
#        """Al crear una compra, se genera automáticamente un vehículo si no se ha seleccionado uno."""
#        if 'vehiculo_id' not in vals or not vals.get('vehiculo_id'):
#            vehiculo_vals = {
#                'marca': vals.get('marca', 'Desconocida'),
#                'modelo': vals.get('modelo', 'Desconocido'),
#                'color': vals.get('color', 'No especificado'),
#                'año': vals.get('año', 2024),
#                'kilometraje': vals.get('kilometraje', 0.0),
#                'potencia_cv': vals.get('potencia_cv', 0.0),
#                'precio': vals.get('precio_unitario', 0.0),
#                'estado': 'disponible',
#                'tipo_combustible': vals.get('tipo_combustible', 'gasolina'),
#                'transmision': vals.get('transmision', 'manual'),
#                'descripcion': vals.get('descripcion', ''),
#                'imagen': vals.get('imagen', False),
#            }
#            nuevo_vehiculo = self.env['concesionario.vehiculo'].create(vehiculo_vals)
#            vals['vehiculo_id'] = nuevo_vehiculo.id  # Asignamos el nuevo vehículo a la compra

#        return super(Compra, self).create(vals)






#    @api.depends('cantidad', 'precio_unitario')
#    def _compute_total(self):
#        for record in self:
#            record.precio_total = record.cantidad * record.precio_unitario