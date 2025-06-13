# Simulador MIPS

Este é um simulador básico de arquitetura MIPS, desenvolvido em Python. Ele é capaz de carregar e executar programas escritos em um subconjunto da linguagem Assembly MIPS, simulando o comportamento de uma CPU, registradores e memória.

## Funcionalidades

* **Execução de Instruções MIPS:** Suporta as seguintes instruções:
    * **Tipo R:** `add`, `sub`, `mul`, `and`, `or`
    * **Tipo I:** `addi`, `lw`, `sw`, `lb`, `sb`, `beq`
    * **Tipo J:** `j`
    * **Pseudoinstrução:** `li` (convertida internamente para `addi`)
    * **Instrução de Sistema:** `syscall` (com suporte básico para `exit` - código 10)
* **Simulação de Registradores:** Gerencia 32 registradores MIPS, com valores atualizados a cada ciclo.
* **Simulação de Memória:** Permite operações de leitura (`lw`, `lb`) e escrita (`sw`, `sb`) na memória, com suporte a manipulação byte a byte e agrupamento por palavras.
* **Modo de Execução:** Suporta execução contínua ou passo a passo (instrução por instrução).
* **Geração de Código de Máquina:** Converte instruções Assembly MIPS para suas representações binária e hexadecimal.
* **Estatísticas de Execução:** Contabiliza o total de instruções executadas, ciclos consumidos e tempo total estimado da simulação, com cálculo baseado na frequência do clock.

## Arquitetura e Componentes

O simulador é estruturado em módulos claros, cada um com uma responsabilidade específica:

* **Parser (`parser_mips.py`):** Responsável por interpretar o código MIPS, identificando instruções e seus operandos. Lida com a limpeza das linhas e a conversão de pseudoinstruções como `li` para suas equivalentes MIPS.
* **Assembler (`assembler_mips.py`):** Converte as instruções MIPS (objetos `Instrucao`) em suas representações binárias e hexadecimais, suportando os formatos R, I e J.
* **CPU (`cpu.py`):** Atua como o componente central do simulador, controlando o fluxo do programa (PC), gerenciando o estado dos registradores e da memória. É responsável por decodificar o tipo de instrução e executar a operação correspondente.
* **Registradores (`registradores.py`):** Abstração que simula o banco de registradores da CPU MIPS, permitindo operações de leitura e escrita de valores nos registradores.
* **Memória (`memory.py`):** Simula a memória de dados do sistema, permitindo leitura e escrita de bytes e palavras completas. Apresenta o estado da memória em formato hexadecimal para visualização.
* **Utils (`utils.py`):** Módulo com funções utilitárias que auxiliam na conversão de formatos (inteiro para binário/hexadecimal) e no parsing de argumentos complexos (como offset para instruções de memória).
* **Totalizador (integrado em `main.py`):** O simulador mantém um controlador global que contabiliza o total de instruções executadas, ciclos consumidos por tipo de instrução e o tempo total estimado da simulação, com base na frequência do clock configurada.

## Métodos Principais

A seguir, alguns dos métodos chave que orquestram o funcionamento do simulador:

* **`assemble_instrucao` (em `assembler_mips.py`):** Converte uma instrução MIPS textual e seus operandos para sua representação binária, suportando os formatos R, I e J. Auxiliares internos (`REGISTRADORES_MAP`, `OPCODES`, `FUNCT_CODES`) fornecem os códigos opcode e função (funct) necessários para montar a instrução binária.
* **`executar_instrucao` (em `cpu.py`):** Centraliza a lógica de execução de cada instrução MIPS, atualizando o PC e o estado dos registradores e da memória conforme a operação.
* **`ler`/`escrever` (em `memory.py`):** Implementam a leitura e escrita simulada de dados na memória.
* **`ler`/`escrever` (em `registradores.py`):** Métodos para acessar e modificar os valores armazenados nos registradores.
* **Cálculo de Tempo e Ciclos (em `main.py`):** Os métodos `mostrar_estatisticas` calculam o tempo consumido pela simulação com base na frequência do clock (`CPU_CLOCK_HZ`) e no total de ciclos (`ciclos_totais`). Os ciclos por tipo de instrução são definidos e usados para essa contabilização.

## Requisitos

Para rodar este simulador, você precisa ter:

* **Python 3.x** instalado.

## Como Usar

1.  **Salve os arquivos:** Certifique-se de que todos os arquivos (`main.py`, `assembler_mips.py`, `cpu.py`, `memory.py`, `parser_mips.py`, `registradores.py`, `utils.py`) estejam no mesmo diretório.

2.  **Crie seu programa Assembly MIPS:** Escreva ou deixe seu código MIPS em um arquivo `.asm` no mesmo diretório do simulador. Por exemplo, crie um arquivo chamado `meu_programa.asm`:

3.  **Execute o simulador:** Abra o terminal na pasta onde os arquivos estão salvos e execute o comando:

    ```bash
    python main.py meu_programa.asm
    ```

    Para executar em **modo passo a passo**, adicione `--step`:

    ```bash
    python main.py meu_programa.asm --step
    ```

    No modo passo a passo, a execução pausará após cada instrução e você precisará pressionar `Enter` para continuar.

## Pontos Importantes

* **Subconjunto MIPS:** Este simulador implementa um subconjunto específico de instruções MIPS. Nem todas as instruções da arquitetura MIPS completa são suportadas.
* **Tratamento de Erros Básico:** O simulador tenta lidar com algumas condições de erro (ex: registradores ou offsets inválidos), retornando valores padrão (`0` ou `0x00000000`) para evitar falhas.
* **Controle Rigoroso do PC:** O `program counter` (PC) é rigorosamente controlado, com suporte a desvios (`beq`) e saltos (`j`), respeitando os efeitos de cada instrução no fluxo do programa.
* **Implementação Detalhada da Memória:** A memória permite manipulação byte a byte (`lb`, `sb`) e agrupamento por palavras (`lw`, `sw`), com visualização clara do estado em formato hexadecimal.
* **Contabilização Precisa:** Há uma contabilização precisa dos ciclos de clock por instrução e o cálculo estimado do tempo total de execução baseado na frequência do clock configurada.
* **Uso de Dicionários:** Coleções e dicionários são amplamente utilizados para manter registradores, opcodes, e o conteúdo da memória, garantindo eficiência e clareza no acesso aos dados.
* **Complemento de Dois:** A conversão de valores imediatos e offsets para binário utiliza o complemento de dois para números negativos, garantindo a correção para valores de 16 bits.