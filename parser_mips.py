# parser_mips.py

class Instrução:
    def __init__(self, opcode, operandos, linha_original):
        self.opcode = opcode
        self.operandos = operandos
        self.linha_original = linha_original

    def __repr__(self):
        return f"{self.opcode.upper()} {', '.join(self.operandos)}"

def limpar_linha(linha):
    linha = linha.split('#')[0]  # Remove comentários
    return linha.strip()

def parse_linha(linha):
    limpa = limpar_linha(linha)
    if not limpa:
        return None

    partes = limpa.replace(',', ' ').split()
    opcode = partes[0].lower()
    operandos = partes[1:]
    return Instrução(opcode, operandos, linha)

def carregar_codigo(caminho_arquivo):
    instrucoes = []
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            instrucao = parse_linha(linha)
            if instrucao:
                instrucoes.append(instrucao)
    return instrucoes
