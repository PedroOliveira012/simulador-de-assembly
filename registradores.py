# registradores.py

class Registradores:
    def __init__(self):
        # Registradores MIPS (apenas os principais para começar)
        self.regs = {
            '$zero': 0,  # constante 0
            '$t0': 0, '$t1': 0, '$t2': 0, '$t3': 0, '$t4': 0,
            '$t5': 0, '$t6': 0, '$t7': 0,
            '$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0, '$s4': 0,
            '$s5': 0, '$s6': 0, '$s7': 0
        }

    def ler(self, nome):
        return self.regs.get(nome, 0)

    def escrever(self, nome, valor):
        if nome != '$zero':  # $zero não pode ser modificado
            self.regs[nome] = valor

    def mostrar(self):
        for reg, val in self.regs.items():
            print(f"{reg}: {val}")
