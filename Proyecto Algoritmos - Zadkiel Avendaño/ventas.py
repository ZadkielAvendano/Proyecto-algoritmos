# PROYECTO ALGORITMOS - ZADKIEL AVENDAÑO - C.I: 32695391

import json
from clientes import Cliente
from productos import Producto
from pagos import Pago, registrar_pago
from envios import Envio, registrarEnvio
from estadisticas import agregar_producto_vendido, agregar_compra_cliente, agregar_venta_fecha

class Venta:
    def __init__(self, cliente: Cliente, productos_comprados: list[Producto], cantidad_productos: dict, metodo_pago: str, metodo_envio: str, subtotal: float, descuentos: float, iva: float, igtf: float, total: float):
        self.cliente = cliente
        self.productos_comprados = productos_comprados
        self.cantidad_productos = cantidad_productos
        self.metodo_pago = metodo_pago
        self.metodo_envio = metodo_envio
        self.subtotal = subtotal
        self.descuentos = descuentos
        self.iva = iva
        self.igtf = igtf
        self.total = total

    def mostrar_detalles(self):
        print(f"Venta a {self.cliente.nombre} ({self.cliente.cedula})")
        print(f"Subtotal: {self.subtotal} | Descuentos: {self.descuentos} | IVA: {self.iva} | IGTF: {self.igtf} | Total: {self.total}")
        print(f"Productos comprados:")
        for producto, cantidad in self.cantidad_productos.items():
            print(f"{producto.name} - Cantidad: {cantidad} - Precio: {producto.price}")



# Actualiza la base de datos de ventas indicando la nueva lista de ventas
def actualizar_ventas(ventas: list[Venta]):
    ventas_dic = []

    for venta in ventas:
        # Creamos un diccionario con la información de cada venta
        dic = {
            "cliente": {
                "cedula": venta.cliente.cedula,
                "nombre": venta.cliente.nombre,
                "correo": venta.cliente.correo,
                "direccion_envio": venta.cliente.direccion_envio,
                "telefono": venta.cliente.telefono,
                "juridico": venta.cliente.juridico,
                "contacto_nombre": venta.cliente.contacto_nombre,
                "contacto_telefono": venta.cliente.contacto_telefono,
                "contacto_correo": venta.cliente.contacto_correo
            },
            "productos_comprados": [
                {"id": producto.id, "cantidad": venta.cantidad_productos[producto]} for producto in venta.productos_comprados
            ],
            "metodo_pago": venta.metodo_pago,
            "metodo_envio": venta.metodo_envio,
            "subtotal": venta.subtotal,
            "descuentos": venta.descuentos,
            "iva": venta.iva,
            "igtf": venta.igtf,
            "total": venta.total
        }

        ventas_dic.append(dic)

    # Guardamos la lista de ventas en un archivo JSON
    with open("assets/ventas.json", "w", encoding="utf-8") as a:
        json.dump(ventas_dic, a, indent=4, ensure_ascii=False)



# Función para calcular los totales y crear la venta
def calcular_totales(productos_comprados: list[Producto], cantidad_productos: dict, moneda: str, metodo_envio: str, cliente: Cliente):
    subtotal = sum(producto.price * cantidad_productos[producto] for producto in productos_comprados)
    
    print(moneda)

    # Aplicamos descuentos
    if cliente.juridico:
        descuentos = subtotal * 0.015
    else:
        descuentos = 0
    
    # Calculamos impuestos
    iva = subtotal * 0.16

    if moneda == "USD":
        igtf = subtotal * 0.03
    else:
        igtf = 0
    
    # Total a pagar
    total = subtotal - descuentos + iva + igtf
    
    return subtotal, descuentos, iva, igtf, total



