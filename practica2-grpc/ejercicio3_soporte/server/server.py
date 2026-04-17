from concurrent import futures
import json
import os
import threading
import time

import grpc

import soporte_pb2
import soporte_pb2_grpc

ESTADO_PATH = os.path.join(os.path.dirname(__file__), "../data/estado.json")
LOCK = threading.Lock()
PESO_PRIORIDAD = {"alta": 0, "media": 1, "baja": 2}


def log(msg):
    print(f"[LOG] {time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}")


def cargar_estado():
    with LOCK, open(ESTADO_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def guardar_estado(estado):
    with LOCK, open(ESTADO_PATH, "w", encoding="utf-8") as file:
        json.dump(estado, file, indent=2, ensure_ascii=False)


class SoporteService(soporte_pb2_grpc.SoporteServiceServicer):
    def GenerarTicket(self, request, context):
        prioridad = request.prioridad.strip().lower()
        cliente = request.cliente.strip()
        descripcion = request.descripcion.strip()

        if prioridad not in PESO_PRIORIDAD:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Prioridad no valida: baja/media/alta")
        if not cliente:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Cliente requerido")

        estado = cargar_estado()
        numero = estado["next_num"]
        estado["next_num"] += 1
        codigo = f"TK-{numero:04d}"

        ticket = {
            "codigo": codigo,
            "prioridad": prioridad,
            "cliente": cliente,
            "descripcion": descripcion,
            "creado": time.time(),
        }
        estado["tickets"].append(ticket)
        estado["tickets"].sort(key=lambda item: (PESO_PRIORIDAD[item["prioridad"]], item["creado"]))
        guardar_estado(estado)

        log(f"Ticket {codigo} creado con prioridad {prioridad}")
        return soporte_pb2.Ticket(
            codigo=codigo,
            prioridad=prioridad,
            cliente=cliente,
            descripcion=descripcion,
        )

    def AtenderSiguiente(self, request, context):
        agente = request.agente.strip() or "agente"
        _ = context

        estado = cargar_estado()
        if not estado["tickets"]:
            mensaje = "Sin tickets pendientes"
            log(mensaje)
            return soporte_pb2.TicketAtendido(hay_ticket=False, mensaje=mensaje)

        ticket = estado["tickets"].pop(0)
        guardar_estado(estado)

        mensaje = f"{agente} atiende {ticket['codigo']} ({ticket['prioridad']})"
        log(mensaje)
        return soporte_pb2.TicketAtendido(
            hay_ticket=True,
            mensaje=mensaje,
            ticket=soporte_pb2.Ticket(
                codigo=ticket["codigo"],
                prioridad=ticket["prioridad"],
                cliente=ticket["cliente"],
                descripcion=ticket["descripcion"],
            ),
        )

    def VerPendientes(self, request, context):
        _ = request
        _ = context
        estado = cargar_estado()
        alta = sum(1 for ticket in estado["tickets"] if ticket["prioridad"] == "alta")
        media = sum(1 for ticket in estado["tickets"] if ticket["prioridad"] == "media")
        baja = sum(1 for ticket in estado["tickets"] if ticket["prioridad"] == "baja")
        return soporte_pb2.ResumenPendientes(alta=alta, media=media, baja=baja)


def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    soporte_pb2_grpc.add_SoporteServiceServicer_to_server(SoporteService(), server)
    server.add_insecure_port("[::]:50063")
    log("Servidor de soporte escuchando en puerto 50063")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    servir()
