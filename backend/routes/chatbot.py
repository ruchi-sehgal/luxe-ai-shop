from fastapi import APIRouter
from pydantic import BaseModel
from pydantic_ai.messages import ModelMessagesTypeAdapter

from backend.chatbot.agent import agent
from backend.database import db

router = APIRouter(prefix="/chat", tags=["chatbot"])


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


def search_with_fallback(query: dict, limit: int):
    total = db.products.count_documents(query)
    if total > 0:
        return list(db.products.find(query, {"_id": 0}).limit(limit)), total, None

    if "price" in query:
        relaxed = {k: v for k, v in query.items() if k != "price"}
        total_r = db.products.count_documents(relaxed)
        if total_r > 0:
            products_r = list(db.products.find(relaxed, {"_id": 0}).sort("price", 1).limit(limit))
            return products_r, total_r, "price"

    if "colours" in query:
        relaxed = {k: v for k, v in query.items() if k != "colours"}
        total_r = db.products.count_documents(relaxed)
        if total_r > 0:
            products_r = list(db.products.find(relaxed, {"_id": 0}).limit(limit))
            return products_r, total_r, "colour"

    if "name" in query:
        relaxed = {k: v for k, v in query.items() if k != "name"}
        total_r = db.products.count_documents(relaxed)
        if total_r > 0:
            products_r = list(db.products.find(relaxed, {"_id": 0}).limit(limit))
            return products_r, total_r, "item type"

    return [], 0, None


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

    products, total_matches, relaxed_field = search_with_fallback(query, filters.limit)
    new_history = ModelMessagesTypeAdapter.dump_python(result.all_messages(), mode="json")

    if total_matches == 0:
        reply = "I couldn't find anything matching that, even trying nearby options — want to try a different search?"
    elif relaxed_field:
        reply = f"I didn't find an exact match, but here's what's available if we're flexible on {relaxed_field}:"
    else:
        reply = filters.reply

    return {
        "reply": reply,
        "filter": filters.model_dump(),
        "total_matches": total_matches,
        "relaxed_field": relaxed_field,
        "products": products,
        "history": new_history,
    }