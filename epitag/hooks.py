app_name = "epitag"
app_title = "EpiTag"
app_publisher = "Applied Relevance"
app_description = "Barcode and QR code printing and scanning support for ERPNext"
app_email = "geveritt@appliedrelevance.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_js = [
#     "/assets/epitag/js/qr_scanner.js"
# ]
# app_include_css = [
#     "/assets/epitag/css/qr_scanner.css"
# ]

# Jinja
jinja = {"filters": ["epitag.utils.jinja_filters.barcode"]}

# Fixtures
# --------
fixtures = [
    {
        "doctype": "Print Format",
        "filters": [
            {
                "name": [
                    "in",
                    [
                        "Barcode Format Demo",
                        "Compact Shelf Label",
                        "Inventory Sheet with QR Codes",
                    ],
                ]
            }
        ],
    }
]
