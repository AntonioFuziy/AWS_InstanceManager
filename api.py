import requests

# def get_tasks(url):
#   response = requests.get(url)
#   print(response)
#   return response.json()

# def post_task(url, title, date, description):
#   response = requests.post(
#     url, 
#     data={
#       "title": title,
#       "pub_date": date,
#       "description": description
#     }
#   )
#   print(response)
#   return response.json()

# def delete_task(url, task_id):
#   response = requests.delete(url + str(task_id))
#   print(response)
#   return response.json()

method = input("Digite o método [GET ou POST ou DELETE]: ")

if method == "GET":
  url = input("Digite a URL: ")
  response = requests.get(url)
  print(response)
  print(response.json())

elif method == "POST":
  url = input("Digite a URL: ")
  title = input("Digite o título: ")
  ano = input("Digite o ano: ")
  mes = input("Digite o mês: ")
  dia = input("Digite o dia: ")
  hora = input("Digite a hora: ")
  minuto = input("Digite o minuto: ")
  date = f"{ano}-{mes}-{dia}T{hora}:{minuto}"
  description = input("Digite a descrição: ")
  # print(post_task(url, title, date, description))

  response = requests.post(
    url, 
    data={
      "title": title,
      "pub_date": date,
      "description": description
    }
  )

  print(response)
  print(response.json())

elif method == "DELETE":
  url = input("Digite a URL: ")
  task_id = input("Digite o ID da tarefa: ")
  response = requests.delete(url + str(task_id) + "/")
  print(response)
  print(response.json())