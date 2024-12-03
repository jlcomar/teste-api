from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, field_validator
from sqlalchemy import (
    create_engine, insert, Table, MetaData, Column, String, Float, Integer, Boolean, ForeignKey, Text, TIMESTAMP, func, update
)
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
# from cpf import is_cpf_valid
from typing import List
from sqlalchemy.sql import select, join
import requests
import threading
import time
import boto3
import json
from app.controllers.cliente_controller import router as cliente_router
from app.controllers.pedido_controller import router as pedido_router
from app.models.schemas import Cliente as cliente
from app.models.schemas import Pedido as pedido
from app.models.database import metadata, engine
from app.controllers.sqs import handle_sqs_message, queues

def lifespan(app: FastAPI):
    def start_sqs_handlers():
        for queue_name, queue_url in queues.items():
            threading.Thread(target=handle_sqs_message, args=(queue_name, queue_url)).start()
    
    start_sqs_handlers()
    yield  # Aqui pode incluir lógica para encerrar threads ou outros recursos, se necessário

app = FastAPI(lifespan=lifespan)

app.include_router(cliente_router)
app.include_router(pedido_router)

# Configuração do SQLAlchemy
DATABASE_URL = "mysql+mysqlconnector://pedido_user:Mudar123!@db-servicos:3306/pedido"
SQS_UPDATE_QUEUE = "pedido-atualizacao"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Gerenciamento de sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




