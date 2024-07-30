from afd import AutomatoFinitoDeterministico
from afn import AutomatoFinitoNaoDeterministico

def converter_afn_para_afd(afn):
    # Inicializa os novos estados, começando com o estado inicial do AFN.
    novos_estados = []
    novas_transicoes = {}
    
    # O estado inicial do AFD é o conjunto contendo apenas o estado inicial do AFN.
    estado_inicial = frozenset([afn.estado_inicial])
    novos_estados.append(estado_inicial)
    novas_transicoes[estado_inicial] = {}
    
    # Lista de estados a serem processados.
    processar_estados = [estado_inicial]
    
    # Conjunto para armazenar os estados finais do AFD.
    estados_finais = set()
    
    # Processa todos os estados até que não haja mais estados a serem processados.
    while processar_estados:
        estado_atual = processar_estados.pop()
        novas_transicoes[estado_atual] = {}
        
        # Para cada símbolo no alfabeto do AFN, calcula os novos estados alcançáveis.
        for simbolo in afn.alfabeto:
            novos_estados_atuais = set()
            for subestado in estado_atual:
                if subestado in afn.transicoes and simbolo in afn.transicoes[subestado]:
                    novos_estados_atuais.update(afn.transicoes[subestado][simbolo])
            
            # Converte os novos estados alcançáveis em um conjunto imutável (frozenset).
            novos_estados_atuais = frozenset(novos_estados_atuais)
            
            if novos_estados_atuais:
                # Atualiza as transições para o estado atual.
                novas_transicoes[estado_atual][simbolo] = novos_estados_atuais
                
                # Se os novos estados não foram processados anteriormente, adiciona-os à lista.
                if novos_estados_atuais not in novos_estados:
                    novos_estados.append(novos_estados_atuais)
                    processar_estados.append(novos_estados_atuais)
                
                # Se qualquer um dos novos estados é um estado final no AFN, adiciona ao conjunto de estados finais do AFD.
                if novos_estados_atuais & set(afn.estados_finais):
                    estados_finais.add(novos_estados_atuais)
    
    
    return AutomatoFinitoDeterministico(
        estados=novos_estados,
        alfabeto=afn.alfabeto,
        transicoes=novas_transicoes,
        estado_inicial=estado_inicial,
        estados_finais=estados_finais
    )


def simular_afn(afn, palavra):
    estados_atuais = {afn.estado_inicial}
    for simbolo in palavra:
        novos_estados = set()
        for estado in estados_atuais:
            if estado in afn.transicoes and simbolo in afn.transicoes[estado]:
                novos_estados.update(afn.transicoes[estado][simbolo])
        estados_atuais = novos_estados
    return bool(estados_atuais & set(afn.estados_finais))


def simular_afd(afd, palavra):
    estado_atual = afd.estado_inicial
    for simbolo in palavra:
        if estado_atual in afd.transicoes and simbolo in afd.transicoes[estado_atual]:
            estado_atual = afd.transicoes[estado_atual][simbolo]
        else:
            return False
    return estado_atual in afd.estados_finais


def demonstrar_equivalencia(afn, afd, palavras):
    for palavra in palavras:
        aceito_afn = simular_afn(afn, palavra)
        aceito_afd = simular_afd(afd, palavra)
        print(f"Palavra: {palavra}")
        print(f"  Aceito pelo AFN: {aceito_afn}")
        print(f"  Aceito pelo AFD: {aceito_afd}")
        print(f"  Equivalente: {aceito_afn == aceito_afd}")
        print()


def minimizar_afd(afd):
    # Inicializa a lista P com dois conjuntos: estados finais e não finais.
    P = [afd.estados_finais, set(afd.estados) - set(afd.estados_finais)]
    
    # Inicializa a lista W com os estados finais.
    W = [afd.estados_finais]

    # Loop até que não haja mais partições em W para processar.
    while W:
        # Retira o próximo conjunto de estados a ser processado.
        A = W.pop()

        # Para cada símbolo no alfabeto do AFD.
        for simbolo in afd.alfabeto:
            # Inicializa um conjunto vazio X para estados que transitam para A com o símbolo.
            X = set()
            
            # Para cada estado no AFD.
            for estado in afd.estados:
                # Se há uma transição do estado com o símbolo que leva a um estado em A.
                if simbolo in afd.transicoes.get(estado, {}) and afd.transicoes[estado][simbolo] in A:
                    # Adiciona o estado ao conjunto X.
                    X.add(estado)

            # Itera sobre uma cópia de P, pois P pode ser modificado dentro do loop.
            for Y in P[:]:
                # Calcula a interseção de X e Y, e a diferença entre Y e X.
                interseccao = X & Y
                diferenca = Y - X
                
                # Se a interseção e a diferença não são vazias, divide Y em dois conjuntos.
                if interseccao and diferenca:
                    # Remove Y de P.
                    P.remove(Y)
                    # Adiciona as novas partições interseccao e diferenca a P.
                    P.append(interseccao)
                    P.append(diferenca)
                    
                    # Atualiza W de acordo com as novas partições.
                    if Y in W:
                        W.remove(Y)
                        W.append(interseccao)
                        W.append(diferenca)
                    else:
                        # Adiciona a menor das novas partições a W.
                        if len(interseccao) <= len(diferenca):
                            W.append(interseccao)
                        else:
                            W.append(diferenca)

    # Converte as partições em estados do novo AFD.
    novos_estados = {frozenset(particao) for particao in P}
    
    # Determina o novo estado inicial, procurando a partição que contém o estado inicial do AFD original.
    novo_estado_inicial = next(particao for particao in novos_estados if afd.estado_inicial in particao)
    
    # Determina os novos estados finais, procurando partições que contêm qualquer estado final do AFD original.
    novos_estados_finais = {particao for particao in novos_estados if particao & afd.estados_finais}

    # Inicializa o dicionário de novas transições para o AFD minimizado.
    novas_transicoes = {}
    
    # Para cada partição nos novos estados.
    for particao in novos_estados:
        # Escolhe um estado representante da partição.
        estado_representante = next(iter(particao))
        novas_transicoes[particao] = {}
        
        # Para cada símbolo no alfabeto do AFD original.
        for simbolo in afd.alfabeto:
            # Se há uma transição a partir do estado representante com o símbolo.
            if simbolo in afd.transicoes[estado_representante]:
                # Determina o estado destino.
                estado_destino = afd.transicoes[estado_representante][simbolo]
                
                # Encontra a partição destino que contém o estado destino.
                for destino in novos_estados:
                    if estado_destino in destino:
                        # Adiciona a transição ao dicionário de novas transições.
                        novas_transicoes[particao][simbolo] = destino
                        break

    # Retorna o novo AFD minimizado com os estados, alfabeto, transições, estado inicial e estados finais.
    return AutomatoFinitoDeterministico(
        estados=novos_estados,
        alfabeto=afd.alfabeto,
        transicoes=novas_transicoes,
        estado_inicial=novo_estado_inicial,
        estados_finais=novos_estados_finais
    )