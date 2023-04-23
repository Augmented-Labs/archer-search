from fastapi import FastAPI
from pydantic import BaseModel
from helper import calculate_linkedin_relevancy, get_posts_company
from fastapi.responses import JSONResponse
import requests
import time
app = FastAPI()


class Data(BaseModel):
    query: str
    searchType: str
    url: str


@app.post("/relevancy")
async def create_item(data: Data):
    data_dict = data.dict()
    try:
        if data_dict['searchType'] == 'Individual Search':
            result = calculate_linkedin_relevancy(
                data_dict['url'], data_dict['query'], data_dict['searchType'])
            return result
        if data_dict['searchType'] == 'Company Search':
            result = get_posts_company(
                data_dict['url'], data_dict['query'])
            return {'result': result, 'searchType': data_dict['searchType']}
    except Exception as e:
        return {}
