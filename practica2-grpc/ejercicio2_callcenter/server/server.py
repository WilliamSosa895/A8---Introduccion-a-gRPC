from concurrent import futures
import json
import os
import threading
import time

import grpc

import callcenter_pb2
import callcenter_pb2_grpc

ESTADO_PATH = os.path.join(os.path.dirname(__file__), "../data/estado.json")
LOCK = threading.Lock()
IDIOMAS = {"es": "ES", "en": "EN", "fr": "FR"}


def log(msg):
    print(f"[LOG] {time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}")


def cargar_estado():
    with LOCK, open(ESTADO_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def guardar_estado(estado):
    with LOCK, open(ESTADO_PATH, "w", encoding="utf-8") as file:
        json.dump(estado, file, indent=2, ensure_ascii=False)


class CallCenterService(callcenter_pb2_grpc.CallCenterServiceServicer):
    def GenerarTicket(self, request, context):
        idioma = request.idioma.strip().lower()
        cliente = request.cliente.strip()

        if idioma not in IDIOMAS:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Idioma no valido: use es/en/fr")
        if not cliente:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Cliente requerido")

        estado = cargar_estado()
        numero = estado["next_num"][idioma]
        estado["next_num"][idioma] += 1
        codigo = f"{IDIOMAS[idioma]}-{numero:03d}"
        ticket = {"codigo": codigo, "idioma": idioma, "cliente": cliente}
        estado["colas"][idioma].append(ticket)
        guardar_estado(estado)

        log(f"Ticket {codigo} generado para idioma {idioma} ({cliente})")
        return callcenter_pb2.Ticket(codigo=codigo, idioma=idioma, cliente=cliente)

    def AtenderPorIdioma(self, request, context):
        idioma = request.idioma.strip().lower()
        agente = request.agente.strip() or "agente"

        if idioma not in IDIOMAS:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Idioma no valido: use es/en/fr")

        estado = cargar_estado()
        cola = estado["colas"][idioma]
        if not cola:
            mensaje = f"Sin tickets pendientes para idioma {idioma}"
            log(mensaje)
            return callcenter_pb2.TicketAtendido(hay_ticket=False, mensaje=mensaje)

        ticket = cola.pop(0)
        ultimos = estado["ultimos"][idioma]
        ultimos.append(ticket["codigo"])
        estado["ultimos"][idioma] = ultimos[-3:]
        guardar_estado(estado)

        mensaje = f"{agente} atiende ticket {ticket['codigo']} ({ticket['cliente']})"
        log(mensaje)
        return callcenter_pb2.TicketAtendido(
            hay_ticket=True,
            mensaje=mensaje,
            ticket=callcenter_pb2.Ticket(
                codigo=ticket["codigo"],
                idioma=ticket["idioma"],
                cliente=ticket["cliente"],
            ),
        )

    def VerEstadoIdiomas(self, request, context):
        _ = request
        _ = context
        estado = cargar_estado()
        for idioma in ["es", "en", "fr"]:
            yield callcenter_pb2.EstadoIdioma(
                idioma=idioma,
                pendientes=len(estado["colas"][idioma]),
                ultimos=estado["ultimos"][idioma],
            )


def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    callcenter_pb2_grpc.add_CallCenterServiceServicer_to_server(CallCenterService(), server)
    server.add_insecure_port("[::]:50062")
    log("Servidor call center escuchando en puerto 50062")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    servir()
