@app.exception_handler(RequestValidationError)
async def unprocesable(request: Request, exc: RequestValidationError):
    details = []
    for error in exc.errors():
        details.append(f"Variável '{error["loc"][1]}' com valor '{error["input"]}' está com o erro '{error["msg"]}'")
    return templates.TemplateResponse("error.html", {"request": request, 
                                                     "error": f"Erro 422 | Erro no formulário", 
                                                     "details": details},
                                                     status_code=401)