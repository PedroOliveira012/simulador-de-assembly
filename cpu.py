# cpu.py

def executar_instrucao(instrucao, registradores, memoria, pc):
    op = instrucao.opcode
    args = instrucao.operandos

    if op == 'addi':
        rd, rs, imediato = args
        val = registradores.ler(rs)
        registradores.escrever(rd, val + int(imediato))
        pc += 1

    elif op == 'add':
        rd, rs, rt = args
        val = registradores.ler(rs) + registradores.ler(rt)
        registradores.escrever(rd, val)
        pc += 1

    elif op == 'sub':
        rd, rs, rt = args
        val = registradores.ler(rs) - registradores.ler(rt)
        registradores.escrever(rd, val)
        pc += 1

    elif op == 'beq':
        rs, rt, offset = args
        if registradores.ler(rs) == registradores.ler(rt):
            pc += int(offset)
        else:
            pc += 1

    elif op == 'j':
        target = int(args[0])
        pc = target

    else:
        print(f"Instrução não implementada: {op}")
        pc += 1

    return pc
