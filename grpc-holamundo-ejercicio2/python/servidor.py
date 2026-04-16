from concurrent import futures

import grpc

import saludo_pb2
import saludo_pb2_grpc


class SaludadorServicer(saludo_pb2_grpc.SaludadorServicer):
    def SayHello(self, request, context):
        _ = context
        nombre = request.nombre.strip()

        if len(nombre) < 2:
            return saludo_pb2.SaludoReply(mensaje="Nombre no valido.")

        mensaje = f"Hola, {nombre}."
        return saludo_pb2.SaludoReply(mensaje=mensaje)


def servir():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    saludo_pb2_grpc.add_SaludadorServicer_to_server(SaludadorServicer(), servidor)
    servidor.add_insecure_port("[::]:50051")
    servidor.start()
    print("Servidor gRPC en ejecucion en puerto 50051...")
    servidor.wait_for_termination()


if __name__ == "__main__":
    servir()
