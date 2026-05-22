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

    Select-String -Path deploy\api\package\main.py -Pattern "passlib|password_hash|hash_password|verify_password|pwd_context"
    Select-String -Path deploy\api\package\requirements.txt -Pattern "passlib|bcrypt"

Resultado:

- `main.py` contiene importación de `CryptContext`.
- `main.py` contiene configuración `pwd_context`.
- `main.py` contiene funciones de hash y verificación.
- `main.py` guarda usuarios nuevos con `password_hash`.
- `requirements.txt` contiene `passlib[bcrypt]==1.7.4`.
- `requirements.txt` contiene `bcrypt==4.0.1`.

## Pruebas pendientes

| Prueba | Estado |
|---|---|
| Arranque del panel sin errores | Pendiente |
| Login con admin | Pendiente |
| Crear usuario nuevo desde Administración | Pendiente |
| Comprobar que `users.json` guarda `password_hash` | Pendiente |
| Login con usuario nuevo | Pendiente |
| Migración de usuario antiguo en texto plano | Pendiente |
| Validación en VM Ubuntu | Pendiente |

## Conclusión

R-015 queda implementado a nivel de código y pendiente de validación funcional en entorno real.
