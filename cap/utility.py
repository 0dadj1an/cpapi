import base64

def base64_ascii(base64resp):
    """Converts base64 to ascii for run command/showtask."""
    return base64.b64decode(base64resp).decode('utf-8')
