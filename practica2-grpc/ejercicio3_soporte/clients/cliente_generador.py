import grpc

import soporte_pb2
import soporte_pb2_grpc


def main():
    canal = grpc.insecure_channel("localhost:50063")
    stub = soporte_pb2_grpc.SoporteServiceStub(canal)

    print("Generador de tickets (prioridad: baja/media/alta)")
    while True:
        prioridad = input("Prioridad (enter para salir): ").strip().lower()
        if not prioridad:
            break
        cliente = input("Cliente: ").strip()
        descripcion = input("Descripcion: ").strip()
        try:
            ticket = stub.GenerarTicket(
                soporte_pb2.NuevoTicketRequest(
                    prioridad=prioridad,
                    cliente=cliente,
                    descripcion=descripcion,
                )
            )
            print(f"Ticket generado: {ticket.codigo} ({ticket.prioridad})")
        except grpc.RpcError as error:
            print("Error:", error.details())


if __name__ == "__main__":
    main()
