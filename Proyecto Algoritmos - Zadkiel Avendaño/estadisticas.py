# PROYECTO ALGORITMOS - ZADKIEL AVENDAÑO - C.I: 32695391

import json
from datetime import datetime

# Actualiza la base de datos de estadisticas indicando la nueva lista de estadisticas
def actualizar_estadisticas(estadisticas: list):
    with open("assets/estadisticas.json", "w", encoding="utf-8") as a:
            json.dump(estadisticas, a, indent=4, ensure_ascii=False)



# Agrega una venta de la fecha actual a la base de datos de estadisticas
def agregar_venta_fecha(estadisticas: list):
    dic = estadisticas[0]
    fecha = str(datetime.now().date())
    if fecha in dic:
        dic[fecha] = int(dic[fecha]) + 1
    else:
        dic[fecha] = 1
    estadisticas[0] = dic
    actualizar_estadisticas(estadisticas)



# Agrega un producto comprado a la base de datos de estadisticas
def agregar_producto_vendido(estadisticas: list, id: str, cantidad: int):
    dic = estadisticas[1]
    id = str(id)
    if id in dic:
        dic[id] += cantidad
    else:
        dic[id] = cantidad
    actualizar_estadisticas(estadisticas)



# Agrega una compra de cliente a la base de datos de estadisticas
def agregar_compra_cliente(estadisticas: list, cedula: str):
    dic = estadisticas[2]
    if cedula in dic:
        dic[cedula] = int(dic[cedula]) + 1
    else:
        dic[cedula] = 1
    estadisticas[2] = dic
    actualizar_estadisticas(estadisticas)



# Agrega una pago de la fecha actual a la base de datos de estadisticas
def agregar_pago_fecha(estadisticas: list):
    dic = estadisticas[3]
    fecha = str(datetime.now().date())
    if fecha in dic:
        dic[fecha] = int(dic[fecha]) + 1
    else:
        dic[fecha] = 1
    estadisticas[3] = dic
    actualizar_estadisticas(estadisticas)



# Agrega un envio de la fecha actual a la base de datos de estadisticas
def agregar_envio_fecha(estadisticas: list):
    dic = estadisticas[5]
    fecha = str(datetime.now().date())
    if fecha in dic:
        dic[fecha] = int(dic[fecha]) + 1
    else:
        dic[fecha] = 1
    estadisticas[3] = dic
    actualizar_estadisticas(estadisticas)



def obtener_clientes_con_pagos_pendientes(ventas: list, pagos: list):
    ventas_totales = {}
    pagos_realizados = {}

    # Calcular ventas totales por cliente
    for venta in ventas:
        cedula = venta.cliente.cedula
        if cedula in ventas_totales:
            ventas_totales[cedula] += venta.total
        else:
            ventas_totales[cedula] = venta.total

    # Calcular pagos realizados por cliente
    for pago in pagos:
        cedula = pago.cliente.cedula
        if cedula in pagos_realizados:
            pagos_realizados[cedula] += pago.monto
        else:
            pagos_realizados[cedula] = pago.monto

    # Identificar clientes con pagos pendientes
    clientes_con_pagos_pendientes = []

    for cedula, total_ventas in ventas_totales.items():
        pagos = pagos_realizados.get(cedula, 0)
        if total_ventas > pagos:
            cliente_info = next(venta.cliente for venta in ventas if venta.cliente.cedula == cedula)
            cliente_info.deuda = total_ventas - pagos
            clientes_con_pagos_pendientes.append(cliente_info)

    return clientes_con_pagos_pendientes



# Genera el informe sobre las ventas
def generar_informe_ventas(estadisticas: list):
    from datetime import datetime

    ventas_por_dia = estadisticas[0]
    productos_vendidos = estadisticas[1]
    compras_clientes = estadisticas[2]

    # Convertir las claves a fechas y calcular las ventas por día, semana, mes y año
    ventas_por_semana = {}
    ventas_por_mes = {}
    ventas_por_anio = {}

    for fecha_str, cantidad in ventas_por_dia.items():
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        
        # Agrupar por semana
        semana = fecha.strftime("%Y-%U")  # Año y semana del año
        if semana not in ventas_por_semana:
            ventas_por_semana[semana] = 0
        ventas_por_semana[semana] += cantidad
        
        # Agrupar por mes
        mes = fecha.strftime("%Y-%m")  # Año y mes
        if mes not in ventas_por_mes:
            ventas_por_mes[mes] = 0
        ventas_por_mes[mes] += cantidad
        
        # Agrupar por año
        anio = fecha.strftime("%Y")  # Año
        if anio not in ventas_por_anio:
            ventas_por_anio[anio] = 0
        ventas_por_anio[anio] += cantidad

    print("\n -- VENTAS POR DIA / MES / AÑO -- ")
    print("Ventas por día:", ventas_por_dia)
    print("Ventas por semana:", ventas_por_semana)
    print("Ventas por mes:", ventas_por_mes)
    print("Ventas por año:", ventas_por_anio)

    # Definir una función que devuelva el valor
    def obtener_valor(item):
        return item[1]

    # Ordenar el diccionario por las ventas en orden descendente y obtener los 5 primeros
    productos_mas_vendidos = sorted(productos_vendidos.items(), key=obtener_valor, reverse=True)[:5]

    print("\n -- LOS 5 PRODUCTOS MAS VENDIDOS -- ")
    for producto, ventas in productos_mas_vendidos:
        print(f"Producto ID: {producto}, Ventas: {ventas}")

    # Ordenar el diccionario por las compras de los clientes en orden descendente y obtener los 5 mas frecuentes
    clientes_frecuentes = sorted(compras_clientes.items(), key=obtener_valor, reverse=True)[:5]

    print("\n -- LOS 5 CLIENTES MAS FRECUENTES -- ")
    for cliente, compras in clientes_frecuentes:
        print(f"Cliente ( CI / RIF ): {cliente}, Compras: {compras}")
    
    print("")



