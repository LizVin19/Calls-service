from fastapi import FastAPI
from app.routers import calls
from app.routers import recordings

app = FastAPI(title='Calls & Recordings')


@app.get('/health')
def health():
    return {'status': 'ok'}

app.include_router(calls.router)
app.include_router(recordings.router)