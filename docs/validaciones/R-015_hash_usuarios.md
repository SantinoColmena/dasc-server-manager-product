# Validación R-015 - Hash de contraseñas de usuarios

## Objetivo

Implementar almacenamiento seguro de contraseñas para usuarios creados desde el panel DASC Server Manager.

## Estado inicial

Antes de esta tarea, los usuarios creados desde el panel se guardaban en `data/users.json` con la contraseña en texto plano.

El login comparaba directamente la contraseña introducida con el valor guardado.

## Cambios realizados

- Se añade `passlib` con bcrypt.
- Se añade `bcrypt` como dependencia fijada.
- Se crea la función `hash_password()`.
- Se crea la función `verify_password()`.
- Los usuarios nuevos se guardan con el campo `password_hash`.
- Se evita guardar nuevas contraseñas en texto plano.
- Se mantiene compatibilidad temporal con usuarios antiguos que todavía tengan `password`.
- Si se detecta un usuario antiguo con `password`, se migra automáticamente a `password_hash`.
- El login ya no guarda la contraseña dentro del objeto de sesión.

## Archivos modificados

- `deploy/api/package/main.py`
- `deploy/api/package/requirements.txt`

## Validación estática

Comandos utilizados:

    python -m py_compile deploy\api\package\main.py

Resultado:

- El archivo `main.py` compila correctamente.
- No se detectan errores de sintaxis.

## Validación funcional local

Entorno utilizado:

- Windows
- PowerShell
- Entorno virtual Python `.venv`
- Uvicorn en `127.0.0.1:8000`

Pruebas realizadas:

| Prueba | Estado |
|---|---|
| Arranque del panel sin errores | Correcto |
| Login con admin | Correcto |
| Crear usuario nuevo desde Administración | Correcto |
| Comprobar que `users.json` guarda `password_hash` | Correcto |
| Comprobar que no se guarda `password` en texto plano | Correcto |
| Login con usuario nuevo | Correcto |
| Validación en VM Ubuntu | Pendiente |

Usuario de prueba creado:

    prueba

Permisos asignados:

    logs
    servicios

Resultado observado en `data/users.json`:

    [
      {
        "username": "prueba",
        "password_hash": "$2b$...",
        "permissions": [
          "logs",
          "servicios"
        ]
      }
    ]

Conclusión de la prueba:

El sistema permite crear usuarios desde el panel, guarda la contraseña como hash bcrypt y permite iniciar sesión correctamente con el usuario creado.

## Estado de cierre

R-015 queda implementado y validado localmente.

Queda pendiente la validación final en máquina Ubuntu real cuando se pruebe el instalador del panel.
