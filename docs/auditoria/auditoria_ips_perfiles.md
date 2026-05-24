# AuditorÃ­a de IPs fijas y perfiles

Fecha: 2026-05-24 08:39:43

## Objetivo

Detectar referencias a IPs fijas dentro del repositorio para preparar instaladores adaptables por perfil e IPs reales.

## Resumen

| Campo | Valor |
|---|---|
| Total referencias IP detectadas | 206 |
| Severidad ALTA | 8 |
| Severidad MEDIA | 36 |
| Severidad BAJA | 10 |
| Severidad INFO | 152 |

## Criterio de severidad

| Severidad | Significado |
|---|---|
| ALTA | IP fija en instalador o configuraciÃ³n real. Debe revisarse antes de usar en cliente real. |
| MEDIA | IP fija en herramienta de producto o cÃ³digo/recurso. Debe parametrizarse si afecta a ejecuciÃ³n. |
| BAJA | IP en ejemplo de configuraciÃ³n. Puede mantenerse temporalmente si estÃ¡ claro que es ejemplo. |
| INFO | IP en documentaciÃ³n o validaciones. No bloquea, pero debe quedar contextualizada. |

## Hallazgos

| Severidad | Zona | IP | Archivo | LÃ­nea | Contenido |
|---|---|---|---|---:|---|
| ALTA | instalador | 127.0.0.1 | $fileSafe | 342 | $lineSafe |
| ALTA | instalador | 127.0.0.1 | $fileSafe | 417 | $lineSafe |
| ALTA | instalador | 127.0.0.1 | $fileSafe | 426 | $lineSafe |
| ALTA | instalador | 192.168.60.20 | $fileSafe | 9 | $lineSafe |
| ALTA | instalador | 192.168.60.30 | $fileSafe | 10 | $lineSafe |
| ALTA | instalador | 192.168.60.10 | $fileSafe | 16 | $lineSafe |
| ALTA | instalador | 127.0.0.1 | $fileSafe | 6 | $lineSafe |
| ALTA | instalador | 127.0.0.1 | $fileSafe | 101 | $lineSafe |
| BAJA | ejemplo_configuracion | 192.168.60.30 | $fileSafe | 12 | $lineSafe |
| BAJA | ejemplo_configuracion | 192.168.60.30 | $fileSafe | 13 | $lineSafe |
| BAJA | ejemplo_configuracion | 192.168.60.20 | $fileSafe | 14 | $lineSafe |
| BAJA | ejemplo_configuracion | 192.168.60.20 | $fileSafe | 18 | $lineSafe |
| BAJA | ejemplo_configuracion | 192.168.60.30 | $fileSafe | 37 | $lineSafe |
| BAJA | ejemplo_configuracion | 192.168.60.40 | $fileSafe | 37 | $lineSafe |
| BAJA | ejemplo_configuracion | 127.0.0.1 | $fileSafe | 37 | $lineSafe |
| BAJA | ejemplo_configuracion | 192.168.60.20 | $fileSafe | 37 | $lineSafe |
| BAJA | ejemplo_configuracion | 192.168.60.20 | $fileSafe | 39 | $lineSafe |
| BAJA | ejemplo_configuracion | 192.168.60.20 | $fileSafe | 48 | $lineSafe |
| INFO | documentacion | 192.168.60.40 | $fileSafe | 53 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 16 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 24 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 25 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 32 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 45 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 13 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 14 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 38 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 65 | $lineSafe |
| INFO | documentacion | 192.168.60.40 | $fileSafe | 12 | $lineSafe |
| INFO | documentacion | 192.168.60.40 | $fileSafe | 12 | $lineSafe |
| INFO | documentacion | 192.168.60.40 | $fileSafe | 25 | $lineSafe |
| INFO | documentacion | 192.168.1.248 | $fileSafe | 26 | $lineSafe |
| INFO | documentacion | 192.168.60.40 | $fileSafe | 20 | $lineSafe |
| INFO | documentacion | 192.168.1.248 | $fileSafe | 21 | $lineSafe |
| INFO | documentacion | 192.168.60.40 | $fileSafe | 56 | $lineSafe |
| INFO | documentacion | 192.168.60.40 | $fileSafe | 56 | $lineSafe |
| INFO | documentacion | 192.168.60.40 | $fileSafe | 60 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 84 | $lineSafe |
| INFO | documentacion | 192.168.60.40 | $fileSafe | 84 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 84 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 84 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 80 | $lineSafe |
| INFO | documentacion | 192.168.60.40 | $fileSafe | 32 | $lineSafe |
| INFO | documentacion | 192.168.1.248 | $fileSafe | 33 | $lineSafe |
| INFO | documentacion | 192.168.1.248 | $fileSafe | 54 | $lineSafe |
| INFO | documentacion | 192.168.60.40 | $fileSafe | 120 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 25 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 26 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 27 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 55 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 56 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 57 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 86 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 87 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 88 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 38 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 39 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 40 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 211 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 112 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 310 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 316 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 322 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 336 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 351 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 357 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 129 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 21 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 27 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 78 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 35 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 40 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 40 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 114 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 27 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 118 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 15 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 16 | $lineSafe |
| INFO | documentacion | 192.168.60.0 | $fileSafe | 24 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 31 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 32 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 66 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 76 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 94 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 15 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 16 | $lineSafe |
| INFO | documentacion | 192.168.1.250 | $fileSafe | 54 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 28 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 29 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 64 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 81 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 144 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 158 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 15 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 16 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 59 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 103 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 135 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 165 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 107 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 108 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 15 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 16 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 120 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 15 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 16 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 15 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 16 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 56 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 88 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 192 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 11 | $lineSafe |
| INFO | documentacion | 192.168.1.244 | $fileSafe | 11 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 12 | $lineSafe |
| INFO | documentacion | 192.168.1.243 | $fileSafe | 12 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 13 | $lineSafe |
| INFO | documentacion | 192.168.1.245 | $fileSafe | 13 | $lineSafe |
| INFO | documentacion | 192.168.60.0 | $fileSafe | 21 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 34 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 35 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 39 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 122 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 123 | $lineSafe |
| INFO | documentacion | 192.168.1.137 | $fileSafe | 143 | $lineSafe |
| INFO | documentacion | 192.168.1.244 | $fileSafe | 160 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 207 | $lineSafe |
| INFO | documentacion | 192.168.1.244 | $fileSafe | 272 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 12 | $lineSafe |
| INFO | documentacion | 192.168.1.244 | $fileSafe | 13 | $lineSafe |
| INFO | documentacion | 192.168.1.244 | $fileSafe | 14 | $lineSafe |
| INFO | documentacion | 192.168.1.137 | $fileSafe | 43 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 19 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 20 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 21 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 81 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 82 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 83 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 111 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 177 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 178 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 179 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 180 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 48 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 13 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 30 | $lineSafe |
| INFO | documentacion | 127.0.0.1 | $fileSafe | 20 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 13 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 13 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 51 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 52 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 53 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 11 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 12 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 13 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 41 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 42 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 43 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 44 | $lineSafe |
| INFO | documentacion | 192.168.60.10 | $fileSafe | 11 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 28 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 29 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 30 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 31 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 50 | $lineSafe |
| INFO | documentacion | 192.168.60.30 | $fileSafe | 51 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 52 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 53 | $lineSafe |
| INFO | documentacion | 192.168.60.20 | $fileSafe | 98 | $lineSafe |
| INFO | documentacion | 192.168.1.248 | $fileSafe | 25 | $lineSafe |
| INFO | documentacion | 192.168.60.40 | $fileSafe | 76 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.30 | $fileSafe | 12 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.30 | $fileSafe | 13 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.20 | $fileSafe | 14 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.20 | $fileSafe | 18 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.30 | $fileSafe | 37 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.40 | $fileSafe | 37 | $lineSafe |
| MEDIA | codigo_o_recurso | 127.0.0.1 | $fileSafe | 37 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.20 | $fileSafe | 37 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.20 | $fileSafe | 18 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.30 | $fileSafe | 19 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.30 | $fileSafe | 20 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.30 | $fileSafe | 21 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.20 | $fileSafe | 22 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.20 | $fileSafe | 23 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.20 | $fileSafe | 17 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.30 | $fileSafe | 18 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.20 | $fileSafe | 19 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.30 | $fileSafe | 20 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.30 | $fileSafe | 21 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.20 | $fileSafe | 22 | $lineSafe |
| MEDIA | codigo_o_recurso | 127.0.0.1 | $fileSafe | 15 | $lineSafe |
| MEDIA | codigo_o_recurso | 127.0.0.1 | $fileSafe | 16 | $lineSafe |
| MEDIA | codigo_o_recurso | 127.0.0.1 | $fileSafe | 17 | $lineSafe |
| MEDIA | codigo_o_recurso | 127.0.0.1 | $fileSafe | 18 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.30 | $fileSafe | 43 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.30 | $fileSafe | 44 | $lineSafe |
| MEDIA | codigo_o_recurso | 127.0.0.1 | $fileSafe | 45 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.20 | $fileSafe | 47 | $lineSafe |
| MEDIA | codigo_o_recurso | 127.0.0.1 | $fileSafe | 53 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.10 | $fileSafe | 37 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.1.244 | $fileSafe | 37 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.1.243 | $fileSafe | 38 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.20 | $fileSafe | 38 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.60.30 | $fileSafe | 39 | $lineSafe |
| MEDIA | codigo_o_recurso | 192.168.1.245 | $fileSafe | 39 | $lineSafe |
| MEDIA | herramienta_producto | 127.0.0.1 | $fileSafe | 103 | $lineSafe |

## InterpretaciÃ³n inicial

Esta auditorÃ­a no corrige automÃ¡ticamente las IPs.

Sirve para decidir quÃ© referencias deben transformarse en variables de instalaciÃ³n y cuÃ¡les pueden quedarse como documentaciÃ³n de laboratorio.

## PrÃ³ximo paso

Clasificar los hallazgos en:

- A mantener como evidencia histÃ³rica o documentaciÃ³n.
- A convertir en valores de config.env.example.
- A preguntar desde instaladores.
- A derivar segÃºn perfil Lite, PyME 2 servidores o Pro 3 servidores.

## Resultado

Resultado: REVISAR. Hay IPs fijas de severidad ALTA.
