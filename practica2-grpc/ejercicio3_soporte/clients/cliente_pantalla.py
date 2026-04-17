import grpc

import soporte_pb2
import soporte_pb2_grpc


def main():
    canal = grpc.insecure_channel("localhost:50063")
    stub = soporte_pb2_grpc.SoporteServiceStub(canal)

    while True:
        comando = input("Enter para refrescar pendientes (q para salir): ").strip().lower()
        if comando == "q":
            break
        resumen = stub.VerPendientes(soporte_pb2.Vacio())
        print("Pendientes por prioridad:")
        print(f"alta={resumen.alta}, media={resumen.media}, baja={resumen.baja}")


if __name__ == "__main__":
    main()
