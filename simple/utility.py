def truncate(string, width):
    if len(string) <= width:
        return string
    return string[:width-3] + '...'
