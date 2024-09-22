from fastapi import FastAPI
from app.api import auth, conferenceapi, endpoints, paperapi
from app.database import engine
from app.models import user, paper, conference

#dimiourgia pinakwn apo ta montela
user.Base.metadata.create_all(bind=engine)
paper.Base.metadata.create_all(bind=engine)
conference.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(endpoints.router)
app.include_router(conferenceapi.router)
app.include_router(paperapi.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)