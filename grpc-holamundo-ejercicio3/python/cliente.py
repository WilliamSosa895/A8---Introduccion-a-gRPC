import grpc
from google.protobuf import empty_pb2

import saludo_pb2
import saludo_pb2_grpc


def run():
    canal = grpc.insecure_channel("localhost:50051")
    stub = saludo_pb2_grpc.SaludadorStub(canal)

    nombre_usuario = input("Ingresa tu nombre: ").strip()
    idioma = input("Ingresa idioma (es/en/fr): ").strip().lower()

    respuesta_saludo = stub.SayHello(saludo_pb2.SaludoRequest(nombre=nombre_usuario, idioma=idioma))
    print("Respuesta del servidor:", respuesta_saludo.mensaje)

    respuesta_hora = stub.ObtenerHoraServidor(empty_pb2.Empty())
    print("Fecha y hora del servidor:", respuesta_hora.fecha_hora)


if __name__ == "__main__":
    run()
