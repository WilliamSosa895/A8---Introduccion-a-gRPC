import grpc

import library_pb2
import library_pb2_grpc


def consultar_libro(stub):
    id_libro = int(input("ID del libro a consultar: "))
    try:
        respuesta = stub.ConsultarLibro(library_pb2.LibroID(id=id_libro))
        print(f"Titulo: {respuesta.titulo}, Autor: {respuesta.autor}")
    except grpc.RpcError as error:
        print("Error:", error.details())


def listar_libros(stub):
    print("Listado de libros:")
    for libro in stub.ListarLibros(library_pb2.Vacio()):
        print(f"{libro.id} - {libro.titulo} ({libro.autor})")


def registrar_libros(stub):
    def generar_libros():
        while True:
            id_ = input("ID del libro (enter para terminar): ").strip()
            if not id_:
                break
            titulo = input("Titulo: ").strip()
            autor = input("Autor: ").strip()
            yield library_pb2.Libro(id=int(id_), titulo=titulo, autor=autor)

    respuesta = stub.RegistrarLibros(generar_libros())
    print(f"Total registrados: {respuesta.total_registrados}")


def transacciones_tiempo_real(stub):
    def enviar_transacciones():
        while True:
            tipo = input("Tipo de transaccion (prestamo/devolucion, enter para terminar): ").strip()
            if not tipo:
                break
            id_libro = int(input("ID del libro: "))
            usuario = input("Usuario: ").strip()
            yield library_pb2.Transaccion(tipo=tipo, id_libro=id_libro, usuario=usuario)

    respuestas = stub.TransaccionesTiempoReal(enviar_transacciones())
    for respuesta in respuestas:
        print("Confirmacion:", respuesta.mensaje)


def main():
    direccion = input("Direccion del servidor (ej. localhost:50052): ").strip()
    canal = grpc.insecure_channel(direccion)
    stub = library_pb2_grpc.BibliotecaServiceStub(canal)

    while True:
        print("\n--- Menu Biblioteca ---")
        print("1. Consultar libro")
        print("2. Listar libros")
        print("3. Registrar libros")
        print("4. Transacciones en tiempo real")
        print("5. Salir")

        opcion = input("Selecciona una opcion: ").strip()
        if opcion == "1":
            consultar_libro(stub)
        elif opcion == "2":
            listar_libros(stub)
        elif opcion == "3":
            registrar_libros(stub)
        elif opcion == "4":
            transacciones_tiempo_real(stub)
        elif opcion == "5":
            print("Hasta luego.")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()
