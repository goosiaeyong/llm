import chatbot
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

print(f"System: Env Variables are loaded: {load_dotenv()}")

app = FastAPI()
chatbot = chatbot.FairytaleMaker()

class MakeRequest(BaseModel):
    missions: str 
    name: str
    age: int
    character: str

@app.post("/fairytale")
async def ask_question(request: MakeRequest):
    # The query method returns a Python dictionary
    response = chatbot.make_fairytale(request)
    # FastAPI automatically converts this dictionary to JSON
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
