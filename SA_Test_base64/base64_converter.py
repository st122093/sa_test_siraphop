from fastapi import FastAPI
import base64

app = FastAPI()

@app.get("/{name_str}")
def convert_to_base64(name_str: str):
    # Convert string to base 64
    base64_name = base64.b64encode(name_str.encode('ascii'))
    return {'base64': base64_name}