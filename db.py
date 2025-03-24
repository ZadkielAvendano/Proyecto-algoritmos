# PROYECTO ALGORITMOS - ZADKIEL AVENDAÑO - C.I: 32695391

import requests
import json
import os
from productos import Producto
from ventas import Venta
from clientes import Cliente
from pagos import Pago
from ventas import Venta
from envios import Envio

API = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/products.json"

# Obtiene todos los datos de la base de datos local. Si no existen los crea a partir de la API
def obtener_datos():
    # Verifica si existen datos guardados
    if os.path.exists("assets"):
        try:
            # Obtiene los datos de los productos
            with open("assets/productos.json", "r", encoding="utf-8") as a:
                productos_dic = json.load(a)

            # Obtiene los datos de las ventas
            with open("assets/ventas.json", "r", encoding="utf-8") as a:
                ventas_dic = json.load(a)

            # Obtiene los datos de los clientes
            with open("assets/clientes.json", "r", encoding="utf-8") as a:
                clientes_dic = json.load(a)

            # Obtiene los datos de los pagos
            with open("assets/pagos.json", "r", encoding="utf-8") as a:
                pagos_dic = json.load(a)

            # Obtiene los datos de los envios
            with open("assets/envios.json", "r", encoding="utf-8") as a:
                envios_dic = json.load(a)

            # Obtiene los datos de las estadisticas
            with open("assets/estadisticas.json", "r", encoding="utf-8") as a:
                estatisticas_dic = json.load(a)

        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error al leer los archivos JSON: {e}")
            productos_dic = []
            ventas_dic = []
            clientes_dic = []
            pagos_dic = []
            envios_dic = []
            estatisticas_dic = [{},{},{},{},{},{}]
    else:
        print("Descargando productos...")

        try:
            # Obtiene los productos desde la API del proyecto
            solicitud = requests.get(url=API)
            solicitud.raise_for_status()
            productos_dic = solicitud.json()

            # Crea variables vacías para los datos restantes
            ventas_dic = []
            clientes_dic = []
            pagos_dic = []
            envios_dic = []
            estatisticas_dic = [{},{},{},{},{},{}]

            # Crea la carpeta 'assets' donde se guardarán todos los datos
            os.makedirs("assets", exist_ok=True)

            # Crea el JSON donde se guardan los productos
            with open("assets/productos.json", "w", encoding="utf-8") as a:
                json.dump(productos_dic, a, indent=4, ensure_ascii=False)

            # Crea el JSON donde se guardan las ventas
            with open("assets/ventas.json", "w", encoding="utf-8") as a:
                json.dump(ventas_dic, a, indent=4, ensure_ascii=False)

            # Crea el JSON donde se guardan los clientes
            with open("assets/clientes.json", "w", encoding="utf-8") as a:
                json.dump(clientes_dic, a, indent=4, ensure_ascii=False)

            # Crea el JSON donde se guardan los pagos
            with open("assets/pagos.json", "w", encoding="utf-8") as a:
                json.dump(pagos_dic, a, indent=4, ensure_ascii=False)

            # Crea el JSON donde se guardan los envios
            with open("assets/envios.json", "w", encoding="utf-8") as a:
                json.dump(envios_dic, a, indent=4, ensure_ascii=False)

            # Crea el JSON donde se guardan las estadisticas
            with open("assets/estadisticas.json", "w", encoding="utf-8") as a:
                json.dump(estatisticas_dic, a, indent=4, ensure_ascii=False)

        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            productos_dic = []
            ventas_dic = []
            clientes_dic = []
            pagos_dic = []
            envios_dic = []
            estatisticas_dic = [{},{},{},{},{},{}]



    # Convierte el diccionario de productos a una lista de Objetos (Productos)
    productos = []
    for i in productos_dic:
        obj = Producto(i["id"], i["name"], i["description"], i["price"], i["category"], i["inventory"], i["compatible_vehicles"])
        productos.append(obj)



    # Convierte el diccionario de pagos a una lista de Objetos (Pagos)
    pagos = []
    for i in pagos_dic:
        cliente = Cliente(i["cliente"]["nombre"], i["cliente"]["cedula"], i["cliente"]["correo"], i["cliente"]["direccion_envio"], i["cliente"]["telefono"], i["cliente"]["juridico"], i["cliente"]["contacto_nombre"], i["cliente"]["contacto_telefono"], i["cliente"]["contacto_correo"])
        obj = Pago(cliente, i["monto"], i["moneda"], i["tipo_pago"], i["fecha"])
        pagos.append(obj)


    
    # Convierte el diccionario de envios a una lista de Objetos (Envios)
    envios = []
    for i in envios_dic:
        cliente = Cliente(i["cliente"]["nombre"], i["cliente"]["cedula"], i["cliente"]["correo"], i["cliente"]["direccion_envio"], i["cliente"]["telefono"], i["cliente"]["juridico"], i["cliente"]["contacto_nombre"], i["cliente"]["contacto_telefono"], i["cliente"]["contacto_correo"])
        obj = Envio(cliente, i["orden_compra"], i["servicio_envio"], i["datos_motorizado"], i["costo_servicio"], i["fecha"], i["enviado"])
        envios.append(obj)



    # Convierte el diccionario de clientes a una lista de Objetos (Clientes)
    clientes = []
    for i in clientes_dic:
        if i["juridico"]:
            obj = Cliente(i["nombre"], i["cedula"], i["correo"], i["direccion_envio"], i["telefono"], i["juridico"], i["contacto_nombre"], i["contacto_telefono"], i["contacto_correo"])
        else:
            obj = Cliente(i["nombre"], i["cedula"], i["correo"], i["direccion_envio"], i["telefono"], i["juridico"], None, None, None)
        clientes.append(obj)



    # Convierte el diccionario de ventas a una lista de Objetos (Ventas)
    ventas = []
    # Recorremos cada venta en el diccionario de ventas (suponiendo que `ventas_dic` es la lista de ventas cargada)
    for i in ventas_dic:
        # Buscar el cliente correspondiente por cédula
        cliente_obj = None
        for c in clientes:
            if c.cedula == i["cliente"]["cedula"]:
                cliente_obj = c
                break  # Encontramos al cliente, salimos del ciclo

        if cliente_obj is None:
            print(f"No se encontró el cliente con cédula {i['cliente']['cedula']}. No se podrá registrar esta venta.")
            continue  # Si no encontramos el cliente, saltamos esta venta

        # Ahora, para los productos de la venta, se hace algo similar
        productos_comprados = []
        cantidad_productos = {}
        
        for prod_data in i["productos_comprados"]:
            producto_obj = None
            for p in productos:
                if p.id == prod_data["id"]:
                    producto_obj = p
                    break  # Encontramos el producto, salimos del ciclo
            
            if producto_obj is None:
                print(f"No se encontró el producto con ID {prod_data['id']}. No se podrá registrar esta venta.")
                continue  # Si no encontramos el producto, no lo agregamos

            productos_comprados.append(producto_obj)  # Añadimos el producto a la lista
            cantidad_productos[producto_obj] = prod_data["cantidad"]  # Guardamos la cantidad del producto

        # Ahora calculamos los demás campos: subtotal, descuentos, iva, igtf, total
        subtotal = 0
        for producto in productos_comprados:
            cantidad = cantidad_productos[producto]
            subtotal += producto.price * cantidad
        

        # Crear objeto de la venta
        venta = Venta(cliente_obj, productos_comprados, cantidad_productos, i["metodo_pago"], i["metodo_envio"], subtotal, i["descuentos"], i["iva"], i["igtf"], i["total"])

        # Añadimos la venta a la lista de ventas
        ventas.append(venta)


    return productos, clientes, ventas, pagos, envios, estatisticas_dic
