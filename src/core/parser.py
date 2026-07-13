#testando o que aprendi
class ParseError(Exception):
    def __init__(self, pos, msg, *args):
        self.pos = pos # posição do texto
        self.msg = msg
        self.args = args
    
    def __str__(self):
        return '%s at position %s' % (self.msg % self.args, self.pos)


# quanto mais eu leio sobre parsers, mais eu penso que esse código não vai ser a versão final, mas o exercício mental é válido por hora
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
            # possível teste para avaliar necessidade desse elif
            continue
    
    for index, char in enumerate(expressao):
        # Segunda regra do PEMDAS: Expoentes
        if char == "^":
            # pensamento: loop reverso iniciado no ^, pra achar index que começa o bloco do número que é a base da potenciação; depois loop com direção normal pra encontrar o index que termina o bloco de número que é o expoente;
            
            last = 0
            for i, x in range(enumerate(expressao)[index-1], 0, -1):
                now = {i: x}
                if type(x) is int:
                    last = {i: x}
                    continue
                else:
                    break
            base = expressao[last[i]:index-1]
            parte1 = parse_nele(base)
            
            last = 0
            for i, x in range(enumerate(expressao)[index+1]):
                now = {i: x}
                if type(x) is int:
                    last = {i: x}
                    continue
                else:
                    break
            expo = expressao[index+1:last[i]]
            parte2 = parse_nele(expo)
            
            parsed.append(parte1)
            parsed.append("^")
            parsed.append(parte2)
            # pergunta: é válido chamar parse_nele em ambas a base e o expoente?
    
    
    return parsed