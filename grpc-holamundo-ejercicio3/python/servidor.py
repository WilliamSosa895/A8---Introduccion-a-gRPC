from concurrent import futures
from datetime import datetime

import grpc

import saludo_pb2
import saludo_pb2_grpc


class SaludadorServicer(saludo_pb2_grpc.SaludadorServicer):
    def SayHello(self, request, context):
        nombre = request.nombre
        idioma = request.idioma.lower().strip()

        saludos = {
            "es": "Hola",
            "en": "Hello",
            "fr": "Bonjour",
        }

        saludo = saludos.get(idioma, "Hola")
        mensaje = f"{saludo}, {nombre}."
        return saludo_pb2.SaludoReply(mensaje=mensaje)

    def ObtenerHoraServidor(self, request, context):
        _ = request
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return saludo_pb2.HoraServidorReply(fecha_hora=fecha_hora)


def servir():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    saludo_pb2_grpc.add_SaludadorServicer_to_server(SaludadorServicer(), servidor)
    servidor.add_insecure_port("[::]:50051")
    servidor.start()
    print("Servidor gRPC en ejecucion en puerto 50051...")
    servidor.wait_for_termination()


if __name__ == "__main__":
    servir()
