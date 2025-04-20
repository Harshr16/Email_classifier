from fastapi import FastAPI
from pydantic import BaseModel
from utils import mask_pii, demask_email, classify_email
import re
from typing import List, Dict

app = FastAPI(title="Email Classifier API")

class EmailRequest(BaseModel):
    email_text: str

class MaskedEntity(BaseModel):
    position: List[int]
    classification: str
    entity: str

class EmailResponse(BaseModel):
    input_email_body: str
    list_of_masked_entities: List[MaskedEntity]
    masked_email: str
    category_of_the_email: str

@app.post("/classify", response_model=EmailResponse)
def classify_email_route(request: EmailRequest):
    masked_email, pii_dict = mask_pii(request.email_text)

    list_of_entities = []
    for tag, entity_list in pii_dict.items():
        for entity in entity_list:
            start = request.email_text.find(entity)
            end = start + len(entity)
            list_of_entities.append({
                "position": [start, end],
                "classification": tag.strip("[]"),
                "entity": entity
                })


    category = classify_email(masked_email)

    return {
        "input_email_body": request.email_text,
        "list_of_masked_entities": list_of_entities,
        "masked_email": masked_email,
        "category_of_the_email": category
    }