# Función para registrar una venta
def registrarVenta(clientes: list[Cliente], productos: list[Producto], ventas: list[Venta], pagos: list[Pago], envios: list[Envio], estadisticas: list):
    print("\n-- Registrar Venta --")
    
    # Seleccionar cliente
    cedula_cliente = input("Ingrese la cédula o RIF del cliente: ")
    cliente = next((cliente for cliente in clientes if cliente.cedula == cedula_cliente), None)
    
    if not cliente:
        print("Cliente no encontrado. Intente de nuevo.")
        return

    # Seleccionar productos
    productos_comprados = []
    cantidad_productos = {}
    
    while True:
        print("\nSeleccione un producto (ID o 'salir' para terminar):")
        idx = 1
        for producto in productos:
            print(f"{idx}. {producto.name} - Precio: {producto.price}")
            idx += 1

        seleccion = input("\nIngrese el ID del producto o ( salir ) para terminar: ")
        if seleccion.lower() == 'salir':
            break
        
        try:
            producto_seleccionado = productos[int(seleccion) - 1]
            cantidad = int(input(f"¿Cuántas unidades de {producto_seleccionado.name} desea comprar?: "))
            
            if producto_seleccionado not in productos_comprados:
                productos_comprados.append(producto_seleccionado)
            cantidad_productos[producto_seleccionado] = cantidad_productos.get(producto_seleccionado, 0) + cantidad
        except (ValueError, IndexError):
            print("Selección no válida. Intente de nuevo.")
            continue

    # Métodos de pago y envío
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
    
    while True:
        metodo_envio = input("\nSeleccione el método de envío (Zoom, Delivery): ")
        metodo_envio = metodo_envio.lower()
        if metodo_envio == "zoom":
            datos_motorizado = None
            costo_servicio = 199.99
            break
        elif metodo_envio == "delivery":
            datos_motorizado = input("Datos del motorizado: ")
            costo_servicio = 49.99
            break
        else:
            print("\nElige un metodo de envio valido...\n")

    # Calcular totales
    subtotal, descuentos, iva, igtf, total = calcular_totales(productos_comprados, cantidad_productos, moneda, metodo_envio, cliente)
    
    # Crear venta
    venta = Venta(cliente, productos_comprados, cantidad_productos, metodo_pago, metodo_envio, round(subtotal, 2), round(descuentos, 2), round(iva, 2), round(igtf, 2), round(total, 2))

    ventas.append(venta)
    
    actualizar_ventas(ventas)
    
    print("")
    venta.mostrar_detalles()
    print(f"\nVenta registrada con éxito!\nOrden de compra: {len(ventas)}\n")
    
    # Registra el pago en la base de datos
    if cliente.juridico:
        while True:
            print("\nQuieres pagar de contado o credito ( Plazo de 30 a 15 dias )")
            entrada = input("Ingresa tu respuesta ( Contado / Credito ): ")
            if entrada.lower() == "contado":
                print("Pago registrado!")
                registrar_pago(pagos, cliente, total, moneda, metodo_pago, estadisticas)
                break
            elif entrada.lower() == "credito":
                print("Pago pendiente...")
                break
            else:
                print("\nIngresa un valor valido...")
    else:
        registrar_pago(pagos, cliente, total, moneda, metodo_pago, estadisticas)

    # Registra el envio en la base de datos si es por delivery
    if metodo_envio == "zoom":
        registrarEnvio(envios, cliente, len(ventas), metodo_envio, datos_motorizado, costo_servicio, False, estadisticas)
    else:
        registrarEnvio(envios, cliente, len(ventas), metodo_envio, datos_motorizado, costo_servicio, True, estadisticas)

    # Registra los valores a la base de datos de ESTADISTICAS
    agregar_venta_fecha(estadisticas)
    agregar_compra_cliente(estadisticas, cliente.cedula)
    for producto, cantidad in cantidad_productos.items():
            agregar_producto_vendido(estadisticas, producto.id, cantidad)






# Función para generar una factura
def generarFactura(id_venta: int, ventas: list[Venta]):
    try:
        venta = ventas[id_venta]

        print("\n-- Factura --")
        print(f"Factura #{id_venta + 1}")
        print(f"Cliente: {venta.cliente.nombre} ({venta.cliente.cedula})")
        print(f"Subtotal: {venta.subtotal} | Descuentos: {venta.descuentos} | IVA: {venta.iva} | IGTF: {venta.igtf} | Total: {venta.total}")
        print("Productos comprados:")
        
        for producto, cantidad in venta.cantidad_productos.items():
            print(f"{producto.name} - Cantidad: {cantidad} - Precio: {producto.price}\n")

        if venta.cliente.juridico:
            print("Puede realizar el pago a credito en un plazo de 15 a 30 dias.\n")
        else:
            print("Pago en el momento.\n")
    
    except (FileNotFoundError, IndexError) as e:
        print(f"Error al generar la factura: {e}")



# Función para buscar ventas
def buscarVenta(ventas: list[Venta]):

    print("\n-- Buscar Venta --")
    filtro = input("Ingrese el número de venta o la cédula del cliente: ")
        
    ventas_encontradas = []
        
    idx = 0
    for venta in ventas:
        if filtro in str(venta.cliente.cedula) or filtro == str(idx + 1):
            ventas_encontradas.append(venta)
        idx += 1
        
    if not ventas_encontradas:
        print("No se encontraron ventas con ese criterio.")
        return
        
    for venta in ventas_encontradas:
        print(f"\nVenta #{ventas.index(venta) + 1}")
        print(f"Cliente: {venta.cliente.nombre} ({venta.cliente.cedula})")
        print(f"Total: {venta.total}")
