from concurrent import futures
import grpc
import saludo_pb2
import saludo_pb2_grpc

class SaludadorServicer(saludo_pb2_grpc.SaludadorServicer):
    def SayHello(self, request, context):
        nombre = request.nombre
        mensaje = f"Hola, {nombre}. ¡Bienvenido a gRPC!"
        return saludo_pb2.SaludoReply(mensaje=mensaje)

def servir():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    saludo_pb2_grpc.add_SaludadorServicer_to_server(SaludadorServicer(), servidor)
    servidor.add_insecure_port('[::]:50051')
    servidor.start()
    print("Servidor gRPC en ejecución en puerto 50051...")
    servidor.wait_for_termination()

if __name__ == '__main__':
    servir()