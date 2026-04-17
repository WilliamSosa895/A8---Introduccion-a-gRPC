import grpc

import callcenter_pb2
import callcenter_pb2_grpc


def main():
    canal = grpc.insecure_channel("localhost:50062")
    stub = callcenter_pb2_grpc.CallCenterServiceStub(canal)

    print("Generador de tickets (idiomas: es, en, fr)")
    while True:
        idioma = input("Idioma (enter para salir): ").strip().lower()
        if not idioma:
            break
        cliente = input("Cliente: ").strip()
        try:
            ticket = stub.GenerarTicket(callcenter_pb2.NuevoTicketRequest(idioma=idioma, cliente=cliente))
            print(f"Ticket generado: {ticket.codigo}")
        except grpc.RpcError as error:
            print("Error:", error.details())


if __name__ == "__main__":
    main()
