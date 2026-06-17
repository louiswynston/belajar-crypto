from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./cryptolearn.db"
engine = create_engine(DATABASE_URL)

class Pendaftar(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nama: str
    email: str

def init_db():
    SQLModel.metadata.create_all(engine)

daftar_coin = [
    {"id": "bitcoin", "simbol": "BTC", "nama": "Bitcoin"},
    {"id": "ethereum", "simbol": "ETH", "nama": "Ethereum"},
    {"id": "solana", "simbol": "SOL", "nama": "Solana"},
    {"id": "bnb", "simbol": "BNB", "nama": "BNB"},
]

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def akar():
    return {"pesan": "Halo dari API CryptoLearn!"}

@app.get("/coins")
def lihat_coins():
    return daftar_coin

@app.get("/coin/{coin_id}")
def detail_coin(coin_id: str):
    for coin in daftar_coin:
        if coin["id"] == coin_id:
            return coin
    return {"error": "Coin tidak ditemukan"}

@app.get("/pendaftar")
def lihat_pendaftar():
    with Session(engine) as session:
        pendaftar = session.exec(select(Pendaftar)).all()
        return JSONResponse(
            content={
                "total": len(pendaftar),
                "data": [{"id": p.id, "nama": p.nama, "email": p.email} for p in pendaftar]
            },
            headers={"Content-Type": "application/json"}
        )

@app.post("/daftar")
def daftar_newsletter(data: Pendaftar):
    with Session(engine) as session:
        session.add(data)
        session.commit()
        session.refresh(data)
        return {
            "pesan": f"Terima kasih {data.nama}, kamu sudah terdaftar!",
            "id": data.id
        }