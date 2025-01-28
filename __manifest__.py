{
    "name": "Concesionario de Autos de Segunda Mano",
    "version": "1.0.0",
    "summary": "Gestión de vehículos, clientes y ventas para concesionarios de autos usados.",
    "author": "Daniel Rico Ramírez",
    "website": "http://www.dadesapp.com",
    "license": "AGPL-3",
    "category": "Sales",
    "depends": ["base", "sale", "stock"],  # Dependencias de Odoo
    "data": [
        "security/ir.model.access.csv",  # Permisos de acceso
        "views/vehicle_views.xml",  # Vistas para los vehículos
        "views/customer_views.xml",  # Vistas para clientes
        "views/sale_views.xml",  # Vistas para ventas
        "data/initial_data.xml",  # Datos iniciales (opcional)
    ],
    "demo": ["demo/demo_data.xml"],  # Datos de demostración (opcional)
    "installable": True,
    "application": True,
    "auto_install": False,
}
