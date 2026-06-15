from contextlib import contextmanager, asynccontextmanager
from fastapi import FastAPI
from config.database import Base, engine
from controller.auth_controller import router as auth_router
from controller.task_controller import router as task_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield

# Creamos una instancia de la aplicación FastAPI
app  =  FastAPI (
    title="MyProjectPython",
    version="0,1",
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(task_router)

@ app.get ( "/" )
async  def  bienvenida ():
    return { "mensaje" : "¡Bienvenido a mi primera API con FastAPI!" }

