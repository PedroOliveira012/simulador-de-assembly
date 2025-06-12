# class Memoria:
#     def __init__(self):
#         self.mem = {}

#     def ler(self, endereco):
#         return self.mem.get(endereco & 0xFFFFFFFC, 0)

#     def escrever(self, endereco, valor):
#         self.mem[endereco & 0xFFFFFFFC] = valor & 0xFFFFFFFF

#     def mostrar(self):
#         print("\n--- Memória ---")
#         if not self.mem:
#             print("(vazia)")
#         for addr in sorted(self.mem.keys()):
#             print(f"[0x{addr:08x}]: 0x{self.mem[addr]:08x}")

class Memoria:
    def __init__(self):
        self.mem = {}

    def ler(self, endereco):
        # Garante alinhamento de 4 bytes e retorna 0 se o endereço não estiver mapeado
        return self.mem.get(endereco & 0xFFFFFFFC, 0)

    def escrever(self, endereco, valor):
        # Garante alinhamento de 4 bytes e armazena o valor como 32 bits unsigned
        self.mem[endereco & 0xFFFFFFFC] = valor & 0xFFFFFFFF

    def mostrar(self):
        print("\n--- Memória ---")
        if not self.mem:
            print("(vazia)")
        else:
            # Ordena os endereços para exibição consistente
            for addr in sorted(self.mem.keys()):
                print(f"[0x{addr:08x}]: 0x{self.mem[addr]:08x}")