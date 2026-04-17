import grpc

import soporte_pb2
import soporte_pb2_grpc


def main():
    canal = grpc.insecure_channel("localhost:50063")
    stub = soporte_pb2_grpc.SoporteServiceStub(canal)

    agente = input("Nombre del agente: ").strip() or "agente"

    while True:
        comando = input("Enter para atender siguiente (q para salir): ").strip().lower()
        if comando == "q":
            break
        respuesta = stub.AtenderSiguiente(soporte_pb2.AtenderRequest(agente=agente))
        print(respuesta.mensaje)


if __name__ == "__main__":
    main()
