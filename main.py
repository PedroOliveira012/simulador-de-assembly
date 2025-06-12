# from parser_mips import carregar_codigo
# from registradores import Registradores
# from memoria import Memoria
# from cpu import executar_instrucao
# import sys

# class SimuladorMIPS:
#     def __init__(self):
#         self.registradores = Registradores()
#         self.memoria = Memoria()
#         self.pc = 0
#         self.instrucoes = []

#     def carregar_programa(self, arquivo):
#         try:
#             self.instrucoes = carregar_codigo(arquivo)
#             print(f"Programa carregado com {len(self.instrucoes)} instruções")
#             return True
#         except Exception as e:
#             print(f"Erro ao carregar programa: {e}")
#             return False

#     def executar(self, passo_a_passo=False):
#         if not self.instrucoes:
#             print("Nenhum programa carregado!")
#             return

#         print("\nIniciando execução...")
#         while 0 <= self.pc < len(self.instrucoes):
#             instrucao = self.instrucoes[self.pc]
#             print(f"\n[PC={self.pc}] Executando: {instrucao}")
            
#             self.pc = executar_instrucao(instrucao, self.registradores, self.memoria, self.pc)
            
#             self.registradores.mostrar()
#             self.memoria.mostrar()
            
#             if passo_a_passo:
#                 input("\nPressione Enter para continuar...")

#         print("\nExecução concluída!")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Uso: python main.py <arquivo.asm> [--step]")
#         sys.exit(1)

#     arquivo_asm = sys.argv[1]
#     passo_a_passo = len(sys.argv) > 2 and sys.argv[2] == "--step"

#     simulador = SimuladorMIPS()
    
#     if simulador.carregar_programa(arquivo_asm):
#         simulador.executar(passo_a_passo)

from parser_mips import carregar_codigo
from registradores import Registradores
from memoria import Memoria
from cpu import executar_instrucao, obter_tipo_instrucao
from assembler_mips import assemble_instrucao
import sys

class SimuladorMIPS:
    def __init__(self):
        self.registradores = Registradores()
        self.memoria = Memoria()
        self.pc = 0
        self.instrucoes = []
        self.ciclos_totais = 0
        # Adiciona 'SYSCALL' ao dicionário de contagem de instruções por tipo
        self.contagem_instrucoes_por_tipo = {'R': 0, 'I': 0, 'J': 0, 'SYSCALL': 0, 'Desconhecido': 0, 'Erro': 0}
        self.iteracao_atual = 0

        self.CPU_CLOCK_HZ = 100_000_000
        self.CICLOS_POR_TIPO = {
            'R': 4,
            'I': 5,
            'J': 3,
            'SYSCALL': 10 # Um valor de exemplo para o custo de uma syscall
        }

    def carregar_programa(self, arquivo):
        try:
            self.instrucoes = carregar_codigo(arquivo)
            print(f"Programa carregado com {len(self.instrucoes)} instruções")
            return True
        except Exception as e:
            print(f"Erro ao carregar programa: {e}")
            return False

    def executar(self, passo_a_passo=False):
        if not self.instrucoes:
            print("Nenhum programa carregado!")
            return

        print("\nIniciando execução...")
        self.ciclos_totais = 0
        # Resetar ao iniciar a execução, incluindo 'SYSCALL'
        self.contagem_instrucoes_por_tipo = {'R': 0, 'I': 0, 'J': 0, 'SYSCALL': 0, 'Desconhecido': 0, 'Erro': 0}
        self.iteracao_atual = 0

        while 0 <= self.pc < len(self.instrucoes):
            self.iteracao_atual += 1
            instrucao = self.instrucoes[self.pc]
            
            # Converte a instrução para binário e hexadecimal
            binario_inst, hex_inst = assemble_instrucao(instrucao)

            print(f"\n======== Iteração {self.iteracao_atual} (PC: {self.pc}) ========")
            print(f"  Instrução Assembly: {instrucao}")
            print(f"  Instrução Binária: {binario_inst}")
            print(f"  Instrução Hexadecimal: {hex_inst}")
            
            proximo_pc, tipo_inst = executar_instrucao(instrucao, self.registradores, self.memoria, self.pc)
            
            self.pc = proximo_pc
            
            custo_ciclos = self.CICLOS_POR_TIPO.get(tipo_inst, 0)
            self.ciclos_totais += custo_ciclos
            self.contagem_instrucoes_por_tipo[tipo_inst] += 1
            
            self.registradores.mostrar()
            self.memoria.mostrar()
            
            if passo_a_passo:
                input("\nPressione Enter para continuar...")
            
            # Se a syscall de exit foi chamada, o PC será -1, então saímos do loop
            if self.pc == -1:
                break

        print("\nExecução concluída!")
        self.mostrar_estatisticas()

    def mostrar_estatisticas(self):
        print("\n--- Estatísticas Finais de Execução ---")
        print(f"Total de Iterações de Instrução: {self.iteracao_atual}")
        print(f"Total de Ciclos de Clock: {self.ciclos_totais}")
        print(f"Frequência do Clock da CPU: {self.CPU_CLOCK_HZ / 1_000_000:.2f} MHz")
        
        if self.CPU_CLOCK_HZ > 0:
            tempo_total_segundos = self.ciclos_totais / self.CPU_CLOCK_HZ
            print(f"Tempo Total de Execução: {tempo_total_segundos:.9f} segundos")
        else:
            print("Frequência do Clock da CPU não definida ou zero, não é possível calcular o tempo.")
            
        print("\nContagem de Instruções por Tipo:")
        for tipo, count in self.contagem_instrucoes_por_tipo.items():
            print(f"  Tipo {tipo}: {count} instruções")
        
        # O total agora inclui o tipo 'SYSCALL'
        total_instrucoes_executadas = sum(self.contagem_instrucoes_por_tipo[t] for t in ['R', 'I', 'J', 'SYSCALL'])
        print(f"  Total de Instruções Executadas: {total_instrucoes_executadas}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.asm> [--step]")
        sys.exit(1)

    arquivo_asm = sys.argv[1]
    passo_a_passo = len(sys.argv) > 2 and sys.argv[2] == "--step"

    simulador = SimuladorMIPS()
    
    if simulador.carregar_programa(arquivo_asm):
        simulador.executar(passo_a_passo)