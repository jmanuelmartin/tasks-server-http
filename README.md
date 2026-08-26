# Ingeniería de Software I (Taller)

## Misión 1: Construir un Servidor HTTP con WSGI en Python

### Juan Manuel Martin

#### Explicación de GET, POST, PATCH y DELETE

Aquí hablaremos de los distintos tipos de requests y qué hace cada uno:

- **GET**: Este verbo lo que hace es obtener datos desde el servidor.

- **POST**: En cambio, este envía datos hacia el servidor (generalmente, dentro del cuerpo de la request) con el objetivo de crear un registro.

- **PATCH**: Actualiza sólo una parte de un registro almacenado en el servidor.

- **DELETE**: Elimina datos que se encuentran almacenados dentro del servidor.

#### ¿Por qué POST no es idempotente?

Primero pensemos en qué sería idempotente. La idempotencia nos dice que, al ejecutar una misma request varias veces, el efecto producido va a ser exactamente igual a que si la ejecutáramos una sola vez.

Pero, ¿esto sucede con el POST? Claramente no. Si lo pensamos, cada vez que hacemos un POST estamos asignándole un ID a esa tarea. Si yo envío la misma tarea de nuevo, se le asignará el siguiente ID, y así sucesivamente. Por ende, cada tarea es distinta, ya que tienen el mismo cuerpo, pero sus ID son distintos.

Por eso es que decimos que el verbo POST no es idempotente.