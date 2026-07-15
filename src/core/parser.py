#testando o que aprendi
class ParseError(Exception):
    def __init__(self, pos, msg, *args):
        self.pos = pos # posição do texto
        self.msg = msg
        self.args = args
    
    def __str__(self):
        # a mensagem de erro
        return '%s at position %s' % (self.msg % self.args, self.pos)

class Parser:
    def __init__(self):
        self.cache = {}
    
    def parse(self, text):
        self.text = text
        self.pos = -1   # antes de scannear o string
        self.len = len(text) - 1    # max index do string
        rv = self.start()
        self.assert_end()
        return rv
    
    def assert_end(self):
        # checando posição atual
        if self.pos < self.len:
            raise ParseError(
                self.pos + 1,
                'Expected end of string but got %s',
                self.text[self.pos + 1]
            )
    
    def whitespace_eater(self):
        # to eat whitespaces when they appear
        while self.pos < self.len and self.text[self.pos + 1] in " \f\v\r\t\n":
            self.pos += 1
    
    def split_char_ranges(self, chars):
        # se aparecer de novo
        try:
            return self.cache[chars]
        except KeyError:
            pass
        
        rv = []
        index = 0
        length = len(chars)
        
        while index < length:
            if index + 2 < length and chars[index + 1] == '-':
                if chars[index] >= chars[index + 2]:
                    raise ValueError('Bad character range')
                
                # cobre o range todo, algo tipo 'x-y'
                rv.append(chars[index:index + 3])
                index += 3
            else:
                rv.append(chars[index])
                index += 1
        # like self.char('A-Za-z0-9'), mas more clean
        
        self.cache[chars] = rv
        return rv
    
    def char(self, chars=None):
        if self.pos >= self.len:
            # checando veracidade do conteúdo
            raise ParseError(
                self.pos + 1,
                'Expected %s but got end of string',
                'character' if chars is None else '[%s]' % chars
            )
        
        next_char = self.text[self.pos + 1]
        if chars == None:
            self.pos += 1
            return next_char
        
        for char_range in self.split_char_ranges(chars):
            # nesse loop checa se encaixa com o character ou o range
            if len(char_range) == 1:
                if next_char == char_range:
                    self.pos += 1
                    return next_char
            elif char_range[0] <= next_char <= char_range[2]:
                self.pos += 1
                return next_char
        
        raise ParseError(
            self.pos + 1,
            'Expected %s but got %s',
            'character' if chars is None else '[%s]' % chars, next_char
        )
    
    def keyword(self, *keywords):
        self.whitespace_eater()
        if self.pos >= self.len:
            raise ParseError(
                self.pos + 1,
                'Expected %s but got end of string',
                ','.join(keywords)
            )
        
        for keyword in keywords:
            low = self.pos + 1
            high = low + len(keyword)

            if self.text[low:high] == keyword:
                self.pos += len(keyword)
                self.whitespace_eater()
                return keyword
        
        raise ParseError(
            self.pos + 1,
            'Expected %s but got %s',
            ','.join(keywords),
            self.text[self.pos + 1],
        )
    
    def item(self):
        return self.match('number', 'word')
    
    def match(self, *rules):
        self.whitespace_eater()
        last_error_pos = -1
        last_exception = None
        last_error_rules = []
        
        # o match finder
        for rule in rules:
            initial_pos = self.pos
            try:
                rv = getattr(self, rule)()
                self.whitespace_eater()
                return rv
            except ParseError as e:
                self.pos = initial_pos
                
                if e.pos > last_error_pos:
                    last_exception = e
                    last_error_pos = e.pos
                    last_error_rules.clear()
                    last_error_rules.append(rule)
                elif e.pos == last_error_pos:
                    last_error_rules.append(rule)
        if len(last_error_rules) == 1:
            raise last_exception
        else:
            raise ParseError(
                last_error_pos,
                'Expected %s but got %s',
                ','.join(last_error_rules),
                self.text[last_error_pos]
            )
    

# quanto mais eu leio sobre parsers, mais eu penso que esse código não vai ser a versão final, mas o exercício mental é válido por hora
def parse_nele(expressao: str):
    # A estrutura com a expressão decodificada, organizada na ordem de resolução
    parsed = []
    
    for index, char in range(enumerate(expressao)):
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
    
    for index, char in range(enumerate(expressao)):
        # Segunda regra do PEMDAS: Expoentes
        if char == "^":
            # pensamento: loop reverso iniciado no ^, pra achar index que começa o bloco do número que é a base da potenciação; depois loop com direção normal pra encontrar o index que termina o bloco de número que é o expoente;
            
            last = 0
            for i, x in range(enumerate(expressao)[index-1], 0, -1):
                now = {i: x}
                if type(x) is int:
                    last = now
                else:
                    break
            base = expressao[last[i]:index-1]
            parte1 = parse_nele(base)
            
            last = 0
            for i, x in range(enumerate(expressao)[index+1]):
                now = {i: x}
                if type(x) is int:
                    last = now
                else:
                    break
            expo = expressao[index+1:last[i]]
            parte2 = parse_nele(expo)
            
            parsed.append(parte1)
            parsed.append("^")
            parsed.append(parte2)
            # pergunta: é válido chamar parse_nele em ambas a base e o expoente?
    
    
    return parsed