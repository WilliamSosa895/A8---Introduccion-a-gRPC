import grpc

import consultorio_pb2
import consultorio_pb2_grpc


def main():
    canal = grpc.insecure_channel("localhost:50061")
    stub = consultorio_pb2_grpc.ConsultorioServiceStub(canal)

    while True:
        comando = input("Enter para actualizar pantalla (q para salir): ").strip().lower()
        if comando == "q":
            break
        print("--- Ultimos 3 llamados por especialidad ---")
        for bloque in stub.VerUltimos(consultorio_pb2.Vacio()):
            ultimos = ", ".join(bloque.codigos) if bloque.codigos else "sin llamados"
            print(f"{bloque.especialidad}: {ultimos}")


if __name__ == "__main__":
    main()
