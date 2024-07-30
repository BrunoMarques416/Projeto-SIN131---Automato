class AutomatoFinitoNaoDeterministico:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais


def criar_afn():
    estados = sorted(set(input("Digite os estados separados por espaço: ").split()))
    alfabeto = sorted(set(input("Digite o alfabeto separado por espaço: ").split()))
    transicoes = {}
    for estado in estados:
        transicoes[estado] = {}
    for estado in estados:
        print(f"Definindo transições para o estado {estado}:")
        for simbolo in alfabeto:
            destinos = set(input(f"  Destinos para a transição {estado} --{simbolo}--> (separe por espaço, deixe em branco para nenhum): ").split())
            if destinos:
                transicoes[estado][simbolo] = destinos

    estado_inicial = input("Digite o estado inicial: ")
    estados_finais = sorted(set(input("Digite os estados finais separados por espaço: ").split()))

    return AutomatoFinitoNaoDeterministico(
        estados=estados,
        alfabeto=alfabeto,
        transicoes=transicoes,
        estado_inicial=estado_inicial,
        estados_finais=estados_finais
    )


def imprimir_afn(afn):
    print("AFN:")
    print("Estados:", afn.estados)
    print("Alfabeto:", afn.alfabeto)
    print("Transições:")
    for estado, transicoes in afn.transicoes.items():
        for simbolo, destinos in transicoes.items():
            print(f"  {estado} --{simbolo}--> {destinos}")
    print("Estado Inicial:", afn.estado_inicial)
    print("Estados Finais:", afn.estados_finais)
    print()
