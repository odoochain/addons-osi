{
    "name": "OSI Inventory Valuation by Location and Date",
    "version": "14.0.1.0.0",
    "category": "stock",
    "summary": "Stock Inventory Valuation by Location and Date export to Excel and PDF",
    "author": "Open Source Integrators",
    "website": "https://github.com/ursais/osi-addons",
    "depends": ["stock", "osi_stock_move_value"],
    "data": [
        "security/inventory_valuation_security.xml",
        "security/ir.model.access.csv",
        "wizard/inventory_valuation.xml",
        "views/inventory_valuation_menu.xml",
        "views/inventory_valuation_template.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
    "maintainers": ["b-kannan"],
}
