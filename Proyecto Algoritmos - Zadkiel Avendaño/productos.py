# PROYECTO ALGORITMOS - ZADKIEL AVENDAÑO - C.I: 32695391

import json

class Producto():
    def __init__(self, id: int, name: str, description: str, price: float, category: str, inventory: int, compatible_vehicles: list[str]):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.inventory = inventory
        self.compatible_vehicles = compatible_vehicles
    
    def __str__(self):
        return f"Producto({self.id}), Nombre: {self.name}, Descripcion: {self.description}, Precio: {self.price}, Categoria: {self.category}, Inventario: {self.inventory}, Vehiculos compatibles: {self.compatible_vehicles}"



# Actualiza la base de datos de productos indicando la nueva lista de productos
def actualizar_productos(productos: list[Producto]):
    productos_dic = []

    for producto in productos:
        dic = {
            "id": productos.index(producto) + 1,
            "name": producto.name,
            "description": producto.description,
            "price": producto.price,
            "category": producto.category,
            "inventory": producto.inventory,
            "compatible_vehicles": producto.compatible_vehicles 
        }
        productos_dic.append(dic)

    with open("assets/productos.json", "w", encoding="utf-8") as a:
            json.dump(productos_dic, a, indent=4, ensure_ascii=False)



# Busca los productos dependiendo de un filtro
def buscar_productos(productos: list[Producto], filtro: str, valor):
        for producto in productos:
            if filtro == "categoria" and valor.lower() in producto.category.lower():
                print(producto)
            elif filtro == "precio" and producto.price <= valor:
                print(producto)
            elif filtro == "nombre" and valor.lower() in producto.name.lower():
                print(producto)
            elif filtro == "inventario" and producto.inventory >= valor:
                print(producto)



# Funcion que se llama para agregar productos desde el programa principal
def agregarProducto(productos: list[Producto]):
    print("\n-- Agregar Producto --")

    # Pregunta la informacion del producto nuevo
    nombre = input("\nEscribe el nombre del producto: ")
    descripcion = input("\nEscribe la descripcion del producto: ")
    categoria = input("\nIndica la categoria del producto: ")

    while True:
        precio = input("\nEscribe el precio del producto: ")
        try:
            precio = float(precio)
            break
        except ValueError:
            print("Indica un numero valido...")
            continue
            
    while True:
        inventario = input("\nIndica cuanto inventario hay del producto: ")
        if inventario.isnumeric():
            inventario = float(inventario)
            break
        else:
            print("Indica un numero valido...")
            continue

    # Crea el producto y lo añade a la lista de productos
    producto = Producto((len(productos)+1), nombre, descripcion, precio, categoria, inventario, [])
    productos.append(producto)

    # Agrega el nuevo producto a la base de datos
    actualizar_productos(productos)
    
    print(f"\nNuevo producto agregado:\n{producto}\n")



# Funcion que se llama para buscar productos desde el programa principal
def buscarProducto(productos: list[Producto]):
    while True:
        print("1. Categoria\n2. Precio\n3. Nombre\n4. Disponibilidad en inventario")
        entrada_1 = input("\nSelecciona un filtro de busqueda: ")
        if entrada_1 == "1":
            entrada_2 = input("Ingresa la categoria: ")
            buscar_productos(productos, "categoria", entrada_2)
            break
        elif entrada_1 == "2":
            entrada_2 = input("Ingresa el precio maximo: ")
            if not entrada_2.isnumeric():
                print("\nDebes ingresar un numero valido")
                continue
            buscar_productos(productos, "precio", float(entrada_2))
            break
        elif entrada_1 == "3":
            entrada_2 = input("Ingresa el nombre a buscar: ")
            buscar_productos(productos, "nombre", entrada_2)
            break
        elif entrada_1 == "4":
            entrada_2 = input("Ingresa el inventario minimo: ")
            if not entrada_2.isnumeric():
                print("\nDebes ingresar un numero valido")
                continue
            buscar_productos(productos, "inventario", int(entrada_2))
            break
        else:
            print("\nSelecciona una opcion valida...")
            continue
    print("")



# Funcion que se llama para modificar productos desde el programa principal
def modificarProducto(productos: list[Producto]):
    print("\n-- Modificar Producto --")

    # Pregunta el ID del producto a modificar
    while True:
        Id = input("Indica el ID del producto que deseas modificar: ")
        if Id.isnumeric():
            Id = int(Id)
            if Id <= len(productos):
                break
            else:
                print("Indica un numero valido...")
                continue
        else:
            print("Indica un numero valido...")
            continue

    # Pregunta la informacion del producto
    nombre = input("\nEscribe el nombre del producto: ")
    descripcion = input("\nEscribe la descripcion del producto: ")
    categoria = input("\nIndica la categoria del producto: ")

    while True:
        precio = input("\nEscribe el precio del producto: ")
        try:
            precio = float(precio)
            break
        except ValueError:
            print("Indica un numero valido...")
            continue
            
    while True:
        inventario = input("\nIndica cuanto inventario hay del producto: ")
        if inventario.isnumeric():
            inventario = float(inventario)
            break
        else:
            print("Indica un numero valido...")
            continue

    # Crea el producto y lo modifica de la lista de productos
    producto = Producto(Id, nombre, descripcion, precio, categoria, inventario, [])
    productos[Id-1] = producto

    # Agrega el producto modificado a la base de datos
    actualizar_productos(productos)
    
    print(f"\nProducto modificado:\n{producto}\n")



# Funcion que se llama para eliminar un producto desde el programa principal
def eliminarProducto(productos: list[Producto]):
    print("\n-- Eliminar Producto --")

    # Pregunta el ID del producto a modificar
    while True:
        Id = input("Indica el ID del producto que deseas eliminar: ")
        if Id.isnumeric():
            Id = int(Id)
            if Id <= len(productos):
                break
            else:
                print("Indica un numero valido...")
                continue
        else:
            print("Indica un numero valido...")
            continue
    
    while True:
        print(f"Producto seleccionado:\n{productos[Id-1]}")
        entrada = input("\nEscribe (ELIMINAR) para borrar el producto o presiona (ENTER) para cancelar la operacion: ")
        if entrada.lower() == "eliminar":
            del productos[Id-1]

            # Actualiza la base de datos con los productos restantes
            actualizar_productos(productos)

            print("\nProducto eliminado...\n")
            break
        else:
            print("\nOperacion cancelada...\n")
            break