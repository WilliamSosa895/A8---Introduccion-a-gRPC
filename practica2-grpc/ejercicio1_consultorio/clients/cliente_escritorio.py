import grpc

import consultorio_pb2
import consultorio_pb2_grpc


def main():
    canal = grpc.insecure_channel("localhost:50061")
    stub = consultorio_pb2_grpc.ConsultorioServiceStub(canal)

    especialidad = input("Especialidad del escritorio: ").strip().lower()
    escritorio = input("Nombre del escritorio: ").strip() or "escritorio"

    while True:
        comando = input("Enter para atender siguiente (q para salir): ").strip().lower()
        if comando == "q":
            break
        try:
            respuesta = stub.AtenderSiguiente(
                consultorio_pb2.AtenderRequest(especialidad=especialidad, escritorio=escritorio)
            )
            print(respuesta.mensaje)
        except grpc.RpcError as error:
            print("Error:", error.details())


if __name__ == "__main__":
    main()
