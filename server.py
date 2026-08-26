from wsgiref.simple_server import make_server
import json

tasks = [
    {"id": 0, "task": {"task": "Barrer", "done": True}},
    {"id": 1, "task": {"task": "Cocinar", "done": False}}
]

def app(environ, start_response):
    match environ.get("REQUEST_METHOD"):

        # Caso 1: Request GET
        case "GET":
            # Extraemos de la request la ruta enviada
            path_info = environ.get("PATH_INFO")

            # Dividimos la ruta en base a la slash
            partes = path_info.strip("/").split("/")

            # Chequeamos que la primera ruta sea válida
            if (partes[0] == "tasks"):

                # Chequeamos si nos pasó o no un ID
                if (len(partes) == 1):

                    all_tasks = []

                    for task in tasks:
                        all_tasks.append(
                            {
                                "task": task["task"]["task"], 
                                "done": task["task"]["done"]
                            }
                        )

                    # En caso de no tener ID, retornamos todas las tareas
                    all_tasks_json = json.dumps(all_tasks).encode("utf-8")

                    msg200(environ, start_response)
                    return [all_tasks_json]
                else:
                    id = int(partes[1])

                    # Iteramos sobre la lista de tareas en busca del ID
                    for currTask in tasks:
                            if currTask["id"] == id:  

                                # Armamos el retorno
                                task = {
                                            "task": currTask["task"]["task"],
                                            "done": currTask["task"]["done"]
                                        }

                                # Lo convertimos en JSON
                                task_json = json.dumps(task).encode("utf-8")

                                msg200(environ, start_response)
                                return[task_json]
                    
                    # Si no lo encontró, devolvemos 404 Not Found
                    return msg404(environ, start_response)
            else:
                return msg404(environ, start_response)
    
        # Caso default: Method Not Allowed
        case _:
            return msg405(environ, start_response)

def msg200(environ, start_response):
    status = "200 OK"
    headers = [("Content-Type", "application/json; charset=utf-8")]
    start_response(status, headers)

def msg404(environ, start_response):
    status = "404 Not Found"
    headers = [("Content-Type", "text/plain")]
    start_response(status, headers)
    return [b"404 Not Found"]

def msg405(environ, start_response):
    status = "405 Method Not Allowed"
    headers = [("Content-Type", "text/plain")]
    start_response(status, headers)
    return [b"405 Method Not Allowed"]

with make_server("", 9292, app) as server:
    print("Listening on http://localhost:9292")
    server.serve_forever()