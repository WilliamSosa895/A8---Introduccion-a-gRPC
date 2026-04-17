from concurrent import futures
import json
import os
import threading
import time

import grpc

import consultorio_pb2
import consultorio_pb2_grpc

ESTADO_PATH = os.path.join(os.path.dirname(__file__), "../data/estado.json")
LOCK = threading.Lock()
ESPECIALIDADES = {"medicina_general": "MG", "pediatria": "PD", "odontologia": "OD"}


def log(msg):
    print(f"[LOG] {time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}")


def cargar_estado():
    with LOCK, open(ESTADO_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def guardar_estado(estado):
    with LOCK, open(ESTADO_PATH, "w", encoding="utf-8") as file:
        json.dump(estado, file, indent=2, ensure_ascii=False)


class ConsultorioService(consultorio_pb2_grpc.ConsultorioServiceServicer):
    def GenerarTurno(self, request, context):
        especialidad = request.especialidad.strip().lower()
        paciente = request.paciente.strip()

        if especialidad not in ESPECIALIDADES:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Especialidad no valida")
        if not paciente:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Paciente requerido")

        estado = cargar_estado()
        numero = estado["next_num"][especialidad]
        estado["next_num"][especialidad] += 1
        codigo = f"{ESPECIALIDADES[especialidad]}-{numero:03d}"

        turno = {"codigo": codigo, "especialidad": especialidad, "paciente": paciente}
        estado["colas"][especialidad].append(turno)
        guardar_estado(estado)

        log(f"Generado turno {codigo} para {especialidad} ({paciente})")
        return consultorio_pb2.Turno(codigo=codigo, especialidad=especialidad, paciente=paciente)

    def AtenderSiguiente(self, request, context):
        especialidad = request.especialidad.strip().lower()
        escritorio = request.escritorio.strip() or "escritorio"

        if especialidad not in ESPECIALIDADES:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Especialidad no valida")

        estado = cargar_estado()
        cola = estado["colas"][especialidad]

        if not cola:
            mensaje = f"Sin turnos pendientes en {especialidad}"
            log(mensaje)
            return consultorio_pb2.TurnoAtendido(hay_turno=False, mensaje=mensaje)

        siguiente = cola.pop(0)
        ultimos = estado["ultimos"][especialidad]
        ultimos.append(siguiente["codigo"])
        estado["ultimos"][especialidad] = ultimos[-3:]
        guardar_estado(estado)

        mensaje = f"{escritorio} atiende {siguiente['codigo']} ({siguiente['paciente']})"
        log(mensaje)
        return consultorio_pb2.TurnoAtendido(
            hay_turno=True,
            mensaje=mensaje,
            turno=consultorio_pb2.Turno(
                codigo=siguiente["codigo"],
                especialidad=siguiente["especialidad"],
                paciente=siguiente["paciente"],
            ),
        )

    def VerUltimos(self, request, context):
        _ = request
        _ = context
        estado = cargar_estado()
        for especialidad in ESPECIALIDADES:
            yield consultorio_pb2.UltimoLlamado(
                especialidad=especialidad,
                codigos=estado["ultimos"].get(especialidad, []),
            )


def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    consultorio_pb2_grpc.add_ConsultorioServiceServicer_to_server(ConsultorioService(), server)
    server.add_insecure_port("[::]:50061")
    log("Servidor consultorio escuchando en puerto 50061")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    servir()
