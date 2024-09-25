@admin.post("/area/restrita/{icao}/communication/{frequency_old}/edit")
async def edit_communication(request: Request,
                             icao: str,
                             frequency_old: int,
                             frequency: int = Form(ge=108000, le=137000),
                             comm_type: str = Form(...)):