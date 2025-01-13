import frappe
from barcode import get_barcode_class
import qrcode
from io import BytesIO
import base64
from PIL import Image
import xml.etree.ElementTree as ET

def _make_svg_qr(qr_matrix, size):
    """Convert QR matrix to SVG string"""
    # SVG preamble and style
    svg = ET.Element('svg', {
        'viewBox': f'0 0 {size} {size}',
        'xmlns': 'http://www.w3.org/2000/svg',
        'version': '1.1'
    })
    
    # Create background
    ET.SubElement(svg, 'rect', {
        'width': str(size),
        'height': str(size),
        'fill': 'white'
    })
    
    # Create QR code squares
    for row in range(len(qr_matrix)):
        for col in range(len(qr_matrix[row])):
            if qr_matrix[row][col]:
                ET.SubElement(svg, 'rect', {
                    'x': str(col),
                    'y': str(row),
                    'width': '1',
                    'height': '1',
                    'fill': 'black'
                })
    
    # Convert to string
    return ET.tostring(svg, encoding='unicode')

def barcode(value, format_type="code128", show_text=True):
    """Generate barcode or QR code as SVG string
    Args:
        value (str): Value to encode
        format_type (str): Format type (default: code128)
                          For barcodes: code128, code39, ean13, ean8, etc.
                          For QR: qr, qr-l, qr-m, qr-q, qr-h (different error correction levels)
        show_text (bool): Whether to display the text (for barcodes only)
    Returns:
        str: SVG string of barcode or QR code
    """
    try:
        # Handle QR codes
        if format_type.startswith('qr'):
            # Parse error correction level
            error_correction = {
                'qr-l': qrcode.constants.ERROR_CORRECT_L,  # 7%
                'qr-m': qrcode.constants.ERROR_CORRECT_M,  # 15%
                'qr-q': qrcode.constants.ERROR_CORRECT_Q,  # 25%
                'qr-h': qrcode.constants.ERROR_CORRECT_H,  # 30%
            }.get(format_type, qrcode.constants.ERROR_CORRECT_M)  # Default to M

            # Create QR code instance
            qr = qrcode.QRCode(
                version=None,  # Auto-size
                error_correction=error_correction,
                box_size=1,    # Use 1 for SVG units
                border=4,
            )
            qr.add_data(value)
            qr.make(fit=True)

            # Convert matrix to SVG
            size = len(qr.modules) + 2 * qr.border  # Total size including border
            return _make_svg_qr(qr.modules, size)
            
        # Handle regular barcodes
        else:
            # Get the barcode class
            barcode_class = get_barcode_class(format_type)
            
            # Create barcode instance
            code = barcode_class(value)
            
            # Create an in-memory bytes buffer
            stream = BytesIO()
            
            # Write SVG to buffer with configurable text display
            code.write(stream, options={
                'write_text': show_text,
                'module_height': 8,     # Reduce height of bars
                'module_width': 0.25,   # Make bars thinner
                'quiet_zone': 6.5,      # Increase quiet zone (white space) on sides
                'text_distance': 3,     # Increase space between bars and text
                'font_size': 10,        # Slightly larger font
                'center_text': True     # Ensure text is centered
            })
            
            # Get SVG string and strip XML declaration for inline use
            svg_string = stream.getvalue().decode('utf-8')
            if svg_string.startswith('<?xml'):
                svg_string = svg_string[svg_string.find('<svg'):]
                
            return svg_string
                
    except Exception as e:
        frappe.log_error(f"Barcode/QR generation error: {str(e)}")
        return f"Error generating barcode/QR: {str(e)}"