# PROYECTO ALGORITMOS - ZADKIEL AVENDAÑO - C.I: 32695391

from productos import agregarProducto, buscarProducto, modificarProducto, eliminarProducto
from ventas import registrarVenta, generarFactura, buscarVenta
from clientes import registrarCliente, modificarCliente, eliminarCliente, buscarCliente
from pagos import buscarPago, registrarPago
from envios import buscarEnvio
from estadisticas import generar_informe_ventas, generar_informe_pagos, generar_informe_envios
from db import obtener_datos

# Funcion principal de la Gestion de Productos
def gestion_de_Productos():
    print("\nGestión de productos 🛒\n")
    while True:
        print("1. Agregar producto\n2. Buscar producto\n3. Modificar producto\n4. Eliminar producto\n5. Volver a INICIO")

        entrada = input("\nSelecciona una opcion: ")
        if entrada == "1":
            agregarProducto(productos)
            continue
        elif entrada == "2":
            buscarProducto(productos)
            continue
        elif entrada == "3":
            modificarProducto(productos)
            continue
        elif entrada == "4":
            eliminarProducto(productos)
            continue
        elif entrada == "5":
            break
        else:
            print("\nSelecciona una opcion valida...\n")
            continue

def gestion_de_Ventas():
    print("\nGestión de ventas ✅\n")
    while True:
        print("1. Registrar venta\n2. Generar factura\n3. Buscar venta\n4. Volver a INICIO")

        entrada = input("\nSelecciona una opcion: ")
        if entrada == "1":
            registrarVenta(clientes, productos, ventas, pagos, envios, estadisticas)
            continue
        elif entrada == "2":
            id_factura = input("Ingresa el ID de la venta para generar la factura: ")
            if not id_factura.isnumeric():
                print("\nDebes ingresar un valor valido...\n")
                continue
            id_factura = int(id_factura) - 1
            generarFactura(id_factura, ventas)
            continue
        elif entrada == "3":
            buscarVenta(ventas)
            continue
        elif entrada == "4":
            break
        else:
            print("\nSelecciona una opcion valida...\n")
            continue

def gestion_de_Clientes():
    print("\nGestión de clientes 🙂\n")

    while True:
        print("1. Registrar cliente\n2. Modificar cliente\n3. Eliminar cliente\n4. Buscar cliente\n5. Volver a INICIO")

        entrada = input("\nSelecciona una opcion: ")
        if entrada == "1":
            registrarCliente(clientes)
            continue
        elif entrada == "2":
            modificarCliente(clientes)
            continue
        elif entrada == "3":
            eliminarCliente(clientes)
            continue
        elif entrada == "4":
            buscarCliente(clientes)
            continue
        elif entrada == "5":
            break
        else:
            print("\nSelecciona una opcion valida...\n")
            continue

def gestion_de_Pagos():
    print("\nGestión de pagos 💲\n")

    while True:
        print("1. Registrar pago\n2. Buscar pago\n3. Volver a INICIO")

        entrada = input("\nSelecciona una opcion: ")
        if entrada == "1":
            registrarPago(pagos, clientes, estadisticas)
            continue
        elif entrada == "2":
            buscarPago(pagos)
            continue
        elif entrada == "3":
            break
        else:
            print("\nSelecciona una opcion valida...\n")
            continue

def gestion_de_Envios():
    print("\nGestión de envíos 🛩️\n")

    while True:
        print("1. Buscar envio\n2. Volver a INICIO")

        entrada = input("\nSelecciona una opcion: ")
        if entrada == "1":
            buscarEnvio(envios)
            continue
        elif entrada == "2":
            break
        else:
            print("\nSelecciona una opcion valida...\n")
            continue

def gestion_de_Estadisticas():
    print("\nIndicadores de gestión (estadísticas) 📊\n")

    while True:
        print("1. Informe de ventas\n2. Informe de pagos\n3. Informe de envios\n4. Volver a INICIO")

        entrada = input("\nSelecciona una opcion: ")
        if entrada == "1":
            generar_informe_ventas(estadisticas)
            continue
        elif entrada == "2":
            generar_informe_pagos(estadisticas, ventas, pagos)
            continue
        elif entrada == "3":
            generar_informe_envios(estadisticas, envios)
            continue
        elif entrada == "4":
            break
        else:
            print("\nSelecciona una opcion valida...\n")
            continue

if __name__=="__main__":

    # Obtiene toda la informacion de la BASE DE DATOS
    productos, clientes, ventas, pagos, envios, estadisticas = obtener_datos()

    # Inicia el ciclo del programa principal
    print("Tienda en línea de productos para vehículos 🚗")
    while True:
        print("\n1.	Gestión de productos 🛒\n2.	Gestión de ventas ✅\n3.	Gestión de clientes 🙂\n4.	Gestión de pagos 💲\n5.	Gestión de envíos 🛩️\n6.	Indicadores de gestión (estadísticas) 📊\n7.	Salir del programa ❌")
        
        entrada = input("\nSelecciona una opcion: ")
        if entrada == "1":
            gestion_de_Productos()
        elif entrada == "2":
            gestion_de_Ventas()
        elif entrada == "3":
            gestion_de_Clientes()
        elif entrada == "4":
            gestion_de_Pagos()
        elif entrada == "5":
            gestion_de_Envios()
        elif entrada == "6":
            gestion_de_Estadisticas()
        elif entrada == "7":
             print("Cerrando programa...")
             quit()
        else:
             print("\nSelecciona una opcion valida...")
             continue