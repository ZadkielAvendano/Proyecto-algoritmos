# PROYECTO ALGORITMOS - ZADKIEL AVENDAÑO - C.I: 32695391

import json
from datetime import datetime
from clientes import Cliente
from estadisticas import agregar_envio_fecha

class Envio:
    def __init__(self, cliente: Cliente, orden_compra: int, servicio_envio: str, datos_motorizado: str, costo_servicio: float, fecha: str, enviado: bool):
        self.cliente = cliente
        self.orden_compra = orden_compra
        self.servicio_envio = servicio_envio
        self.datos_motorizado = datos_motorizado
        self.costo_servicio = costo_servicio
        self.fecha = fecha
        self.enviado = enviado

    def mostrar_detalles(self):
        if self.datos_motorizado != None:
            print(f"\nCliente: {self.cliente.nombre}\nOrden de compra: #{self.orden_compra}\nServicio de envio: {self.servicio_envio}\nDatos del motorizado: {self.datos_motorizado}\n Costo del servicio: {self.costo_servicio},\nFecha: {self.fecha}\nEnviado: {self.enviado}\n")
        else:
            print(f"\nCliente: {self.cliente.nombre}\nOrden de compra: #{self.orden_compra}\nServicio de envio: {self.servicio_envio}\n Costo del servicio: {self.costo_servicio},\nFecha: {self.fecha}\nEnviado: {self.enviado}")



# Actualiza la base de datos de envios indicando la nueva lista de envios
def actualizar_envios(envios: list[Envio]):
    envios_dic = []

    for envio in envios:
        dic = {
            "cliente": {
                "cedula": envio.cliente.cedula,
                "nombre": envio.cliente.nombre,
                "correo": envio.cliente.correo,
                "direccion_envio": envio.cliente.direccion_envio,
                "telefono": envio.cliente.telefono,
                "juridico": envio.cliente.juridico,
                "contacto_nombre": envio.cliente.contacto_nombre,
                "contacto_telefono": envio.cliente.contacto_telefono,
                "contacto_correo": envio.cliente.contacto_correo
            },
            "orden_compra": envio.orden_compra,
            "servicio_envio": envio.servicio_envio,
            "datos_motorizado": envio.datos_motorizado,
            "costo_servicio": envio.costo_servicio,
            "fecha": envio.fecha,
            "enviado": envio.enviado
        }
        envios_dic.append(dic)

    with open("assets/envios.json", "w", encoding="utf-8") as a:
            json.dump(envios_dic, a, indent=4, ensure_ascii=False)



# Busca los envios dependiendo de un filtro
def buscar_envios(envios: list[Envio], filtro: str, valor):
        for envio in envios:
            if filtro == "cliente" and valor.lower() in envio.cliente.nombre.lower():
                envio.mostrar_detalles()
            elif filtro == "fecha" and valor.lower() == envio.fecha.lower():
                envio.mostrar_detalles()



# Registra el envio en la base de datos
def registrarEnvio(envios: list[Envio], cliente: Cliente, orden_compra: int, servicio_envio: str, datos_motorizado: str, costo_servicio: float, enviado: bool, estadisticas: list):
    fecha = datetime.now().date()
    envio = Envio(cliente, orden_compra, servicio_envio, datos_motorizado, costo_servicio, str(fecha), enviado)
    envios.append(envio)
    actualizar_envios(envios)

    # Registra los valores a la base de datos de ESTADISTICAS
    agregar_envio_fecha(estadisticas)



# Funcion que se llama de el programa principal para buscar envios
def buscarEnvio(envios: list[Envio]):
    while True:
        print("1. Cliente\n2. Fecha")
        entrada_1 = input("\nSelecciona un filtro de busqueda: ")
        if entrada_1 == "1":
            entrada_2 = input("Nombre del cliente: ")
            buscar_envios(envios, "cliente", entrada_2)
            break
        elif entrada_1 == "2":
            entrada_2 = input("Fecha del pago en el siguiente formato ( año-mes-dia ): ")
            buscar_envios(envios, "fecha", entrada_2)
            break
        else:
            print("\nSelecciona una opcion valida...")
            continue
    print("")