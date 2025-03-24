# PROYECTO ALGORITMOS - ZADKIEL AVENDAÑO - C.I: 32695391

import json
from datetime import datetime
from clientes import Cliente
from estadisticas import agregar_pago_fecha

class Pago:
    def __init__(self, cliente: Cliente, monto: float, moneda: str, tipo_pago: str, fecha: str):
        self.cliente = cliente
        self.monto = monto
        self.moneda = moneda
        self.tipo_pago = tipo_pago
        self.fecha = fecha

    def mostrar_detalles(self):
        print(f"\nCliente: {self.cliente.nombre}\nMonto: {self.monto}\nMoneda: {self.moneda}\nTipo de pago: {self.tipo_pago}\n Fecha: {self.fecha}")



# Actualiza la base de datos de pagos indicando la nueva lista de pagos
def actualizar_pagos(pagos: list[Pago]):
    pagos_dic = []

    for pago in pagos:
        dic = {
            "cliente": {
                "cedula": pago.cliente.cedula,
                "nombre": pago.cliente.nombre,
                "correo": pago.cliente.correo,
                "direccion_envio": pago.cliente.direccion_envio,
                "telefono": pago.cliente.telefono,
                "juridico": pago.cliente.juridico,
                "contacto_nombre": pago.cliente.contacto_nombre,
                "contacto_telefono": pago.cliente.contacto_telefono,
                "contacto_correo": pago.cliente.contacto_correo
            },
            "monto": pago.monto,
            "moneda": pago.moneda,
            "tipo_pago": pago.tipo_pago,
            "fecha": pago.fecha
        }
        pagos_dic.append(dic)

    with open("assets/pagos.json", "w", encoding="utf-8") as a:
            json.dump(pagos_dic, a, indent=4, ensure_ascii=False)



# Busca los pagos dependiendo de un filtro
def buscar_pagos(pagos: list[Pago], filtro: str, valor):
        for pago in pagos:
            if filtro == "cliente" and valor.lower() in pago.cliente.nombre.lower():
                pago.mostrar_detalles()
            elif filtro == "fecha" and valor.lower() == pago.fecha.lower():
                pago.mostrar_detalles()
            elif filtro == "tipo" and valor.lower() in pago.tipo_pago.lower():
                pago.mostrar_detalles()
            elif filtro == "moneda" and valor.lower() == pago.moneda.lower():
                pago.mostrar_detalles()



# Registra el pago en la base de datos
def registrar_pago(pagos: list[Pago], cliente: Cliente, monto: float, moneda: str, tipo_pago: str, estadisticas: list):
    fecha = datetime.now().date()
    pago = Pago(cliente, round(monto, 2), moneda, tipo_pago, str(fecha))
    pagos.append(pago)
    actualizar_pagos(pagos)

    # Registra los valores a la base de datos de ESTADISTICAS
    agregar_pago_fecha(estadisticas)



def registrarPago(pagos: list[Pago], clientes: list[Cliente], estadisticas: list):
    print("\n-- Registrar Pago --")
    
    # Seleccionar cliente
    cedula_cliente = input("Ingrese la cédula o RIF del cliente: ")
    cliente = next((cliente for cliente in clientes if cliente.cedula == cedula_cliente), None)
    
    if not cliente:
        print("Cliente no encontrado. Intente de nuevo.")
        return
    
    # Monto del pago
    while True:
        monto = input("\nIngresa el monto a pagar: ")
        if monto.isnumeric():
            monto = float(monto)
            break
        else:
            print("\nIngresa un valor valido...")
            continue

    # Métodos de pago
    while True:
        metodo_pago = input("\nSeleccione el método de pago (Divisas, Efectivo, Tarjeta, Pago movil, Transferencia, Zelle): ")
        metodo_pago = metodo_pago.lower()
        if metodo_pago == "divisas" or metodo_pago == "zelle":
            print("Moneda: USD")
            moneda = "USD"
            break
        elif metodo_pago == "efectivo" or metodo_pago == "tarjeta" or metodo_pago == "pago movil" or metodo_pago == "transferencia":
            print("Moneda: VEF")
            moneda = "VEF"
            break
        else:
            print("\nElige un metodo de pago valido...\n")
    
    registrar_pago(pagos, cliente, monto, moneda, metodo_pago, estadisticas)

    print("\nPago realizado con exito!!\n")



# Funcion que se llama de el programa principal para buscar pagos
def buscarPago(pagos: list[Pago]):
    while True:
        print("1. Cliente\n2. Fecha\n3. Tipo de pago\n4. Moneda")
        entrada_1 = input("\nSelecciona un filtro de busqueda: ")
        if entrada_1 == "1":
            entrada_2 = input("Nombre del cliente: ")
            buscar_pagos(pagos, "cliente", entrada_2)
            break
        elif entrada_1 == "2":
            entrada_2 = input("Fecha del pago en el siguiente formato ( año-mes-dia ): ")
            buscar_pagos(pagos, "fecha", entrada_2)
            break
        elif entrada_1 == "3":
            entrada_2 = input("Tipo de pago: ")
            buscar_pagos(pagos, "tipo", entrada_2)
            break
        elif entrada_1 == "4":
            entrada_2 = input("Moneda ( USD / VEF ): ")
            buscar_pagos(pagos, "moneda", entrada_2)
            break
        else:
            print("\nSelecciona una opcion valida...")
            continue
    print("")
