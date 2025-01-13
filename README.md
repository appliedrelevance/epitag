# EpiTag

EpiTag is a comprehensive barcode and QR code solution designed specifically for ERPNext. It enables seamless generation, printing, and scanning of various barcode formats and QR codes directly from your ERPNext system.

## Features

### Barcode Generation and Printing
- Support for multiple barcode formats:
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

### QR Code Support
- Multiple QR code formats with configurable error correction levels:
  - Standard QR (M-15% error correction)
  - Low density QR (L-7% error correction)
  - High reliability QR (H-30% error correction)
- Rich data encoding for complex information
- Built-in QR code scanning support for web and mobile

### Print Formats
- Ready-to-use print format templates:
  - Barcode Format Demo (showcases all supported formats)
  - Compact Shelf Label (2.25" x 1.25")
  - Inventory Sheet with QR Codes
- Customizable label templates and layouts
- Print preview functionality
- Support for batch printing

### Scanning Features
- Built-in QR code scanner using device camera
- Automatic field population from scan results
- Support for both desktop and mobile browsers
- Visual scanning interface with feedback
- Integration with Frappe UI components

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

## Usage

### Barcode and QR Code Generation

In your print formats, use the `barcode` filter with the desired format:

```html
<!-- Generate Code 128 barcode -->
{{ doc.item_code|barcode("code128") }}

<!-- Generate QR code -->
{{ doc.item_code|barcode("qr") }}

<!-- Generate high-reliability QR code -->
{{ doc.item_code|barcode("qr-h") }}
```

### QR Code Scanning

The scanning interface is automatically added to Item fields. You can also use it programmatically:

```javascript
const scanner = new epitag.scanning.QRScanner({
    callback: (result) => {
        console.log('Scanned:', result);
        // Handle the scanned data
    }
});
scanner.show();
```

### Using Print Formats

1. Navigate to any Item document
2. Click Print > Format
3. Select one of the included formats:
   - Barcode Format Demo
   - Compact Shelf Label
   - Inventory Sheet with QR Codes

### Customizing Templates

1. Navigate to Settings > Printing > Print Format
2. Create a new format or customize existing ones
3. Use the `barcode` filter in your Jinja templates
4. Customize CSS for precise control over label dimensions and layout

## Error Correction Levels for QR Codes

- `qr` or `qr-m`: Medium level (15% data recovery)
- `qr-l`: Low level (7% data recovery)
- `qr-q`: Quartile level (25% data recovery)
- `qr-h`: High level (30% data recovery)

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