# Genera el informe sobre los pagos
def generar_informe_pagos(estadisticas: list, ventas: list, pagos: list):
    from datetime import datetime

    pagos_por_dia = estadisticas[3]

    # Convertir las claves a fechas y calcular las ventas por día, semana, mes y año
    pagos_por_semana = {}
    pagos_por_mes = {}
    pagos_por_anio = {}

    for fecha_str, cantidad in pagos_por_dia.items():
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        
        # Agrupar por semana
        semana = fecha.strftime("%Y-%U")  # Año y semana del año
        if semana not in pagos_por_semana:
            pagos_por_semana[semana] = 0
        pagos_por_semana[semana] += cantidad
        
        # Agrupar por mes
        mes = fecha.strftime("%Y-%m")  # Año y mes
        if mes not in pagos_por_mes:
            pagos_por_mes[mes] = 0
        pagos_por_mes[mes] += cantidad
        
        # Agrupar por año
        anio = fecha.strftime("%Y")  # Año
        if anio not in pagos_por_anio:
            pagos_por_anio[anio] = 0
        pagos_por_anio[anio] += cantidad

    print("\n -- PAGOS POR DIA / MES / AÑO -- ")
    print("Pagos por día:", pagos_por_dia)
    print("Pagos por semana:", pagos_por_semana)
    print("Pagos por mes:", pagos_por_mes)
    print("Pagos por año:", pagos_por_anio)

    clientes_con_pagos_pendientes = obtener_clientes_con_pagos_pendientes(ventas, pagos)

    print("\n -- CLIENTES CON PAGOS PENDIENTES -- ")
    for cliente in clientes_con_pagos_pendientes:
        print(f"Cédula: {cliente.cedula}, Nombre: {cliente.nombre}, Deuda: {round(cliente.deuda, 2)}")


    print("")


# Genera el informe sobre los envios
def generar_informe_envios(estadisticas: list, envios: list):
    from datetime import datetime

    productos_vendidos = estadisticas[1]
    envios_por_dia = estadisticas[5]

    # Convertir las claves a fechas y calcular las ventas por día, semana, mes y año
    envios_por_semana = {}
    envios_por_mes = {}
    envios_por_anio = {}

    for fecha_str, cantidad in envios_por_dia.items():
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        
        # Agrupar por semana
        semana = fecha.strftime("%Y-%U")  # Año y semana del año
        if semana not in envios_por_semana:
            envios_por_semana[semana] = 0
        envios_por_semana[semana] += cantidad
        
        # Agrupar por mes
        mes = fecha.strftime("%Y-%m")  # Año y mes
        if mes not in envios_por_mes:
            envios_por_mes[mes] = 0
        envios_por_mes[mes] += cantidad
        
        # Agrupar por año
        anio = fecha.strftime("%Y")  # Año
        if anio not in envios_por_anio:
            envios_por_anio[anio] = 0
        envios_por_anio[anio] += cantidad

    print("\n -- ENVIOS POR DIA / MES / AÑO -- ")
    print("Envios por día:", envios_por_dia)
    print("Envios por semana:", envios_por_semana)
    print("Envios por mes:", envios_por_mes)
    print("Envios por año:", envios_por_anio)

    # Definir una función que devuelva el valor
    def obtener_valor(item):
        return item[1]

    # Ordenar el diccionario por las ventas en orden descendente y obtener los 5 primeros
    productos_mas_vendidos = sorted(productos_vendidos.items(), key=obtener_valor, reverse=True)[:5]

    print("\n -- LOS 5 PRODUCTOS MAS ENVIADOS -- ")
    for producto, ventas in productos_mas_vendidos:
        print(f"Producto ID: {producto}, Envios: {ventas}")

    # Filtrar envíos pendientes
    envios_pendientes = [envio for envio in envios if not envio.enviado]

    print("\n -- CLIENTES CON ENVIOS PENDIENTES -- ")
    for envio in envios_pendientes:
        print(f"Cédula: {envio.cliente.cedula}, Nombre: {envio.cliente.nombre}, Orden de compra: {envio.orden_compra}, Fecha: {envio.fecha}")


