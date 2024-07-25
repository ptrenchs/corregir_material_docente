from fun_CMD import contenido_directorio
from fun_CMD import fucniones_strings
import json
import os

class Corregir:
    def __init__(self, rutas_alumno):
        self.rutas_alumno = rutas_alumno
        # self.ruta_directorio = ruta_directorio

    def corregir(self):
        carpeta_principal = contenido_directorio.Directorio('/'.join(os.path.abspath(__file__).split('/')[:-2])).all_archivos()
        
        archivos_ref= contenido_directorio.Filtros_formato(rutas = carpeta_principal,formatos = 'ipynb').elejir()
        archivos_ref = contenido_directorio.Filtros_carpetas(rutas = archivos_ref,carpetas = '.ipynb_checkpoints').eliminar()
        for ruta_al in self.rutas_alumno:            
            nombre_al = '.'.join(os.path.basename(ruta_al).split('.')[:-1])
            for ruta_ref in archivos_ref:
                nombre_ref = '.'.join(os.path.basename(ruta_ref).split('.')[:-1])
                if nombre_ref in nombre_al or nombre_ref == nombre_al:
                    break
            if nombre_ref in nombre_al or nombre_ref == nombre_al:
                print(ruta_al)
                print(ruta_ref)
                codigo_al = Extraer_Codigo(ruta_al).Codigo().split('\n')
                with open(ruta_ref,'r',encoding='utf-8') as archivo:
                    datos = json.load(archivo)

                i_ref_0 = 0
                codigo_ref = ''
                for i_al,line_al in enumerate(codigo_al):
                    var_d_al = fucniones_strings.linea(line = line_al).var_dep()
                    if var_d_al != '':
                        left_al = ((var_d_al.split('=')[0]).replace('\t','')).replace(' ','')
                        dic_al = Extraer_Codigo.extraer_variables(codigo_py = codigo_al[:i_al+1])
                        right_al = dic_al[left_al]
                        for i_ref in range(i_ref_0,len(datos['cells'])):
                            if datos['cells'][i_ref]['cell_type'] == 'code':
                                for i in range(len(datos['cells'][i_ref]['source'])):
                                    var_d_ref = fucniones_strings.linea(line = datos['cells'][i_ref]['source'][i]).var_dep()
                                    left_ref = ((var_d_ref.split('=')[0]).replace('\t','')).replace(' ','')
                                    if left_ref == left_al:
                                        i_ref_0 += i_ref + 1

                                        print(codigo_ref + datos['cells'][i_ref]['source'][i])

                                        dic_ref = Extraer_Codigo.extraer_variables(codigo_py = codigo_ref + datos['cells'][i_ref]['source'][i])
                                        right_ref = dic_ref[left_ref]
                                        err_r = abs(right_ref-right_al)/abs(right_ref)
                                        if err_r < 0.5:
                                            datos['cells'][i_ref]['source'][i] = '#---- Resposta correcte ----#\n' + datos['cells'][i_ref]['source'][i] + '#---- Resposta correcte ----#\n'
                                        else:
                                            datos['cells'][i_ref]['source'][i] = '#---- Resposta incorrecte ----#\n' + datos['cells'][i_ref]['source'][i] + f'print({left_ref})\n{left_al} = {right_al}\n' + '#---- Resposta incorrecte ----#\n'
                                        break
                                    codigo_ref += datos['cells'][i_ref]['source'][i].replace('\n','') + '\n'

                                    print('\n\n sep')
                                if left_ref == left_al:
                                    break
                carpeta_corretgit = '/'.join(ruta_al.split('/')[:-2]) + '/5-corretgit'
                os.makedirs(carpeta_corretgit,exist_ok=True)
                ruta_corretgit = carpeta_corretgit + '/' + os.path.basename(ruta_al)
                with open(ruta_corretgit, 'w', encoding='utf-8') as nuevo_archivo:
                    json.dump(datos, nuevo_archivo, ensure_ascii=False, indent=4)
            else:
                print(f'Revisa el nombre del archivo {nombre_al}')

class Extraer_Codigo:
    def __init__(self, ruta):
        self.ruta = ruta

    def extraer_variables(codigo_py):
        if type(codigo_py) != str:
            codigo_py = '\n'.join(codigo_py)
        var = {}
        exec(codigo_py,{},var)
        return var

    def Codigo(self):
        with open(self.ruta,'r',encoding='utf-8') as archivo:
            datos = json.load(archivo)

        codigo_py = ''        
        for pos,cell in enumerate(datos['cells']):
            if cell['cell_type'] == 'code':
                for i in range(len(cell['source'])):
                    line = cell['source'][i].replace('\n','')
                    codigo_py += line + '\n'
        return codigo_py
