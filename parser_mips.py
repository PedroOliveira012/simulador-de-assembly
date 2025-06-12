# class Instrução:
#     def __init__(self, opcode, operandos, linha_original):
#         self.opcode = opcode
#         self.operandos = operandos
#         self.linha_original = linha_original

#     def __repr__(self):
#         return f"{self.opcode.upper()} {', '.join(self.operandos)}"

# def limpar_linha(linha):
#     linha = linha.split('#')[0]
#     return linha.strip()

# def parse_linha(linha):
#     limpa = limpar_linha(linha)
#     if not limpa:
#         return None
#     partes = limpa.replace(',', ' ').split()
#     opcode = partes[0].lower()
#     operandos = partes[1:]
#     return Instrução(opcode, operandos, linha)

# def carregar_codigo(caminho_arquivo):
#     instrucoes = []
#     with open(caminho_arquivo, 'r') as f:
#         for linha in f:
#             instrucao = parse_linha(linha)
#             if instrucao:
#                 instrucoes.append(instrucao)
#     return instrucoes

class Instrução:
    def __init__(self, opcode, operandos, linha_original):
        self.opcode = opcode
        self.operandos = operandos
        self.linha_original = linha_original

    def __repr__(self):
        # Garante que os operandos são unidos corretamente com vírgulas
        # Para li expandido para addi, o __repr__ do addi será usado no cpu
        # Mas para o parser_mips, mantém a representação original se for o caso
        if self.opcode == 'li' and len(self.operandos) == 2:
            return f"LI {self.operandos[0].upper()}, {self.operandos[1]}"
        return f"{self.opcode.upper()} {', '.join(self.operandos)}"

def limpar_linha(linha):
    # Remove comentários e espaços em branco
    linha = linha.split('#')[0]
    return linha.strip()

def parse_linha(linha):
    limpa = limpar_linha(linha)
    if not limpa:
        return None

    # Verifica se é uma diretiva (começa com '.') ou um rótulo (termina com ':')
    if limpa.startswith('.') or limpa.endswith(':'):
        return None # Ignora diretivas e rótulos para fins de execução de instrução

    # Substitui vírgulas por espaços para facilitar o split
    partes = limpa.replace(',', ' ').split()
    
    if not partes: # Linha vazia após limpar e dividir
        return None

    opcode = partes[0].lower() # Converte o opcode para minúsculas
    operandos = partes[1:]

    # --- Expansão da pseudo-instrução LI ---
    if opcode == 'li':
        if len(operandos) == 2:
            reg_destino = operandos[0]
            valor_imediato = operandos[1]
            # Converte 'li $t0, 5' para 'addi $t0, $zero, 5'
            # Criamos uma nova Instrução para 'addi'
            return Instrução('addi', [reg_destino, '$zero', valor_imediato], linha)
        else:
            print(f"Aviso: Formato inválido para 'li': {linha.strip()}. Ignorando.")
            return None

    return Instrução(opcode, operandos, linha)

def carregar_codigo(caminho_arquivo):
    instrucoes = []
    try:
        with open(caminho_arquivo, 'r') as f:
            for linha in f:
                # O parse_linha agora já lida com diretivas, rótulos e li
                instrucao = parse_linha(linha)
                if instrucao: # Apenas adiciona se for uma instrução válida e não ignorada
                    instrucoes.append(instrucao)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo '{caminho_arquivo}': {e}")
        return []
    return instrucoes