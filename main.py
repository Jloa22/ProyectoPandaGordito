from fastapi import FastAPI
from back.dijkstra import ejecutar_dijkstra

app = FastAPI()

@app.get("/recomendar/{familia}")
def recomendar(familia: str):
    return ejecutar_dijkstra(familia)
