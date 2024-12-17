from pydantic import BaseModel, Field, ConfigDict


class EmployerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    employer_id: int
    employer_name: str = Field(max_length=50)
    contact_name: str | None = Field(default=None, max_length=50)
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=50)
