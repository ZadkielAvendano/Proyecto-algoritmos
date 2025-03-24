# PROYECTO ALGORITMOS - ZADKIEL AVENDAÑO - C.I: 32695391

import json

# Clase Cliente para manejar la información de los clientes
class Cliente:
    def __init__(self, nombre: str, cedula: str, correo: str, direccion_envio: str, telefono: str, juridico: bool, contacto_nombre: str, contacto_telefono: str, contacto_correo: str) -> None:
        self.nombre = nombre
        self.cedula = cedula
        self.correo = correo
        self.direccion_envio = direccion_envio
        self.telefono = telefono
        self.juridico = juridico
        self.contacto_nombre = contacto_nombre
        self.contacto_telefono = contacto_telefono
        self.contacto_correo = contacto_correo

    # Método para mostrar la información del cliente
    def Show(self):
        if not self.juridico:
            print(f"Nombre: {self.nombre}, Cedula: {self.cedula}, Correo: {self.correo}, Direccion de envio: {self.direccion_envio}, Telefono: {self.telefono}, Juridico: {self.juridico}")
        else:
            print(f"Nombre: {self.nombre}, Cedula: {self.cedula}, Correo: {self.correo}, Direccion de envio: {self.direccion_envio}, Telefono: {self.telefono}, Juridico: {self.juridico}, Nombre de contacto: {self.contacto_nombre}, Telefono de contacto: {self.contacto_telefono}, Correo de contacto: {self.contacto_correo}")

# Funcion para actualizar la base de datos de clientes
def actualizar_clientes(clientes: list[Cliente]):
    clientes_dic = []

    # Convertir cada objeto Cliente a un diccionario
    for cliente in clientes:
        dic = {
            "nombre": cliente.nombre,
            "cedula": cliente.cedula,
            "correo": cliente.correo,
            "direccion_envio": cliente.direccion_envio,
            "telefono": cliente.telefono,
            "juridico": cliente.juridico,
        }

        # Agregar datos de contacto si el cliente es jurídico
        if cliente.juridico:
            dic["contacto_nombre"] = cliente.contacto_nombre
            dic["contacto_telefono"] = cliente.contacto_telefono
            dic["contacto_correo"] = cliente.contacto_correo

        clientes_dic.append(dic)

    # Guardar la lista de clientes en un archivo JSON
    with open("assets/clientes.json", "w", encoding="utf-8") as a:
        json.dump(clientes_dic, a, indent=4, ensure_ascii=False)

# Función para registrar un nuevo cliente
def registrarCliente(clientes: list[Cliente]):
    print("\n-- Registrar Cliente --")

    # Obtener información del nuevo cliente
    nombre = input("\nNombre del cliente: ")
    correo = input("\nCorreo electronico: ")
    direccion_envio = input("\nDireccion de envio: ")
    telefono = input("\nNumero telefonico: ")
    
    while True:
        print("\n1. Cedula\n2. RIF")
        juridico = input("\nEs persona natural o juridico: ")

        if juridico == "1":
            juridico = False
            cedula = input("\nIngresa la cedula del cliente: ")
            contacto_nombre = None
            contacto_telefono = None
            contacto_correo = None
            break
        elif juridico == "2":
            juridico = True
            cedula = input("\nIngresa el RIF del cliente: ")
            contacto_nombre = input("\nNombre de contacto: ")
            contacto_telefono = input("\nTelefono de contacto: ")
            contacto_correo = input("\nCorreo de contacto: ")
            break
        else:
            print("Elige una opcion valida...")
            continue

    # Crear el objeto Cliente y agregarlo a la lista
    cliente = Cliente(nombre, cedula, correo, direccion_envio, telefono, juridico, contacto_nombre, contacto_telefono, contacto_correo)
    clientes.append(cliente)
    actualizar_clientes(clientes)
    
    # Mostrar información del nuevo cliente registrado
    print(f"\nNuevo cliente registrado:\n")
    cliente.Show()

# Función para modificar un cliente existente
def modificarCliente(clientes: list[Cliente]):
    cedula = input("\nIngrese la cedula o RIF del cliente a modificar: ")
    cliente_encontrado = None

    # Buscar el cliente por su cedula o RIF
    for cliente in clientes:
        if cliente.cedula == cedula:
            cliente_encontrado = cliente
            break

    if cliente_encontrado:
        # Solicitar nuevos datos para el cliente encontrado
        print("\nCliente encontrado. Ingrese los nuevos datos.")
        cliente_encontrado.nombre = input("\nNuevo nombre (dejar vacío para mantener actual): ") or cliente_encontrado.nombre
        cliente_encontrado.correo = input("\nNuevo correo (dejar vacío para mantener actual): ") or cliente_encontrado.correo
        cliente_encontrado.direccion_envio = input("\nNueva dirección de envío (dejar vacío para mantener actual): ") or cliente_encontrado.direccion_envio
        cliente_encontrado.telefono = input("\nNuevo teléfono (dejar vacío para mantener actual): ") or cliente_encontrado.telefono
        if cliente_encontrado.juridico:
            cliente_encontrado.contacto_nombre = input("\nNuevo nombre de contacto (dejar vacío para mantener actual): ") or cliente_encontrado.contacto_nombre
            cliente_encontrado.contacto_telefono = input("\nNuevo teléfono de contacto (dejar vacío para mantener actual): ") or cliente_encontrado.contacto_telefono
            cliente_encontrado.contacto_correo = input("\nNuevo correo de contacto (dejar vacío para mantener actual): ") or cliente_encontrado.contacto_correo
        
        actualizar_clientes(clientes)
        print("\nCliente modificado exitosamente.")
    else:
        print("\nCliente no encontrado.")

# Función para eliminar un cliente
def eliminarCliente(clientes: list[Cliente]):
    cedula = input("\nIngrese la cedula o RIF del cliente a eliminar: ")
    cliente_encontrado = None

    # Buscar el cliente por su cedula o RIF
    for cliente in clientes:
        if cliente.cedula == cedula:
            cliente_encontrado = cliente
            break

    if cliente_encontrado:
        print(f"\nCliente encontrado: {cliente_encontrado.nombre}")
        confirmacion = input("\n¿Está seguro de que desea eliminar este cliente? (si/no): ").lower()
        if confirmacion == "si":
            # Eliminar el cliente encontrado de la lista
            clientes.remove(cliente_encontrado)
            actualizar_clientes(clientes)
            print("\nCliente eliminado exitosamente.")
        else:
            print("\nOperación cancelada.")
    else:
        print("\nCliente no encontrado.")


# Función para buscar un cliente
def buscarCliente(clientes: list[Cliente]):
    print("\n-- Buscar Cliente --")
    print("1. Buscar por Cédula o RIF\n2. Buscar por Correo")
    
    filtro = input("Elige un filtro de búsqueda: ")
    cliente_encontrado = None
    
    if filtro == "1":
        cedula = input("\nIngrese la cédula o RIF del cliente: ")
        for cliente in clientes:
            if cliente.cedula == cedula:
                cliente_encontrado = cliente
                break
    elif filtro == "2":
        correo = input("\nIngrese el correo del cliente: ")
        for cliente in clientes:
            if cliente.correo == correo:
                cliente_encontrado = cliente
                break
    else:
        print("\nOpción no válida. Por favor, elija 1 o 2.\n")
        return

    if cliente_encontrado:
        print("\nCliente encontrado:")
        cliente_encontrado.Show()
    else:
        print("\nCliente no encontrado.")
    print("")
