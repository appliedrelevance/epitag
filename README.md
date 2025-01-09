# EpiTag

EpiTag is a barcode label printing solution designed specifically for ERPNext. It enables seamless generation, printing, and management of barcode labels directly from your ERPNext system.

## Features

- Barcode Label Printing
  - Supports multiple barcode formats including:
    - Code 128
    - Code 39
    - EAN-13
    - EAN-8
    - UPC-A
    - ISBN-13
    - ISBN-10
    - ISSN
    - JAN
    - PZN
  - Dynamic barcode generation based on ERPNext data
  - Customizable label templates and layouts
  - Batch printing capabilities
  - Print queue management
  - Network and USB printer support

## Roadmap

- QR Code support for expanded data capacity
- Additional barcode formats as needed
- Template designer improvements


## Prerequisites

- Python 3.10 or higher
- ERPNext 15.x
- Frappe Bench

## Installation

1. From your bench directory, get the app:
   ```bash
   bench get-app epitag https://github.com/appliedrelevance/epitag
   ```

2. Install the app on your site:
   ```bash
   bench --site your-site.local install-app epitag
   ```

3. Build and install dependencies:
   ```bash
   bench build
   bench restart
   ```

## Configuration

1. Access ERPNext Settings
2. Navigate to EpiTag Settings
3. Configure your printer settings:
   - Printer protocol (EPL, ZPL)
   - Connection type (Network, USB)
   - Default templates

## Usage

### Basic Barcode Generation

```python
from epitag.utils.jinja_filters import barcode

# Generate Code 128 barcode
svg_string = barcode("123456789", "code128")
```

### Creating a Print Format

1. Navigate to Settings > Printing > Print Format
2. Click "New"
3. Fill in the basic details:
   - Name (e.g., "Barcode Item Label")
   - Module (e.g., "Stock")
   - DocType (e.g., "Item")
4. Check "Custom Format"
5. Set "Print Format Type" to "Jinja"
6. In the HTML editor, create your template using the `barcode` filter

Here's an example template for item labels:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        /* Label sizing and layout */
        .shelf-label {
            width: 4in;
            height: 2in;
            padding: 0.125in;
            font-family: Arial, sans-serif;
            page-break-inside: avoid;
        }
        
        /* Barcode container */
        .barcode-container {
            text-align: center;
            margin: 0.125in 0;
        }
        
        .barcode-container svg {
            max-width: 3in;
            height: 0.75in;
        }
        
        @media print {
            @page {
                size: 4in 2in;
                margin: 0;
            }
        }
    </style>
</head>
<body>
    <div class="shelf-label">
        <div class="item-code">{{ doc.item_code }}</div>
        <div class="item-name">{{ doc.item_name }}</div>
        
        <div class="barcode-container">
            {%- if doc.barcodes and doc.barcodes|length > 0 -%}
                {% set barcode_map = {
                    'EAN-13': 'ean13',
                    'EAN-8': 'ean8',
                    'UPC-A': 'upca',
                    'CODE-128': 'code128',
                    'CODE-39': 'code39',
                    'ISBN': 'isbn13',
                    'ISBN-10': 'isbn10',
                    'ISSN': 'issn',
                    'JAN': 'jan',
                    'PZN': 'pzn'
                } %}
                {% set barcode_type = barcode_map.get(doc.barcodes[0].barcode_type, 'code128') %}
                {{ doc.barcodes[0].barcode|barcode(barcode_type) }}
            {%- endif -%}
        </div>
        
        <div class="additional-info">
            <div>UOM: {{ doc.stock_uom }}</div>
            <div>Stock: {{ frappe.db.get_value("Bin", {"item_code": doc.item_code, 
                         "warehouse": doc.item_defaults[0].default_warehouse}, 
                         "actual_qty") if doc.item_defaults else 0 }}</div>
        </div>
    </div>
</body>
</html>
```

Key features of this template:
- Uses standard paper sizes (4"x2")
- Centers the barcode with appropriate dimensions
- Includes item details and stock information
- Proper print media handling
- Automatic barcode type mapping from ERPNext to python-barcode formats

The `barcode` filter supports these format mappings:
- EAN-13 → ean13
- EAN-8 → ean8
- UPC-A → upca
- CODE-128 → code128
- CODE-39 → code39
- ISBN → isbn13
- ISBN-10 → isbn10
- ISSN → issn
- JAN → jan
- PZN → pzn

### Batch Printing

1. Select items from any DocType
2. Use the "Print Labels" action
3. Choose your template
4. Specify quantity
5. Submit to print queue

## Development

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/appliedrelevance/epitag.git
   ```

2. Install development dependencies:
   ```bash
   bench setup requirements --dev
   ```

3. Run tests:
   ```bash
   bench --site your-site.local run-tests --app epitag
   ```

### Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Write tests for your changes
4. Submit a pull request

## Documentation

For detailed documentation, please visit our [documentation site](https://epitag.appliedrelevance.com/docs).

## Support

For support and discussions:
- GitHub Issues: [https://github.com/appliedrelevance/epitag/issues](https://github.com/appliedrelevance/epitag/issues)
- ERPNext Forums: Tag your posts with 'epitag'

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Applied Relevance ([geveritt@appliedrelevance.com](mailto:geveritt@appliedrelevance.com))

## Acknowledgments

- ERPNext Community
- Frappe Framework Team
- Python Barcode Library Contributors