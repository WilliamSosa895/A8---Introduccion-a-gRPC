import grpc

import callcenter_pb2
import callcenter_pb2_grpc


def main():
    canal = grpc.insecure_channel("localhost:50062")
    stub = callcenter_pb2_grpc.CallCenterServiceStub(canal)

    while True:
        comando = input("Enter para refrescar estado (q para salir): ").strip().lower()
        if comando == "q":
            break
        print("--- Estado por idioma ---")
        for estado in stub.VerEstadoIdiomas(callcenter_pb2.Vacio()):
            ultimos = ", ".join(estado.ultimos) if estado.ultimos else "sin atenciones"
            print(f"{estado.idioma}: pendientes={estado.pendientes}, ultimos={ultimos}")


if __name__ == "__main__":
    main()
