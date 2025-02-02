from typing import Optional

from openai import OpenAI
from pydantic import BaseModel
from typing import List

import instructor


class Character(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None


# enables `response_model` in create call
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required, but unused
    ),
    mode=instructor.Mode.JSON,
)

resp = client.chat.completions.create(
    model="llama3.2:1b",
    messages=[
        {
            "role": "user",
            "content": "John is 32 years old",
        }
    ],
    response_model=Character,
)

print(resp)