import grpc
from google.protobuf import empty_pb2

import saludo_pb2
import saludo_pb2_grpc


def run():
    canal = grpc.insecure_channel("localhost:50051")
    stub = saludo_pb2_grpc.SaludadorStub(canal)

    # Prueba de SayHello (metodo previo)
    nombre_usuario = input("Ingresa tu nombre: ").strip()
    idioma = input("Ingresa idioma (es/en/fr): ").strip().lower()
    respuesta_saludo = stub.SayHello(saludo_pb2.SaludoRequest(nombre=nombre_usuario, idioma=idioma))
    print("Respuesta del servidor:", respuesta_saludo.mensaje)

    # Prueba de ObtenerHoraServidor (metodo previo)
    respuesta_hora = stub.ObtenerHoraServidor(empty_pb2.Empty())
    print("Fecha y hora del servidor:", respuesta_hora.fecha_hora)

    # Prueba de SaludarLista (nuevo metodo)
    nombres_entrada = input("Ingresa nombres separados por coma (ej: Ana,Luis,Zoe): ").strip()
    lista_nombres = [n.strip() for n in nombres_entrada.split(",") if n.strip()]

    respuesta_lista = stub.SaludarLista(saludo_pb2.SaludarListaRequest(nombres=lista_nombres))
    print("Respuesta de SaludarLista:", respuesta_lista.mensaje)


if __name__ == "__main__":
    run()
