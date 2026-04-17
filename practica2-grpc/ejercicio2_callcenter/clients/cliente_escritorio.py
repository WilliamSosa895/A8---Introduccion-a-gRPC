import grpc

import callcenter_pb2
import callcenter_pb2_grpc


def main():
    canal = grpc.insecure_channel("localhost:50062")
    stub = callcenter_pb2_grpc.CallCenterServiceStub(canal)

    idioma = input("Idioma del escritorio (es/en/fr): ").strip().lower()
    agente = input("Nombre del agente: ").strip() or "agente"

    while True:
        comando = input("Enter para atender siguiente (q para salir): ").strip().lower()
        if comando == "q":
            break
        try:
            respuesta = stub.AtenderPorIdioma(callcenter_pb2.AtenderIdiomaRequest(idioma=idioma, agente=agente))
            print(respuesta.mensaje)
        except grpc.RpcError as error:
            print("Error:", error.details())


if __name__ == "__main__":
    main()
