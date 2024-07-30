class AutomatoFinitoDeterministico:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais


def criar_afd():
    estados = sorted(set(input("Digite os estados separados por espaço: ").split()))
    alfabeto = sorted(set(input("Digite o alfabeto separado por espaço: ").split()))
    transicoes = {}

    ''' exemplo de transição
    transicoes={
        'q0': {'a': {'q0', 'q1'}, 'b': {'q0'}},
        'q1': {'a': {'q2'}},
        'q2': {'b': {'q2'}}
    },'''

    for estado in estados:
        transicoes[estado] = {}
    for estado in estados:
        print(f"Definindo transições para o estado {estado}:")
        for simbolo in alfabeto:
            destino = input(f"  Destino para a transição {estado} --{simbolo}--> (deixe em branco para nenhum): ")
            if destino:
                transicoes[estado][simbolo] = destino

    estado_inicial = input("Digite o estado inicial: ")
    estados_finais = sorted(set(input("Digite os estados finais separados por espaço: ").split()))

    return AutomatoFinitoDeterministico(
        estados=estados,
        alfabeto=alfabeto,
        transicoes=transicoes,
        estado_inicial=estado_inicial,
        estados_finais=estados_finais
    )


def imprimir_afd(afd):
    print("AFD:")
    print("Estados:", [list(s) for s in afd.estados])
    print("Alfabeto:", afd.alfabeto)
    print("Transições:")
    for estado in afd.transicoes:
        for simbolo in afd.transicoes[estado]:
            print(f"  {list(estado)} --{simbolo}--> {list(afd.transicoes[estado][simbolo])}")
    print("Estado Inicial:", list(afd.estado_inicial))
    print("Estados Finais:", [list(s) for s in afd.estados_finais])
    print()