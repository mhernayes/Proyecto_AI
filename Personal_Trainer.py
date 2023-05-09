#importamos la libreria de openai
import openai  # pip install openai
import typer  # pip install "typer[all]". libreria donde puedo agregar prompts y cosas copadas
from rich import print  # pip install rich. libreria para hacer mas bonitos los prints
from rich.table import Table
#importamos el archivo config donde vamos a guardar la api key
import config

"""
Webs de interés:
- Módulo OpenAI: https://github.com/openai/openai-python
- Documentación API ChatGPT: https://platform.openai.com/docs/api-reference/chat
- Typer: https://typer.tiangolo.com
- Rich: https://rich.readthedocs.io/en/stable/
"""

#definimos la funcion main donde ingresaron el codigo principal del chat. esta funcion es la que definimos en typer
def main():
    #llamamos a la api key desde otro archivo llamado config donde esta guardada con la variable api_key
    openai.api_key = config.api_key

    #definimos la varialbe table como una Tabla y le agregamos 2 filas "exit" y "new" 
    table_1 = Table("💬 [bold red]Personal Trainer[/bold red]")
    table_1.add_row("Realizado con versión de ChatGTP 3.5 Turbo")
    table_2 = Table("Menu", "Descripción")
    table_2.add_row("exit", "Ingrese exit SALIR de la aplicación")
    table_2.add_row("new", "Ingrese new par CREAR una nueva conversación")
    
    #imprimimos la tabla
    print(table_1)
    print(table_2)

    #pedimos por pantallas las variables
    peso = input("Por favor ingrese su peso (kg):\n")
    edad = input("Por favor ingrese su edad (años):\n")
    altura = input("Por favor ingrese su altura (cm):\n")
    role_content = ("Eres un personal trainer de un gimnasio que se dedica a mejorar la calidad de la vida de las personas a través de rutinas. Tenés que tener en cuenta que el usuario tiene un peso de " + peso + ", una edad de " + edad + " y una altura de " + altura)
    
    print("Mi rol como asistente es el siguiente:")
    print(f"[bold yellow]> [/bold yellow] [yellow]{role_content}[/yellow]")
    #definimos el contexto del asistente
    context = {"role": "system",
               "content": role_content}
    #guardamos el contexto del asistente en una lista llamada messages
    messages = [context]
    print("Buenos días, soy un Personal Trainer muy experiminetado.")

    #creamos un bucle para que siga preguntandonos cosas
    while True:
         #llamamos a la funcion __prompt donde emepzamos a preguntar 
        content = __prompt()

        #si quiseramos crear una conversacion nueva volvemos a limpiar la lista messages en "context"
        if content == "new":
            print("🆕 Nueva conversación creada")
            messages = [context]
            #llamamos a la funcion content para que pregunte nuevamente que quiere preguntar
            content = __prompt()

        #vamos añadiendo a la lista message un json con el "role" y "content" que es el contenido de los que vamos preguntando
        messages.append({"role": "user", "content": content})

        #guardamos la respuesta en una variable que se llama response y le pasamos 2 parametros
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", #1 el modelo a utilizar: gpt-3.5-turbo
                                                messages=messages) #2 el mensaje: la lista con todos el "content" que vamos añadiendo

        #nos quedamos con el contenido de la respusta ya que content es una lista con mas informacion
        response_content = response.choices[0].message.content
        
        #vamos añadiendo a la lista messages "response_content" que es el contenido de lo va respondiendo
        messages.append({"role": "assistant", "content": response_content})

        print(f"[bold blue]> [/bold blue] [blue]{response_content}[/blue]")

#definomos la funccion __prompt para preguntar que queiere hacer el usuario 
def __prompt():
    prompt = typer.prompt("\n¿En qué te puedo ayudar? ¿Qué rutina deseas?")

    #si el usuario ingresa salir 
    if prompt == "exit":
        exit = typer.confirm("😨 ¿Estás seguro?")
        if exit:
            print("👋¡Hasta luego!👋")
            #detener la ejecucion de typer
            raise typer.Abort()
        #si no quiero salir vuelvo a llamar a la funcion __prompt
        return __prompt()

    return prompt

#necesitamos este "if" para correr la libreria typer y main que es la funcion principal
if __name__ == "__main__":
    typer.run(main)

    