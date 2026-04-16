import grpc

import saludo_pb2
import saludo_pb2_grpc


def run():
    canal = grpc.insecure_channel("localhost:50051")
    stub = saludo_pb2_grpc.SaludadorStub(canal)

    nombre_usuario = input("Ingresa tu nombre: ")
    respuesta = stub.SayHello(saludo_pb2.SaludoRequest(nombre=nombre_usuario))
    print("Respuesta del servidor:", respuesta.mensaje)


if __name__ == "__main__":
    run()
