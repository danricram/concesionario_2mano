{
    "name": "Concesionario",
    "version": "1.0.0",
    "summary": "Gestión de vehículos, clientes y ventas para concesionarios.",
    "author": "Daniel Rico Ramírez",
    "website": "http://www.dadesapp.com",
    "license": "AGPL-3",
    "category": "Sales",
    "depends": ["base", "sale", "stock"],  # Dependencias de Odoo
    "data": [
        "security/ir.model.access.csv",  # Permisos de acceso
        "views/menu_view.xml",
    ],
    "demo": ["demo/demo_data.xml"],  # Datos de demostración (opcional)
    "installable": True,
    "application": True,
    "auto_install": False,
}