import datetime

# Cadenas de fecha y hora
fecha_str = "231205"  # Formato: aammdd
hora_str = "203540"  # Formato: hhmmss

# Convertir las cadenas en objetos datetime
fecha_dt = datetime.datetime.strptime(fecha_str, "%y%m%d")
hora_dt = datetime.datetime.strptime(hora_str, "%H%M%S")

# Combinar fecha y hora
fecha_hora_dt = fecha_dt.replace(hour=hora_dt.hour, minute=hora_dt.minute, second=hora_dt.second)

# Obtener el timestamp
timestamp = fecha_hora_dt.timestamp()

print(f"Fecha y hora: {fecha_hora_dt}")
print(f"Timestamp: {timestamp:.0f}")