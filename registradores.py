class Registradores:
    def __init__(self):
        self.regs = {
            '$zero': 0, '$at': 0, '$v0': 0, '$v1': 0,
            '$a0': 0, '$a1': 0, '$a2': 0, '$a3': 0,
            '$t0': 0, '$t1': 0, '$t2': 0, '$t3': 0,
            '$t4': 0, '$t5': 0, '$t6': 0, '$t7': 0,
            '$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0,
            '$s4': 0, '$s5': 0, '$s6': 0, '$s7': 0,
            '$t8': 0, '$t9': 0, '$k0': 0, '$k1': 0,
            '$gp': 0, '$sp': 0, '$fp': 0, '$ra': 0
        }

    def ler(self, nome):
        return self.regs.get(nome, 0)

    def escrever(self, nome, valor):
        if nome != '$zero':
            # Garante que o valor se encaixe em 32 bits (unsigned)
            self.regs[nome] = valor & 0xFFFFFFFF

    def mostrar(self):
        print("\n--- Registradores ---")
        # Definindo uma ordem lógica para a exibição dos registradores
        ordem_registradores = [
            # Registradores especiais
            '$zero', '$at', '$gp', '$sp',
            '$fp', '$ra',
            # Valores de retorno e argumentos
            '$v0', '$v1', '$a0', '$a1',
            '$a2', '$a3',
            # Temporários
            '$t0', '$t1', '$t2', '$t3',
            '$t4', '$t5', '$t6', '$t7',
            '$t8', '$t9',
            # Salvos
            '$s0', '$s1', '$s2', '$s3',
            '$s4', '$s5', '$s6', '$s7',
            # Kernel
            '$k0', '$k1'
        ]
        
        # Exibir em linhas de 4 registradores
        for i in range(0, len(ordem_registradores), 4):
            linha_regs = ordem_registradores[i:i+4]
            partes_linha = []
            for reg_nome in linha_regs:
                val = self.regs.get(reg_nome, 0)
                # Formatar o valor em hexadecimal com 8 dígitos e em decimal
                partes_linha.append(f"{reg_nome}: 0x{val:08x} ({val:10})")
            print("  ".join(partes_linha))