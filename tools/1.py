from pydantic import BaseModel, validator


class MyModel(BaseModel):
    my_string: str

    class Config:
        validate_assignment = True
        extra = "allow"

    @validator('my_string')
    def check_my_string_type(cls, value):
        if not isinstance(value, str):
            raise TypeError('my_string must be a string')
        return value

a = MyModel(my_string=1)

print(a.dict())
a.validate()