# utils.py

def inteiro_para_binario(valor, bits=32):
    """
    Converte um inteiro para uma string binária com padding (zero à esquerda).
    """
    return format(valor & ((1 << bits) - 1), f'0{bits}b')


def inteiro_para_hex(valor):
    """
    Converte um inteiro para hexadecimal (com prefixo 0x).
    """
    return hex(valor & 0xFFFFFFFF)


def parse_offset_base(arg):
    """
    Interpreta strings do tipo '4($t0)' e retorna (4, '$t0').
    """
    if '(' in arg:
        offset_str, base_str = arg.replace(')', '').split('(')
        return int(offset_str), base_str.strip()
    else:
        raise ValueError(f"Formato inválido para offset(base): {arg}")
