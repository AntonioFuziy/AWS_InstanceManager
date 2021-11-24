import requests

def get_tasks(url):
  response = requests.get(url)
  return response.json()

def post_task(url, title, date, description):
  response = requests.post(
    url, 
    data={
      "title": title,
      "pub_date": date,
      "description": description
    }
  )
  return response.json()

method = input("Digite o método [GET ou POST]: ")

if method == "GET":
  url = input("Digite a URL: ")
  print(get_tasks(url))

if method == "POST":
  url = input("Digite a URL: ")
  title = input("Digite o título: ")
  ano = input("Digite o ano: ")
  mes = input("Digite o mês: ")
  dia = input("Digite o dia: ")
  hora = input("Digite a hora: ")
  minuto = input("Digite o minuto: ")
  date = f"{ano}-{mes}-{dia}T{hora}:{minuto}"
  description = input("Digite a descrição: ")
  print(post_task(url, title, date, description))

else:
  print("Método inválido")