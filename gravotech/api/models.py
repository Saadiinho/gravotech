from pydantic import BaseModel

class LoadFile(BaseModel):
    filename: str
    nb_marking: int
    mode: str

class Mask(BaseModel):
    mask: str

class PushFile(BaseModel):
    filename: str
    data: bytes

class Rule(BaseModel):
    rule: bool

class GetValue(BaseModel):
    index: int

class SetValue(BaseModel):
    index: int
    text: str

class Response(BaseModel):
    response: str

class HealthcheckResponse(BaseModel):
    name: str
    status: str
    version: str