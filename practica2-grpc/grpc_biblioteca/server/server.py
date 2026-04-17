from concurrent import futures
import json
import os
import threading
import time

import grpc

import library_pb2
import library_pb2_grpc

LIBROS_PATH = os.path.join(os.path.dirname(__file__), "../data/libros.json")
LOCK = threading.Lock()


def cargar_libros():
    with LOCK, open(LIBROS_PATH, "r", encoding="utf-8") as file:
        return {libro["id"]: libro for libro in json.load(file)}


def guardar_libros(libros_dict):
    with LOCK, open(LIBROS_PATH, "w", encoding="utf-8") as file:
        libros = list(libros_dict.values())
        json.dump(libros, file, indent=2, ensure_ascii=False)


def log_operacion(msg):
    print(f"[LOG] {time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}")


class BibliotecaServiceServicer(library_pb2_grpc.BibliotecaServiceServicer):
    def ConsultarLibro(self, request, context):
        libros = cargar_libros()
        libro = libros.get(request.id)
        if libro:
            log_operacion(f"Consulta libro ID {request.id}")
            return library_pb2.Libro(id=libro["id"], titulo=libro["titulo"], autor=libro["autor"])

        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Libro no encontrado")
        return library_pb2.Libro()

    def ListarLibros(self, request, context):
        _ = request
        _ = context
        libros = cargar_libros()
        for libro in libros.values():
            log_operacion(f"Envia libro ID {libro['id']}")
            yield library_pb2.Libro(id=libro["id"], titulo=libro["titulo"], autor=libro["autor"])

    def RegistrarLibros(self, request_iterator, context):
        _ = context
        libros = cargar_libros()
        count = 0
        for libro in request_iterator:
            libros[libro.id] = {"id": libro.id, "titulo": libro.titulo, "autor": libro.autor}
            log_operacion(f"Registro libro ID {libro.id}")
            count += 1
        guardar_libros(libros)
        return library_pb2.ResumenRegistro(total_registrados=count)

    def TransaccionesTiempoReal(self, request_iterator, context):
        _ = context
        for transaccion in request_iterator:
            tipo = transaccion.tipo
            id_libro = transaccion.id_libro
            usuario = transaccion.usuario

            if tipo == "prestamo":
                mensaje = f"{usuario} ha tomado prestado el libro {id_libro}"
            elif tipo == "devolucion":
                mensaje = f"{usuario} ha devuelto el libro {id_libro}"
            else:
                mensaje = f"Transaccion desconocida para el libro {id_libro}"

            log_operacion(mensaje)
            yield library_pb2.Confirmacion(mensaje=mensaje)


def servir():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    library_pb2_grpc.add_BibliotecaServiceServicer_to_server(BibliotecaServiceServicer(), servidor)
    servidor.add_insecure_port("[::]:50052")
    print("Servidor Biblioteca gRPC escuchando en puerto 50052...")
    servidor.start()
    servidor.wait_for_termination()


if __name__ == "__main__":
    servir()
