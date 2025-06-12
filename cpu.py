# def executar_instrucao(instrucao, registradores, memoria, pc):
#     op = instrucao.opcode
#     args = instrucao.operandos

#     try:
#         if op == 'addi':
#             rd, rs, imm = args
#             val = registradores.ler(rs) + int(imm)
#             registradores.escrever(rd, val)
#             return pc + 1

#         elif op == 'add':
#             rd, rs, rt = args
#             val = registradores.ler(rs) + registradores.ler(rt)
#             registradores.escrever(rd, val)
#             return pc + 1

#         elif op == 'sub':
#             rd, rs, rt = args
#             val = registradores.ler(rs) - registradores.ler(rt)
#             registradores.escrever(rd, val)
#             return pc + 1

#         elif op == 'beq':
#             rs, rt, offset = args
#             if registradores.ler(rs) == registradores.ler(rt):
#                 return pc + 1 + int(offset)
#             return pc + 1

#         elif op == 'j':
#             target = int(args[0])
#             return target

#         else:
#             print(f"Instrução não implementada: {op}")
#             return pc + 1

#     except Exception as e:
#         print(f"Erro executando {instrucao}: {e}")
#         return pc + 1

from utils import parse_offset_base
import sys # Importa sys para a syscall de exit

# Adicione a função para determinar o tipo da instrução
def obter_tipo_instrucao(opcode):
    tipo_r = ['add', 'sub'] # Adicionar mais instruções tipo R conforme implementado
    tipo_i = ['addi', 'beq', 'lw', 'sw'] # Adicionar mais instruções tipo I
    tipo_j = ['j'] # Adicionar mais instruções tipo J
    tipo_syscall = ['syscall'] # Adiciona o tipo para syscall

    if opcode in tipo_r:
        return 'R'
    elif opcode in tipo_i:
        return 'I'
    elif opcode in tipo_j:
        return 'J'
    elif opcode in tipo_syscall: # Nova verificação para syscall
        return 'SYSCALL'
    else:
        return 'Desconhecido' # Para instruções não implementadas ainda

def executar_instrucao(instrucao, registradores, memoria, pc):
    op = instrucao.opcode
    args = instrucao.operandos
    
    # Determina o tipo da instrução antes da execução
    tipo_inst = obter_tipo_instrucao(op)

    try:
        if op == 'addi':
            rd, rs, imm = args
            # Garante que o imediato é tratado como um inteiro, pode ser negativo
            val = registradores.ler(rs) + int(imm)
            registradores.escrever(rd, val)
            return pc + 1, tipo_inst # Retorna o tipo
        
        elif op == 'add':
            rd, rs, rt = args
            val = registradores.ler(rs) + registradores.ler(rt)
            registradores.escrever(rd, val)
            return pc + 1, tipo_inst # Retorna o tipo

        elif op == 'sub':
            rd, rs, rt = args
            val = registradores.ler(rs) - registradores.ler(rt)
            registradores.escrever(rd, val)
            return pc + 1, tipo_inst # Retorna o tipo

        elif op == 'beq':
            rs, rt, offset = args
            if registradores.ler(rs) == registradores.ler(rt):
                # O offset para beq é em número de instruções
                return pc + 1 + int(offset), tipo_inst # Retorna o tipo
            return pc + 1, tipo_inst # Retorna o tipo

        elif op == 'j':
            target = int(args[0])
            return target, tipo_inst # Retorna o tipo

        elif op == 'lw': # Load Word
            rt, offset_base = args
            offset, base_reg = parse_offset_base(offset_base)
            endereco_base = registradores.ler(base_reg)
            endereco_final = endereco_base + offset
            
            valor_lido = memoria.ler(endereco_final)
            registradores.escrever(rt, valor_lido)
            return pc + 1, tipo_inst # Retorna o tipo

        elif op == 'sw': # Store Word
            rt, offset_base = args
            offset, base_reg = parse_offset_base(offset_base)
            endereco_base = registradores.ler(base_reg)
            endereco_final = endereco_base + offset
            
            valor_a_escrever = registradores.ler(rt)
            memoria.escrever(endereco_final, valor_a_escrever)
            return pc + 1, tipo_inst # Retorna o tipo

        elif op == 'syscall': # Implementação da syscall
            # O código da syscall é geralmente armazenado em $v0
            syscall_code = registradores.ler('$v0')
            
            if syscall_code == 10: # Syscall para 'exit'
                print("\nPrograma terminado pela syscall (exit).")
                # No simulador, podemos parar a execução definindo pc para um valor fora do limite
                return -1, tipo_inst # Um valor negativo fará o loop principal parar
            # Adicione outras syscalls aqui conforme necessário (e.g., print int, read int)
            # elif syscall_code == 1: # print_int
            #     print(f"SYSCALL (print_int): {registradores.ler('$a0')}")
            #     return pc + 1, tipo_inst
            else:
                print(f"Aviso: Syscall code {syscall_code} não implementado. Continuando...")
                return pc + 1, tipo_inst

        else:
            print(f"Instrução não implementada: {op}")
            return pc + 1, 'Desconhecido' # Retorna 'Desconhecido'

    except Exception as e:
        print(f"Erro executando {instrucao.opcode} {instrucao.operandos}: {e}")
        return pc + 1, 'Erro' # Retorna 'Erro' em caso de exceção