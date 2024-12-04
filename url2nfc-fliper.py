def procesar_url(url):
    def identificar_protocolo(url):
        protocols = {
            "https://www.": "02",
            "http://www.": "01",
            "https://": "04",
            "http://": "03",
            "tel:": "05",
            "mailto:": "06"
        }
        for protocol, identifier in protocols.items():
            if url.startswith(protocol):
                return identifier
        return "00"  # Sin identificador de protocolo conocido

    def obtener_longitud_resto(url):
        protocols = ["https://www.", "http://www.", "https://", "http://", "ftp://"]
        for protocol in protocols:
            if url.startswith(protocol):
                resto = url[len(protocol):]
                break
        else:
            resto = url
        resto_hex = ''.join([format(byte, '02X') for byte in bytearray(resto, 'utf-8')])
        return len(resto) + 1, [resto_hex[i:i+2] for i in range(0, len(resto_hex), 2)]

    longitud_resto, resto_hex = obtener_longitud_resto(url)
    NFC_TYPE = "D1"                                 # NFC type
    LENGTH_RECORD = "01"                            # Length record of URL
    LENGTH_PAYLOAD = format(longitud_resto, '02X')  # Length of the payload
    URI_TYPE = "55"                                 # URI type
    URI_IDENTIFIER = identificar_protocolo(url)     # URI identifier
    STRING = ''.join(resto_hex)                     # Content of the URL (hex string)
    STRUCTURE_NDEF = [NFC_TYPE, LENGTH_RECORD, LENGTH_PAYLOAD, URI_TYPE, URI_IDENTIFIER, STRING]
    resultado = ''.join(STRUCTURE_NDEF)
    return resultado

def dividir_en_filas(resultado, longitud_fila=32):
    resultado = resultado.replace(" ", "")
    bytes_separados = [resultado[i:i+2] for i in range(0, len(resultado), 2)]
    filas = [
        ' '.join(bytes_separados[i:i+(longitud_fila // 2)])
        for i in range(0, len(bytes_separados), longitud_fila // 2)
    ]
    return filas

def rellenar_bloque(fila, longitud=32):
    longitud_actual = len(fila.replace(" ", ""))
    relleno_necesario = (longitud - longitud_actual) // 2  # Longitud en bytes
    return fila if relleno_necesario <= 0 else fila + " " + "00 " * relleno_necesario

def ajustar_bloques_con_numeros(filas, bloque_inicial=4):
    """
    Ajusta los bloques para que sean múltiplos de 4 filas, agrega relleno y etiqueta cada fila con 'Block X', comenzando desde 'bloque_inicial'.
    """
    # Rellenar cada fila con 00 00 si es necesario
    filas_rellenas = [rellenar_bloque(fila) for fila in filas]

    # Calcular cuántas filas adicionales necesitamos para ser múltiplo de 4
    filas_totales = len(filas_rellenas)
    filas_faltantes = (3 - (filas_totales % 4)) % 4  # Módulo para evitar agregar filas si ya es múltiplo de 4

    # Agregar filas vacías para completar un bloque
    for _ in range(filas_faltantes):
        filas_rellenas.append("00 " * 16)  # Fila vacía de 32 caracteres hexadecimales

    # Añadir etiquetas de bloque comenzando desde el bloque_inicial
    bloques_numerados = [
        f"Block {bloque_inicial + i}: {fila}" for i, fila in enumerate(filas_rellenas)
    ]
    return bloques_numerados

def generar_archivo_flipper(url, uid="1E 0A 23 3F"):
    resultado = procesar_url(url)
    INICIO = "03"
    NUM_LENGTH = format(len(resultado) // 2, '02X')
    CONTENT = resultado
    FINAL = "FE"
    result = INICIO + NUM_LENGTH + CONTENT + FINAL
    filas = dividir_en_filas(result)
    bloques_final = ajustar_bloques_con_numeros(filas, bloque_inicial=4)

    bloques_formateados = '\n'.join(bloques_final)

    cabecera = f"""
Filetype: Flipper NFC device
Version: 4
# Device type can be ISO14443-3A, ISO14443-3B, ISO14443-4A, ISO14443-4B, ISO15693-3, FeliCa, NTAG/Ultralight, Mifare Classic, Mifare Plus, Mifare DESFire, SLIX, ST25TB, EMV
Device type: Mifare Classic
# UID is common for all formats
UID: 1E 0A 23 3F
# ISO14443-3A specific data
ATQA: 00 04
SAK: 08
# Mifare Classic specific data
Mifare Classic type: 1K
Data format version: 2
# Mifare Classic blocks, '??' means unknown data
Block 0: 1E 0A 23 3F 08 08 04 00 62 63 64 65 66 67 68 69
Block 1: 14 01 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1
Block 2: 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1
Block 3: A0 A1 A2 A3 A4 A5 78 77 88 C1 89 EC A9 7F 8C 2A
{bloques_formateados}
Block 7: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 8: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 9: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 11: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 12: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 13: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 14: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 15: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 16: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 17: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 18: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 19: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 21: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 22: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 23: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 24: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 25: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 26: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 27: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 28: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 29: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 31: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 32: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 33: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 34: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 35: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 36: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 37: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 38: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 39: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 41: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 42: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 43: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 44: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 45: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 46: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 47: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 48: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 49: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 51: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 52: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 53: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 54: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 55: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 56: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 57: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 58: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 59: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
Block 60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 61: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 62: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Block 63: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF

"""
    return cabecera

# Ejemplo de uso
url = input("Introduce la URL: ")
archivo_flipper = generar_archivo_flipper(url)

# Mostrar el contenido generado en pantalla
print("=== Archivo NFC generado ===")
print(archivo_flipper)
