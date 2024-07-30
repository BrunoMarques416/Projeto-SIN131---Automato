from afd import AutomatoFinitoDeterministico,criar_afd,imprimir_afd
from afn import AutomatoFinitoNaoDeterministico,criar_afn,imprimir_afn
from funcoes import converter_afn_para_afd,simular_afd,simular_afn,demonstrar_equivalencia,minimizar_afd

def main():
    
    afn = None
    afd = None

    while True:
        print("Menu:")
        print("1. Criar AFD")
        print("2. Criar AFN")
        print("3. Converter AFN para AFD")
        print("4. Demonstrar a equivalência entre AFN e AFD")
        print("5. Minimizar AFD")
        print("6. Simular AFD")
        print("7. Simular AFN")
        print("8. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            afd = criar_afd()
            imprimir_afd(afd)
        elif escolha == "2":
            afn = criar_afn()
            imprimir_afn(afn)
        elif escolha == "3":
            if afn:
                afd = converter_afn_para_afd(afn)
                imprimir_afd(afd)
            else:
                print("Você precisa criar um AFN primeiro.")
        elif escolha == "4":
            if afn and afd:
                palavras = input("Digite palavras para testar, separadas por espaço: ").split()
                demonstrar_equivalencia(afn, afd, palavras)
            else:
                print("Você precisa criar um AFN e um AFD primeiro.")
        elif escolha == "5":
            if afd:
                afd_minimizado = minimizar_afd(afd)
                imprimir_afd(afd_minimizado)
            else:
                print("Você precisa criar um AFD primeiro.")
        elif escolha == '6':
            if afd:
                palavra = input("Digite a palavra a ser simulada: ")
                if simular_afd(afd, palavra):
                    print(f"A palavra '{palavra}' foi aceita pelo AFD.")
                else:
                    print(f"A palavra '{palavra}' foi rejeitada pelo AFD.")
            else:
                print("AFD não criado.")
        elif escolha == "7":
            if afn:
                palavra = input("Digite a palavra a ser simulada: ")
                if simular_afn(afn, palavra):
                    print(f"A palavra '{palavra}' foi aceita pelo AFN.")
                else:
                    print(f"A palavra '{palavra}' foi rejeitada pelo AFN.")
            else:
                print("AFN não criado.")
        elif escolha == "8":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()