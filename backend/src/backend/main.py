from fastapi import FastAPI
import pandas as pd
import numpy as np
from pathlib import Path

app = FastAPI(title="EclipseBord API", version="0.1.0")

# Hitta mappen där main.py ligger för att peka rätt på data mappen
BASE_DIR = Path(__file__).resolve().parent

# Läs in data från data mappen med rätt sökväg
solar_df = pd.read_csv(BASE_DIR / "data" / "solar.csv").replace({np.nan: None})
lunar_df = pd.read_csv(BASE_DIR / "data" / "lunar.csv").replace({np.nan: None})

@app.get("/")
def read_root():
    return {"message": "Välkommen till EclipseBord API"}

@app.get("/solar")
def get_solar():
    return solar_df.to_dict(orient="records")

@app.get("/lunar")
def get_lunar():
    return lunar_df.to_dict(orient="records")