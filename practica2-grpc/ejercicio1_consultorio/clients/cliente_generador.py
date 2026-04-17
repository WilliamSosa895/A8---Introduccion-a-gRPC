import grpc

import consultorio_pb2
import consultorio_pb2_grpc


def main():
    canal = grpc.insecure_channel("localhost:50061")
    stub = consultorio_pb2_grpc.ConsultorioServiceStub(canal)

    print("Generador de turnos (medicina_general/pediatria/odontologia)")
    while True:
        especialidad = input("Especialidad (enter para salir): ").strip().lower()
        if not especialidad:
            break
        paciente = input("Paciente: ").strip()
        try:
            turno = stub.GenerarTurno(
                consultorio_pb2.NuevoTurnoRequest(especialidad=especialidad, paciente=paciente)
            )
            print(f"Turno generado: {turno.codigo} - {turno.paciente}")
        except grpc.RpcError as error:
            print("Error:", error.details())


if __name__ == "__main__":
    main()
