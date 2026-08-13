def bytes_to_human_readable(num_bytes: float):
    kb = 1024
    mb = kb ** 2
    gb = kb ** 3

    if num_bytes >= gb:
        return f"{num_bytes / gb:.2f} GB"
    elif num_bytes >= mb:
        return f"{num_bytes / mb:.2f} MB"
    elif num_bytes >= kb:
        return f"{num_bytes / kb:.2f} KB"
    else:
        return f"{num_bytes} Bytes"
