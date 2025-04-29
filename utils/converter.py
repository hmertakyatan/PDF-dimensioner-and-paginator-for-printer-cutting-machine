def convert_to_float(text):
    try:
        return float(text)
    except ValueError:
        return None
def convert_to_int(text):
    try:
        return int(text)
    except ValueError:
        return None