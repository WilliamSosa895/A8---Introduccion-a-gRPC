# Autoevaluacion - Practica 2

## 1) Que ventajas ofrece gRPC sobre otras tecnologias como REST o WebSockets?

gRPC ofrece contratos formales con `.proto`, alto rendimiento por serializacion binaria (Protocol Buffers) y HTTP/2 con multiplexacion. En comparacion con REST, reduce payload y mejora tipado. En comparacion con WebSockets, mantiene un modelo RPC claro con soporte nativo para unary y streaming.

## 2) Cual es la principal diferencia entre una llamada Unary y Server Streaming?

Unary envia 1 solicitud y recibe 1 respuesta. Server Streaming envia 1 solicitud y recibe multiples respuestas secuenciales desde el servidor.

## 3) Que situaciones reales justifican el uso de Client Streaming?

Cuando el cliente necesita enviar lotes de datos: carga masiva de registros, telemetria acumulada, logs de dispositivos o sincronizacion offline de eventos.

## 4) Cuando conviene usar Bidirectional Streaming en una aplicacion?

Cuando ambos lados requieren intercambio continuo y asincorno: chat, monitoreo en vivo, transacciones en tiempo real o control de dispositivos.

## 5) Como influye el uso de HTTP/2 en el rendimiento de gRPC?

Permite multiplexar varias llamadas en una misma conexion TCP, reduce overhead de cabeceras, mejora latencia y aprovecha mejor el ancho de banda.

## 6) Que tipo de RPC resulta mas simple de implementar y por que?

Unary RPC, porque su flujo request-response es directo y no requiere manejar iteradores de entrada/salida.

## 7) Como gestionaste la conexion del cliente con el servidor usando una IP local?

Se parametrizo la direccion del canal gRPC (`grpc.insecure_channel("IP:PUERTO")`) y se probaron conexiones desde clientes locales y remotos en la LAN.

## 8) Que dificultades tecnicas enfrentaste al distribuir los clientes en varias computadoras?

Las principales fueron firewall, puertos cerrados, IPs cambiantes por DHCP y dependencias de Python distintas entre equipos.

## 9) Como validaste que el servidor estaba respondiendo correctamente a multiples clientes?

Se ejecutaron clientes de forma concurrente y se verifico en logs del servidor que las operaciones llegaban en paralelo sin corrupcion de datos, usando `threading.Lock` para persistencia segura.

## 10) Que aprendizajes obtuviste sobre la concurrencia y el procesamiento simultaneo?

Que no basta con hilos en el servidor; tambien hay que proteger secciones criticas de lectura/escritura para evitar condiciones de carrera.

## 11) Que implica disenar un protocolo de comunicacion en un archivo .proto?

Definir mensajes y servicios de forma explicita, versionable y compatible entre cliente y servidor. Es el contrato principal de todo el sistema distribuido.

## 12) Que implicaciones tiene usar streams continuos en terminos de consumo de recursos?

Mayor uso sostenido de memoria y sockets abiertos, necesidad de timeouts, control de flujo y manejo cuidadoso de errores de red.

## 13) Como mantuviste el codigo organizado para cada tipo de cliente?

Separando clientes por rol (`generador`, `escritorio`, `pantalla`) y manteniendo carpetas por ejercicio, lo que facilita pruebas independientes y despliegue distribuido.

## 14) Que similitudes y diferencias encontraste entre los distintos tipos de RPC?

Todos comparten el contrato `.proto` y stubs. Se diferencian en direccion y cantidad de mensajes: unary (1-1), server streaming (1-N), client streaming (N-1), bidireccional (N-N).

## 15) Como se relaciona esta practica con aplicaciones del mundo real como salud, transporte o energia?

Replica patrones reales: turnos medicos, atencion de incidencias, gestion de colas y eventos en tiempo real. Esto es directamente aplicable a sistemas de citas, despacho de flotas y monitoreo de redes electricas.
