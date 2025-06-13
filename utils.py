def inteiro_para_binario(valor, bits=32):
    # Converte um inteiro para uma string binária de 'bits' de comprimento.
    # Usa complemento de 2 para valores negativos.
    if valor < 0:
        return format((1 << bits) + valor, f'0{bits}b')
    else:
        return format(valor, f'0{bits}b')

def inteiro_para_hex(valor):
    # Converte um inteiro para uma string hexadecimal de 32 bits (prefixo 0x)
    return hex(valor & 0xFFFFFFFF)

def parse_offset_base(arg):
    # Analisa strings no formato "offset(base_register)"
    if '(' in arg and arg.endswith(')'):
        offset_str, base_str = arg.replace(')', '').split('(')
        try:
            return int(offset_str), base_str.strip()
        except ValueError:
            raise ValueError(f"Offset inválido em '{arg}'. Deve ser um número inteiro.")
    else:
        raise ValueError(f"Formato inválido para offset(base): {arg}. Esperado 'offset(registrador)'")