from utils import inteiro_para_binario, inteiro_para_hex

# Mapeamento de nomes de registradores para seus números binários (5 bits)
REGISTRADORES_MAP = {
    '$zero': '00000', '$at': '00001', '$v0': '00010', '$v1': '00011',
    '$a0': '00100', '$a1': '00101', '$a2': '00110', '$a3': '00111',
    '$t0': '01000', '$t1': '01001', '$t2': '01010', '$t3': '01011',
    '$t4': '01100', '$t5': '01101', '$t6': '01110', '$t7': '01111',
    '$s0': '10000', '$s1': '10001', '$s2': '10010', '$s3': '10011',
    '$s4': '10100', '$s5': '10101', '$s6': '10110', '$s7': '10111',
    '$t8': '11000', '$t9': '11001', '$k0': '11010', '$k1': '11011',
    '$gp': '11100', '$sp': '11101', '$fp': '11110', '$ra': '11111'
}

# Opcodes MIPS (6 bits)
# Formato: opcode | rs | rt | rd/immediate/target | shamt/funct
OPCODES = {
    'add':  '000000',  # R-type
    'sub':  '000000',  # R-type
    'addi': '001000',  # I-type
    'lw':   '100011',  # I-type
    'sw':   '101011',  # I-type
    'beq':  '000100',  # I-type
    'j':    '000010',  # J-type
    # Adicionar mais opcodes conforme novas instruções forem implementadas
}

# Funct codes para instruções R-type (6 bits)
FUNCT_CODES = {
    'add': '100000',
    'sub': '100010',
    # Adicionar mais funct codes conforme novas instruções R-type forem implementadas
}

def converter_para_binario_complemento_de_2(valor, bits):
    """Converte um inteiro (positivo ou negativo) para binário usando complemento de 2."""
    if valor >= 0:
        return format(valor, f'0{bits}b')
    else:
        # Calcular o complemento de 2
        # Ex: -1 em 16 bits: 0xFFFF (65535)
        return format((1 << bits) + valor, f'0{bits}b')

def assemble_instrucao(instrucao):
    """
    Converte uma instrução MIPS (objeto Instrucao) para sua representação binária de 32 bits.
    Retorna a string binária e a string hexadecimal.
    """
    opcode = instrucao.opcode
    operandos = instrucao.operandos
    
    binario = ""
    hexadecimal = ""

    if opcode in OPCODES:
        op_code_bin = OPCODES[opcode]

        if opcode in ['add', 'sub']: # Tipo R: add, sub
            # Formato: opcode | rs | rt | rd | shamt (00000) | funct
            rd = REGISTRADORES_MAP.get(operandos[0])
            rs = REGISTRADORES_MAP.get(operandos[1])
            rt = REGISTRADORES_MAP.get(operandos[2])
            
            if not all([rd, rs, rt]):
                print(f"Erro: Registrador inválido em instrução R-type: {instrucao}")
                binario = '0' * 32
            else:
                shamt = '00000' # Para add/sub, shamt é 0
                funct = FUNCT_CODES.get(opcode)
                if not funct:
                    print(f"Erro: Funct code não encontrado para {opcode}")
                    binario = '0' * 32
                else:
                    binario = op_code_bin + rs + rt + rd + shamt + funct

        elif opcode == 'addi': # Tipo I: addi
            # Formato: opcode | rs | rt | immediate (16 bits)
            rt = REGISTRADORES_MAP.get(operandos[0])
            rs = REGISTRADORES_MAP.get(operandos[1])
            
            if not all([rt, rs]):
                print(f"Erro: Registrador inválido em instrução ADDI: {instrucao}")
                binario = '0' * 32
            else:
                try:
                    immediate = int(operandos[2])
                    # Garante que o imediato caiba em 16 bits, usando complemento de 2 se negativo
                    immediate_bin = converter_para_binario_complemento_de_2(immediate, 16)
                    binario = op_code_bin + rs + rt + immediate_bin
                except ValueError:
                    print(f"Erro: Imediato inválido em instrução ADDI: {instrucao}")
                    binario = '0' * 32

        elif opcode in ['lw', 'sw']: # Tipo I: lw, sw
            # Formato: opcode | base (rs) | rt | offset (16 bits)
            rt = REGISTRADORES_MAP.get(operandos[0])
            
            if not rt:
                print(f"Erro: Registrador de destino inválido em instrução LW/SW: {instrucao}")
                binario = '0' * 32
            else:
                try:
                    # Parse 'offset(base)'
                    offset_str, base_reg_str = operandos[1].replace(')', '').split('(')
                    offset = int(offset_str)
                    rs = REGISTRADORES_MAP.get(base_reg_str.strip())
                    
                    if not rs:
                        print(f"Erro: Registrador base inválido em instrução LW/SW: {instrucao}")
                        binario = '0' * 32
                    else:
                        # Garante que o offset caiba em 16 bits, usando complemento de 2 se negativo
                        offset_bin = converter_para_binario_complemento_de_2(offset, 16)
                        binario = op_code_bin + rs + rt + offset_bin
                except (ValueError, IndexError):
                    print(f"Erro: Formato de endereço inválido em instrução LW/SW: {instrucao}")
                    binario = '0' * 32

        elif opcode == 'beq': # Tipo I: beq
            # Formato: opcode | rs | rt | offset (16 bits)
            rs = REGISTRADORES_MAP.get(operandos[0])
            rt = REGISTRADORES_MAP.get(operandos[1])

            if not all([rs, rt]):
                print(f"Erro: Registrador inválido em instrução BEQ: {instrucao}")
                binario = '0' * 32
            else:
                try:
                    offset = int(operandos[2])
                    # Offset é um valor imediato de 16 bits, relativo ao PC
                    offset_bin = converter_para_binario_complemento_de_2(offset, 16)
                    binario = op_code_bin + rs + rt + offset_bin
                except ValueError:
                    print(f"Erro: Offset inválido em instrução BEQ: {instrucao}")
                    binario = '0' * 32

        elif opcode == 'j': # Tipo J: j
            # Formato: opcode | target address (26 bits)
            try:
                target = int(operandos[0])
                # Em MIPS real, o target é um endereço de palavra e é shifted 2 bits para a direita.
                # Aqui, para simplicidade, assumimos que o target já é o endereço de instrução.
                # E o valor é 26 bits
                target_bin = format(target, '026b') # Assume target é um número de linha/instrução
                binario = op_code_bin + target_bin
            except ValueError:
                print(f"Erro: Target inválido em instrução J: {instrucao}")
                binario = '0' * 32

        else:
            print(f"Erro: Instrução '{opcode}' não suporta montagem ou tipo desconhecido.")
            binario = '0' * 32 # Retorna 32 zeros para instrução não reconhecida
            
    else:
        print(f"Erro: Opcode '{opcode}' não reconhecido.")
        binario = '0' * 32 # Retorna 32 zeros para opcode não reconhecido

    # Converte a string binária para hexadecimal
    if binario and len(binario) == 32:
        try:
            # Converte para inteiro e depois para hexadecimal
            decimal_val = int(binario, 2)
            hexadecimal = inteiro_para_hex(decimal_val) # Usa a função do utils
        except ValueError:
            hexadecimal = "0x" + "0"*8 # Em caso de erro na conversão
    else:
        hexadecimal = "0x" + "0"*8

    return binario, hexadecimal