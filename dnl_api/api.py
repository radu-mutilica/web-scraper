from typing import List
from fastapi import FastAPI, Query

from database import MongoDB
from models import Product

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})


@app.get("/",
         response_model=List[Product],
         responses={
             200: {
                 "description": "A collection of products",
             }
         },
         )
async def get_products(
        model: str = Query(None, title="Model", description="Filter by model", min_length=1),
        category: str = Query(None, title="Category", description="Filter by category",
                              min_length=1),
        make: str = Query(None, title="Make", description="Filter by make", min_length=1),
        part_number: str = Query(None, title="Part Number", description="Filter by part number",
                                 min_length=1),
        part_type: str = Query(None, title="Part Type", description="Filter by part type",
                               min_length=0),
) -> List[dict]:
    """
    Retrieve a list of products from the database, based on different query parameters.
    """
    # Constructing the filter based on provided query parameters
    filter_query = {}
    if model:
        filter_query["model"] = model
    if category:
        filter_query["category"] = category
    if make:
        filter_query["make"] = make
    if part_number:
        filter_query["part_number"] = part_number
    if part_type:
        filter_query["part_type"] = part_type

    result = list(MongoDB("spider").get_collection("scraped").find(
        filter_query,
        # Exclude the id from the results because its type is not serializable,
        # and also, we don't even need to display it regardless
        {'_id': 0}
    ))

    return result
