import requests


response = requests.post(
    "http://localhost:8000/fairytale",
    json={"missions":"1.양치컵 사용하기\n2. 쓰레기 줍기\n3. 음식 남김없이 다 먹기", "name":"고양핑", "age":10, "character":"요정"})

fairytale = response.json()['content']
print(fairytale)
