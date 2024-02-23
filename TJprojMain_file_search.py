import os
import subprocess
from datetime import datetime

def obtener_informacion_archivo(ruta_archivo):
    try:
        resultado = subprocess.run(['powershell', '-Command', f'Get-Command "{ruta_archivo}" | Format-List'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        informacion = resultado.stdout.decode('cp1252', errors='replace')
        return informacion
    except subprocess.CalledProcessError:
        return None

def buscar_archivos_con_texto(carpeta_raiz, texto):
    archivos_con_texto = []
    for directorio_raiz, _, archivos in os.walk(carpeta_raiz):
        for archivo in archivos:
            if archivo.lower().endswith('.exe'):
                ruta_archivo = os.path.join(directorio_raiz, archivo)
                informacion = obtener_informacion_archivo(ruta_archivo)
                if informacion and texto in informacion:
                    archivos_con_texto.append(ruta_archivo)
    return archivos_con_texto

def borrar_archivos(archivos):
    for archivo in archivos:
        os.remove(archivo)
        print(f"Archivo borrado: {archivo}")

def guardar_en_log(archivos):
    with open('archivos_encontrados.log', 'a') as f:
        f.write(f"\nArchivos encontrados ({datetime.now()}):\n")
        for archivo in archivos:
            f.write(archivo + '\n')

# Loop principal
while True:
    # Obtener la carpeta a analizar desde el usuario
    carpeta_raiz = input("Ingrese la dirección de la carpeta a analizar (o 'q' para salir): ")
    
    # Salir si el usuario ingresa 'q'
    if carpeta_raiz.lower() == 'q':
        break

    # Obtener el texto a buscar desde el usuario
    texto_a_buscar = "TJprojMain"

    # Buscar archivos que contienen el texto especificado
    archivos_con_texto = buscar_archivos_con_texto(carpeta_raiz, texto_a_buscar)

    if archivos_con_texto:
        print("\nArchivos que contienen el texto especificado:")
        for archivo in archivos_con_texto:
            print(archivo)

        # Guardar los archivos encontrados en un log
        guardar_en_log(archivos_con_texto)

        # Preguntar al usuario si desea borrar los archivos
        respuesta = input("\n¿Desea borrar los archivos encontrados? (si/no): ")
        if respuesta.lower() in ['si', 's', 'yes', 'y']:
            borrar_archivos(archivos_con_texto)
    else:
        print("No se encontraron archivos con el texto especificado.")

print("¡Hasta luego!")
