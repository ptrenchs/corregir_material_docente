from fun_CMD import contenido_directorio
from fun_CMD import manipulacion_archivos

carpeta = contenido_directorio.Directorio('/home/ptrenchs/Escritorio/carpeta_probas').all_archivos()
archivos_ipynb = contenido_directorio.Filtros_formato(rutas = carpeta,formatos = 'ipynb').elejir()
archivos_ipynb = contenido_directorio.Filtros_carpetas(rutas = archivos_ipynb,carpetas = '.ipynb_checkpoints').eliminar()
archivos_ipynb = contenido_directorio.Filtros_carpetas(rutas = archivos_ipynb,carpetas = '4-resuelto_Alumnos').elejir()
print(archivos_ipynb)
manipulacion_archivos.Corregir(archivos_ipynb).corregir()