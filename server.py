from wsgiref.simple_server import make_server
import json

# Declaramos la lista que contendrá las tareas
tasks = []

# Declaramos la variable que llevará el último ID
next_id = 0

def app(environ, start_response):

    # Globalizamos la variable
    global next_id

    match environ.get("REQUEST_METHOD"):

        # Caso 1: Request GET
        case "GET":
            url = divide_url(environ)

            # Chequeamos que la primera ruta sea válida
            if (url[0] == "tasks"):

                # Chequeamos si nos pasó o no un ID
                if (len(url) == 1):

                    all_tasks = []

                    for task in tasks:
                        all_tasks.append(
                            {
                                "task": task["title"]["title"], 
                                "done": task["title"]["done"]
                            }
                        )

                    # En caso de no tener ID, retornamos todas las tareas
                    all_tasks_json = json.dumps(all_tasks).encode("utf-8")

                    msg200(environ, start_response)
                    return [all_tasks_json]
                else:
                    # Extraemos el ID de la URL
                    id = int(url[1])

                    # Iteramos sobre la lista de tareas en busca del ID
                    for currTask in tasks:
                            if currTask["id"] == id:  

                                # Armamos el retorno
                                task = {
                                            "title": currTask["title"]["title"],
                                            "done": currTask["title"]["done"]
                                        }

                                # Lo convertimos en JSON
                                task_json = json.dumps(task).encode("utf-8")

                                msg200(environ, start_response)
                                return[task_json]
                    
                    # Si no lo encontró, devolvemos 404 Not Found
                    return msg404(environ, start_response)
            else:
                return msg404(environ, start_response)
        
        # Caso 2: Request POST
        case "POST":
            url = divide_url(environ)

            # Chequeamos que la ruta sea válida
            if (url[0] == "tasks"):
                input = environ.get("wsgi.input")
                content_length = int(environ.get("CONTENT_LENGTH"))
                input_bytes = input.read(content_length)

                # Extraemos la información del body para la nueva tarea
                data = json.loads(input_bytes.decode("utf-8"))

                id = next_id
                title = data.get("title")
                done = data.get("done")

                # Añadimos la tarea a la lista
                tasks.append(
                        {
                            "id": id, 
                            "title": 
                                {
                                    "title": title, 
                                    "done": done
                                }
                        }
                    )

                # Creamos el cuerpo para retornar
                new_task = {
                    "id": id,
                    "title": title,
                    "done": done
                }

                response_json = json.dumps(new_task).encode("utf-8")
                next_id += 1
                
                msg201(environ, start_response)
                return [response_json]
            else:
                return msg404(environ, start_response)

        # Caso 3: Request PATCH
        case "PATCH":
            url = divide_url(environ)

            # Chequeamos que la primera ruta sea válida
            if (url[0] == "tasks"):

                # Chequeamos el ID en busca de existencia
                id = int(url[1])

                input = environ.get("wsgi.input")
                content_length = int(environ.get("CONTENT_LENGTH"))
                input_bytes = input.read(content_length)

                data = json.loads(input_bytes.decode("utf-8"))
                title = data.get("title")
                done = data.get("done")

                found = False
                modified_task = None

                # Iteramos sobre la lista de tareas en busca del ID
                for currTask in tasks:
                    if currTask["id"] == id:
                        found = True
                        
                        # Si se enviaron esos campos, se realizan los campos
                        if (title != None):
                            currTask["title"]["title"] = title
                        if (done != None):
                            currTask["title"]["done"] = done

                        modified_task = {
                            "id": id,
                            "title": currTask["title"]["title"],
                            "done": currTask["title"]["done"]
                        }

                        break

                # Si no encontró el ID, retornamos 404 Not Found
                if (found == False): 
                    return msg404(environ, start_response)

            else:
                return msg404(environ, start_response)

            response_json = json.dumps(modified_task).encode("utf-8")

            msg200(environ, start_response)
            return[response_json]

        # Caso 4: Request DELETE
        case "DELETE":
            url = divide_url(environ)

            # Chequeamos que la primera ruta sea válida
            if (url[0] == "tasks"):

                # Chequeamos el ID en busca de existencia
                id = int(url[1])

                if (id < next_id and id >= 0):
                    currID = 0

                    for task in tasks:
                        if (task["id"] == id):
                            del tasks[currID]
                            break
                        else:
                            currID += 1
                else:
                    return msg404(environ, start_response)

                msg204(environ, start_response)
                return []
    
        # Caso default: Method Not Allowed
        case _:
            return msg405(environ, start_response)

def divide_url(environ):
    # Extraemos de la request la ruta enviada
    path_info = environ.get("PATH_INFO")

    # Dividimos la ruta en base a la slash
    return path_info.strip("/").split("/")

def msg200(environ, start_response):
    status = "200 OK"
    headers = [("Content-Type", "application/json; charset=utf-8")]
    start_response(status, headers)

def msg201(environ, start_response):
    status = "201 Created"
    headers = [("Content-Type", "application/json; charset=utf-8")]
    start_response(status, headers)

def msg204(environ, start_response):
    status = "204 No Content"
    headers = []
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