# memoria.py

class Memoria:
    def __init__(self):
        # Representa a memória como um dicionário: endereço -> valor
        self.mem = {}  # Exemplo: {1000: 42, 1004: 7}

    def ler(self, endereco):
        """
        Lê o valor da memória no endereço especificado.
        Se o endereço não estiver na memória, retorna 0.
        """
        return self.mem.get(endereco, 0)

    def escrever(self, endereco, valor):
        """
        Escreve um valor em um endereço da memória.
        """
        self.mem[endereco] = valor

    def mostrar(self):
        """
        Mostra todo o conteúdo atual da memória em ordem de endereço.
        """
        print("\n--- Estado da Memória ---")
        if not self.mem:
            print("(memória vazia)")
        for endereco in sorted(self.mem.keys()):
            print(f"Endereço {endereco}: {self.mem[endereco]}")
