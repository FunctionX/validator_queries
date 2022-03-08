def _convert_value_into_human_readable(number:str):
    if number=="":
        number=0
    else:
        number=float(int(number)*10**-18)
    return number