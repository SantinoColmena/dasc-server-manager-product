# R-049I-FIX - Corrección TemplateResponse panel central

## Objetivo

Corregir el error `Internal Server Error` al abrir el panel central DASC en navegador.

## Estado

Cerrada.

## Problema detectado

La API central arrancaba correctamente y `/health` respondía OK.

La recepción de tickets funcionaba correctamente:

~~~text
Token incorrecto: 401 OK
Token correcto: CENTRAL-2026-0001 OK
SQLite central: OK
~~~

Pero al abrir:

~~~text
GET /
~~~

en navegador aparecía:

~~~text
Internal Server Error
~~~

## Causa probable

La versión instalada de FastAPI/Starlette espera la llamada moderna a `TemplateResponse`:

~~~text
templates.TemplateResponse(request, "template.html", context)
~~~

En el prototipo inicial se usó la forma antigua:

~~~text
templates.TemplateResponse("template.html", {"request": request, ...})
~~~

## Cambio aplicado

Archivo modificado:

~~~text
deploy/central-support/package/main.py
~~~

Se cambia la llamada del dashboard central para usar la firma moderna.

## Criterio de validación

Este fix queda validado cuando:

- `main.py` compila.
- La API central arranca.
- `GET /health` responde OK.
- `GET /` abre el panel central en navegador.
- El ticket `CENTRAL-2026-0001` aparece en el panel.
