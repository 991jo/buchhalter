def is_number(s):
    try:
        float(s)
        return True
    except:
        return False

def is_int(s):
    try:
        int(s)
        return True
    except:
        return False

