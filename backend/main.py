# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # or ["http://localhost:5173"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

import os 
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from analyze import analyze
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

curr_path = os.path.dirname(__file__)
ip = "http://localhost:8000" # TODO : http for development , need SSL

@app.get("/")
def greet():
    return {"message": "welcome to IRCTC delay API"}

@app.get("/getDelayGraphs/{graph_name}")
def getDelayGraphs(graph_name: str, trainNo: str, station: str) -> FileResponse:
    img_path = os.path.join(curr_path,"graphs",f"{graph_name}")
    return FileResponse(img_path, media_type="image/png")

@app.get("/getDelayData")
def getDelayData(trainNo: str, station: str, cacheOverride: int = 0, cacheUpdate: int = 1):
    cacheUpdate = bool(cacheUpdate)
    cacheOverride = bool(cacheOverride)
    print("running analyze")
    # print(cacheOverride)

    data = analyze(trainNo, station, cacheOverride, cacheUpdate)
    imgs = data["imgs"]
    data["imgs"] = list(map(lambda x : ip+"/getDelayGraphs/"+f"{x}?trainNo={trainNo}&station={station}", imgs))
    return data 



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
