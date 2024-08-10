import requests

# /invoke -> call the paritcular API
response = requests.post(
    "http://localhost:8000/ask",
    json={"question":"음식물이 묻은 비닐 쓰레기는 어떻게 배출해야 돼?"})

answer = response.json()['content']
source = response.json()['source']
print(f"{answer}\nSources:\n{"\n".join(source)}")