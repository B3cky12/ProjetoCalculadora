def parse_nele(expressao: str):
    # A estrutura com a expressão decodificada, organizada na ordem de resolução
    parsed = []
    
    for index, char in enumerate(expressao):
        # Primeira regra do PEMDAS: Parênteses
        if char == "(":
            start = index +1
            end = expressao.index(")")
            parenteses = expressao[start:end] # O que tiver dentro dos '(' e ')' selecionados
            parte = parse_nele(parenteses) # Se tiver parenteses aninhados, aqui é resolvido, se não, segue normal
            parsed.append(parte)
        elif index == -1:
            continue
    
    for index, char in enumerate(expressao):
        # Segunda regra do PEMDAS: Expoentes
        if char == "^":
            # pensamento: loop reverso iniciado no ^, pra achar index que começa o bloco do número que é a base da potenciação; depois loop com direção normal pra encontrar o index que termina o bloco de número que é o expoente;
            # pergunta: é válido chamar parse_nele em ambas a base e o expoente?
    
    return parsed