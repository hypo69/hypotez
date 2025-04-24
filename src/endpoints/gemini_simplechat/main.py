## \file main.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""

Простой интерфейс собраный на базе `fast_api`
================================================

```rst
.. module:: gemini_simplechat.main
```
"""
import sys, os

from pathlib import Path
from types import SimpleNamespace
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

import header
from header import __root__
from src import gs
from src.llm.gemini import GoogleGenerativeAi
from src.utils.get_free_port import get_free_port
from src.utils.jjson import j_loads_ns
from src.logger import logger


class Config:
    """"""
    ENDPOINT:Path = __root__/ 'src'/ 'endpoints'/ 'gemini_simplechat'
    try:
        config:'SimpleNamespace' = j_loads_ns(ENDPOINT/'gemini_simplechat.json')
        HOST:str = config.host
        PORTS_RANGE:list[int] = config.ports_range
        GEMINI_API_KEY:str = gs.credentials.gemini.onela.api_key
        GEMINI_MODEL_NAME:str = config.gemini_model_name #'gemini-1.5-flash-001-tuning' # <- Это модель, которая обучается моему коду
        system_instruction_path:Path = Path(__root__/ 'src' / 'endpoints' / 'hypo69' / 'code_assistant' / 'instructions' / 'instruction_trainer_ru.md')
        SYSTEM_INSTRUCTION:str = system_instruction_path.read_text(encoding='UTF-8') 

    except Exception as ex:
        logger.error(f'Ошибка загрузки конфигурации!')
        ...


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (for testing purposes)
    allow_credentials=True,
    allow_methods=["*"],  # Allowed methods (GET, POST, etc.)
    allow_headers=["*"],  # Allowed headers
)

# Chat request model
class ChatRequest(BaseModel):
    message: str


model: GoogleGenerativeAi = GoogleGenerativeAi(api_key = Config.GEMINI_API_KEY, 
                                               model_name = Config.GEMINI_MODEL_NAME, 
                                               system_instruction = Config.SYSTEM_INSTRUCTION)

# Root route
@app.get("/", response_class=HTMLResponse)
async def root():

    try:
        html_content = Path( __root__/ 'src'/ 'fast_api' / 'html'/ 'index.html').read_text(encoding="utf-8")
        return HTMLResponse(content=html_content)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error reading templates:{str(ex)}" )


# Chat route
@app.post("/api/chat")
async def chat(request: ChatRequest):
    global model
    try:
        response = await model.chat(request.message)
        return {"response": response}
    except Exception as ex:
        logger.error(f"Error in chat: ",ex)
        raise HTTPException(status_code=500, detail=str(e))


    

# Local server execution
if __name__ == "__main__":
    port:int = get_free_port(Config.HOST, Config.PORTS_RANGE) 
    uvicorn.run(app, host = Config.host, port = port)
