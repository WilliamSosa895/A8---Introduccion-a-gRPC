# Practica 2: Tipos de Comunicacion en gRPC

Esta carpeta contiene la practica completa con:

- Caso base `grpc_biblioteca` con los 4 tipos RPC:
  - Unary RPC: `ConsultarLibro`
  - Server Streaming RPC: `ListarLibros`
  - Client Streaming RPC: `RegistrarLibros`
  - Bidirectional Streaming RPC: `TransaccionesTiempoReal`
- Ejercicio 1: `ejercicio1_consultorio`
- Ejercicio 2: `ejercicio2_callcenter`
- Ejercicio 3: `ejercicio3_soporte`

Cada ejercicio incluye:

- 1 servidor
- 3 clientes (`cliente_generador.py`, `cliente_escritorio.py`, `cliente_pantalla.py`)
- Persistencia simulada con JSON
- Logs de operaciones en consola del servidor
- Procesamiento concurrente con `ThreadPoolExecutor` y control de escritura con `threading.Lock`

## Requisitos

- Python 3.10 o superior
- Paquetes:

```powershell
pip install grpcio grpcio-tools
```

## Estructura

```text
practica2-grpc/
├── grpc_biblioteca/
│   ├── proto/
│   ├── server/
│   ├── client/
│   └── data/
├── ejercicio1_consultorio/
│   ├── proto/
│   ├── server/
│   ├── clients/
│   └── data/
├── ejercicio2_callcenter/
│   ├── proto/
│   ├── server/
│   ├── clients/
│   └── data/
├── ejercicio3_soporte/
│   ├── proto/
│   ├── server/
│   ├── clients/
│   └── data/
└── AUTOEVALUACION.md
```

## Ejecutar Caso Base: Biblioteca

1. Terminal 1 (servidor):

```powershell
Set-Location .\grpc_biblioteca\server
python .\server.py
```

2. Terminal 2 (cliente):

```powershell
Set-Location .\grpc_biblioteca\client
python .\menu_cliente.py
```

3. En el cliente ingresa `localhost:50052`.

## Ejecutar Ejercicio 1: Consultorio

1. Servidor:

```powershell
Set-Location .\ejercicio1_consultorio\server
python .\server.py
```

2. Cliente generador:

```powershell
Set-Location .\ejercicio1_consultorio\clients
python .\cliente_generador.py
```

3. Cliente escritorio:

```powershell
Set-Location .\ejercicio1_consultorio\clients
python .\cliente_escritorio.py
```

4. Cliente pantalla:

```powershell
Set-Location .\ejercicio1_consultorio\clients
python .\cliente_pantalla.py
```

Puerto: `50061`.

## Ejecutar Ejercicio 2: Call Center Multilingue

1. Servidor:

```powershell
Set-Location .\ejercicio2_callcenter\server
python .\server.py
```

2. Clientes:

```powershell
Set-Location .\ejercicio2_callcenter\clients
python .\cliente_generador.py
python .\cliente_escritorio.py
python .\cliente_pantalla.py
```

Puerto: `50062`.

## Ejecutar Ejercicio 3: Soporte por Prioridad

1. Servidor:

```powershell
Set-Location .\ejercicio3_soporte\server
python .\server.py
```

2. Clientes:

```powershell
Set-Location .\ejercicio3_soporte\clients
python .\cliente_generador.py
python .\cliente_escritorio.py
python .\cliente_pantalla.py
```

Puerto: `50063`.

## Pruebas en red local

En clientes de otras computadoras, cambia `localhost` por la IP de la maquina servidor, por ejemplo `192.168.1.35:50052`.

Asegura en firewall:

- Abrir puertos TCP 50052, 50061, 50062 y 50063.
- Permitir Python en red privada.

## Notas tecnicas

- Los `*_pb2.py` y `*_pb2_grpc.py` ya se generaron para server y cliente en cada modulo.
- Si regeneras archivos `.proto`, ejecuta `grpc_tools.protoc` de nuevo en los directorios correspondientes.
