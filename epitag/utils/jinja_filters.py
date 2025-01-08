import frappe
from barcode import get_barcode_class
from io import BytesIO

def barcode(value, format_type="code128", show_text=True):
    """Generate barcode as SVG string
    Args:
        value (str): Value to encode
        format_type (str): Barcode format (default: code128)
        show_text (bool): Whether to display the barcode text (default: True)
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
        
        # Write SVG to buffer with configurable text display
        code.write(stream, options={
            'write_text': show_text,
            'module_height': 8,     # Reduce height of bars
            'module_width': 0.25,  # Make bars thinner
            'quiet_zone': 6.5,     # Increase quiet zone (white space) on sides
            'text_distance': 3,    # Increase space between bars and text
            'font_size': 12,       # Slightly larger font
            'center_text': True    # Ensure text is centered
        })
        
        # Get SVG string and strip XML declaration for inline use
        svg_string = stream.getvalue().decode('utf-8')
        if svg_string.startswith('<?xml'):
            svg_string = svg_string[svg_string.find('<svg'):]
            
        return svg_string
    except Exception as e:
        frappe.log_error(f"Barcode generation error: {str(e)}")
        return f"Error generating barcode: {str(e)}"