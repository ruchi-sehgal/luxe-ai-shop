from fastapi import APIRouter
from pydantic import BaseModel
from pydantic_ai.messages import ModelMessagesTypeAdapter

from backend.chatbot.agent import agent
from backend.database import db

router = APIRouter(prefix="/chat", tags=["chatbot"])


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


@router.post("")
async def chat(request: ChatRequest):
    history = ModelMessagesTypeAdapter.validate_python(request.history) if request.history else []
    result = await agent.run(request.message, message_history=history)
    filters = result.output

    query: dict = {}
    if filters.keyword:
        query["name"] = {"$regex": filters.keyword, "$options": "i"}
    if filters.category:
        query["category"] = filters.category
    if filters.colour:
        query["colours"] = {"$regex": filters.colour, "$options": "i"}
    if filters.min_price is not None or filters.max_price is not None:
        query["price"] = {}
        if filters.min_price is not None:
            query["price"]["$gte"] = filters.min_price
        if filters.max_price is not None:
            query["price"]["$lte"] = filters.max_price

    total_matches = db.products.count_documents(query)
    products = list(db.products.find(query, {"_id": 0}).limit(filters.limit))
    new_history = ModelMessagesTypeAdapter.dump_python(result.all_messages(), mode="json")

    return {
        "reply": filters.reply,
        "filter": filters.model_dump(),
        "total_matches": total_matches,
        "products": products,
        "history": new_history,
    }