# epitag/utils/jinja_filters.py

import frappe
from barcode import get_barcode_class
from io import BytesIO

def barcode(value, format_type="code128"):
    """Generate barcode as SVG string
    Args:
        value (str): Value to encode
        format_type (str): Barcode format (default: code128)
    Returns:
        str: SVG string of barcode
    """
    try:
        # Get the barcode class
        barcode_class = get_barcode_class(format_type)
        
        # Create barcode instance
        code = barcode_class(value)
        
        # Create an in-memory bytes buffer
        stream = BytesIO()
        
        # Write SVG to buffer
        code.write(stream, options={'write_text': False, 'module_height': 10})
        
        # Get SVG string and strip XML declaration for inline use
        svg_string = stream.getvalue().decode('utf-8')
        if svg_string.startswith('<?xml'):
            svg_string = svg_string[svg_string.find('<svg'):]
            
        return svg_string
    except Exception as e:
        frappe.log_error(f"Barcode generation error: {str(e)}")
        return f"Error generating barcode: {str(e)}"