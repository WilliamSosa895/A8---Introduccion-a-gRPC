import grpc

import saludo_pb2
import saludo_pb2_grpc


def run():
    canal = grpc.insecure_channel("localhost:50051")
    stub = saludo_pb2_grpc.SaludadorStub(canal)

    nombre_usuario = input("Ingresa tu nombre: ").strip()
    token = input("Ingresa token (deja vacio para enviar sin token): ").strip()

    metadata = [("token", token)] if token else None

    try:
        respuesta = stub.SayHello(saludo_pb2.SaludoRequest(nombre=nombre_usuario), metadata=metadata)
        print("Respuesta del servidor:", respuesta.mensaje)
    except grpc.RpcError as error:
        print("ERROR", error.code().name)


if __name__ == "__main__":
    run()
