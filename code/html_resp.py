@app.get("/taf/{icao}", response_class=HTMLResponse)
async def info_taf(request: Request, icao: str):
    ...