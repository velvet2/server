def hasLabel(data):
    label = data.get('label', False)
    if label is False:
        return False
    else: 
        return bool(label.get('config', False))