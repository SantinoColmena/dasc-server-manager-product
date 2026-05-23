# Validación automática del paquete API instalable

Fecha: 2026-05-23 17:18:08

## Resumen

| Campo | Valor |
|---|---|
| Total comprobaciones | 20 |
| Correctas | 20 |
| Fallidas | 0 |

## Resultado

Resultado: OK.

El paquete API cumple las comprobaciones mínimas para seguir avanzando hacia instalación real.

## Comprobaciones

| Estado | Comprobación | Detalle |
|---|---|---|
| OK | Existe paquete API | Ruta esperada: deploy/api/package |
| OK | Existe instalador API | Ruta esperada: deploy/api/install_dasc_api.sh |
| OK | No existe config.env real en paquete | El paquete no debe incluir secretos reales. |
| OK | Existe config.env.example en paquete | El instalador debe crear config.env a partir de este ejemplo. |
| OK | Existe main.py | Archivo principal del API. |
| OK | Existe requirements.txt | Dependencias del API. |
| OK | Existe carpeta templates | Plantillas web. |
| OK | Existe carpeta static | Archivos estáticos. |
| OK | Existe generador Python de informe operativo | Herramienta de producto dentro del paquete. |
| OK | Existe wrapper Bash de informe operativo | Wrapper para servidor Linux. |
| OK | Existe reports/.gitkeep | Mantiene la carpeta reports sin versionar informes generados. |
| OK | No hay informes runtime versionables en reports | Los informes generados deben ignorarse y no subirse. |
| OK | Instalador requiere config.env.example | El instalador no debe depender de config.env real en el repo. |
| OK | Instalador crea config.env si falta | Debe crear config.env en la instalación real. |
| OK | Instalador prepara data | Debe crear directorio runtime data. |
| OK | Instalador prepara reports | Debe crear directorio runtime reports. |
| OK | Instalador prepara tools | Debe crear directorio tools. |
| OK | Instalador da permisos al wrapper | Debe dar permisos de ejecución al wrapper. |
| OK | install_dasc_api.sh usa LF | Los scripts Linux deben tener LF. |
| OK | generate_operational_report.sh usa LF | Los scripts Linux deben tener LF. |

## Conclusión

El paquete API está preparado a nivel estructural para una prueba de instalación real en Ubuntu.
