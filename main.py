from fastapi import FastAPI, Response

app = FastAPI()


@app.post("/api/auth/register")
def register_user() -> Response:
	return Response(status_code=201)
