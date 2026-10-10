from pydantic import BaseModel, Field

class SuggestTicketHttpRequest(BaseModel):
    problem_description: str = Field(min_length=1)
