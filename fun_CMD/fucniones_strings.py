class linea:
    def __init__(self, line, coment = '#', sep_enter = ' ,\t,\n', especiales = 'if,else,break,for,while'):
        self.line = line
        self.coment = coment
        self.sep_enter = sep_enter
        self.especiales = especiales

    def tipo_linea_code(self):
        cometario = linea(line=self.line).comentario()
        new_line = self.line.replace(cometario,'')
        for sep in self.sep_enter.split(','):
            new_line = new_line.replace(sep,'')
        if new_line != '':
            new_line = self.line.replace(cometario,'')
            for i,car in enumerate(new_line):
                if not (car in self.sep_enter.split(',')[:-1]):
                    break
            new_line = new_line[i:]
            for esp in self.especiales.split(','):
                if new_line.startswith(esp):
                    break
            if not new_line.startswith(esp):
                if '=' in new_line:
                    left = new_line.split('=')[0]
                    rigth = new_line.split('=')[1]
                    try:
                        eval(rigth)
                        return 'indep'
                    except:
                        return 'dep'
                else:
                    return 'display'
            else:
                return 'Esepecial'

        else:
            return ''

    def var_indepe(self):
        if linea(line=self.line).tipo_linea_code() == 'indep':
            cometario = linea(line=self.line).comentario()
            return self.line.replace(cometario,'')
        else:
            return ''
        
        
    def var_dep(self):
        if linea(line=self.line).tipo_linea_code() == 'dep':
            cometario = linea(line=self.line).comentario()
            return self.line.replace(cometario,'')
        else:
            return ''
        
    def line_especial(self):
        if linea(line=self.line).tipo_linea_code() == 'Esepecial':
            cometario = linea(line=self.line).comentario()
            return self.line.replace(cometario,'')
        else:
            return ''
    def ver_valor(self):
        if linea(line=self.line).tipo_linea_code() == 'display':
            cometario = linea(line=self.line).comentario()
            return self.line.replace(cometario,'')
        else:
            return ''


    def comentario(self):
        if self.line == '':
            return ''
        for i,car in enumerate(self.line):
            for com in self.coment.split(','):
                if com == car:
                    break
            if com == car:
                break
        if com == car:
            comentario = self.line[i+1:]
            for i,car in enumerate(comentario):
                if not (car in self.sep_enter.split(',')[:-1]):
                    break
            return '# ' + comentario[i:]
        else:
            return ''
        
# print(linea(line=' #     hola').comentario())