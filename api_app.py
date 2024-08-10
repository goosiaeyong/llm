import chatbot
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

print(f"Env Variables are loaded: {load_dotenv()}")


app = FastAPI()
docs_dir_path = "./document_set"
db_dir = './database'
chatbot = chatbot.QnAChatBot(docs_dir_path, db_dir)

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    # The query method returns a Python dictionary
    response = chatbot.query(request.question)
    # FastAPI automatically converts this dictionary to JSON
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
