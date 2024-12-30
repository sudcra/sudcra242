import pandas as pd

def generar_codigo(contador, total_tipos):
    primer_digito = str(total_tipos)
    segundo_digito = str(contador)
    return 'a' + primer_digito + segundo_digito

def carga_dataset():
    ruta = "C:\\Users\\mcorteze\\Desktop\\Rutinas\\Creando_pdf\\Intento 4\\Libro2.xlsx"
    # Aquí deberías cargar tu DataFrame, ya que la función `convertir_a_df_tipo_0` no está definida aquí
    df = pd.read_excel(ruta)

    tipos_medida = df['nombre_tipo_medida']

    
    df_aprendizajes = pd.DataFrame(tipos_medida, columns=['nombre_tipo_medida'])

    df_aprendizajes.reset_index(drop=True, inplace=True)

    contador_por_tipo = {}
    codigos = []

    for tipo in df_aprendizajes['nombre_tipo_medida']:
        if tipo not in contador_por_tipo:
            contador_por_tipo[tipo] = 1
            total_tipos = len(contador_por_tipo)
            codigo = generar_codigo(contador_por_tipo[tipo], total_tipos)
        else:
            contador_por_tipo[tipo] += 1
            total_tipos = len(contador_por_tipo)
            codigo_existente = generar_codigo(contador_por_tipo[tipo] - 1, total_tipos)
            nuevo_codigo = generar_codigo(contador_por_tipo[tipo], total_tipos)
            while nuevo_codigo == codigo_existente:
                contador_por_tipo[tipo] += 1
                nuevo_codigo = generar_codigo(contador_por_tipo[tipo], total_tipos)
            codigo = nuevo_codigo
        codigos.append(codigo)

    df_aprendizajes['codigo'] = codigos

    # Agregar la columna de numeración
    df_aprendizajes['numeracion'] = df_aprendizajes.index + 1


    # Agregar otra columna desde el dataframe original
    df_aprendizajes['desc_larga'] = df['desc_larga'] 
    df_aprendizajes['logro'] = df['logro']
    df_aprendizajes['orden'] = df['orden']   
    
    # Cambiar orden de los campos
    nuevo_orden = ['numeracion','nombre_tipo_medida', 'codigo', 'orden','desc_larga', 'logro']
    df_aprendizajes = df_aprendizajes.reindex(columns=nuevo_orden)

    # Cambiar el nombre de los campos
    nuevos_nombres = ['n', 'aprendizaje', 'clave', 'orden', 'descripcion_aprendizaje','logro_estudiante']
    df_aprendizajes.columns = nuevos_nombres

    return df_aprendizajes

print(carga_dataset())
