from concurrent import futures

import grpc

import saludo_pb2
import saludo_pb2_grpc


class AuthInterceptor(grpc.ServerInterceptor):
    def __init__(self, token_valido):
        self.token_valido = token_valido

    def intercept_service(self, continuation, handler_call_details):
        handler = continuation(handler_call_details)
        if handler is None:
            return None

        if handler.unary_unary:
            def auth_unary_unary(request, context):
                metadata = dict(context.invocation_metadata())
                token = metadata.get("token")

                if token != self.token_valido:
                    context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token invalido")

                return handler.unary_unary(request, context)

            return grpc.unary_unary_rpc_method_handler(
                auth_unary_unary,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

        return handler


class SaludadorServicer(saludo_pb2_grpc.SaludadorServicer):
    def SayHello(self, request, context):
        _ = context
        mensaje = f"Hola, {request.nombre}."
        return saludo_pb2.SaludoReply(mensaje=mensaje)


def servir():
    interceptor = AuthInterceptor(token_valido="12345")
    servidor = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[interceptor],
    )
    saludo_pb2_grpc.add_SaludadorServicer_to_server(SaludadorServicer(), servidor)
    servidor.add_insecure_port("[::]:50051")
    servidor.start()
    print("Servidor gRPC en ejecucion en puerto 50051...")
    servidor.wait_for_termination()


if __name__ == "__main__":
    servir()
