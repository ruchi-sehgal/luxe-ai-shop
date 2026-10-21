from typing import Literal

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel, GroqModelSettings
from pydantic_ai.providers.groq import GroqProvider

from backend.config import settings


class ProductFilter(BaseModel):
    keyword: str | None = Field(None, description="A product-type word from the message, e.g. 'shirt', 'jeans', 'hoodie' — searched against the product name. Null if none mentioned.")
    category: Literal["men", "women", "kids"] | None = Field(None, description="The shopper's gender/age segment — ONLY if explicitly stated ('for men', 'for my daughter'). Never inferred from a clothing item name like 'shirt'.")
    colour: str | None = Field(None, description="A colour the shopper mentioned, or null")
    min_price: float | None = Field(None, description="Minimum price if mentioned, or null")
    max_price: float | None = Field(None, description="Maximum price if mentioned, or null")
    limit: int = Field(6, ge=1, le=20, description="How many products the shopper asked for, e.g. 'top 3' means 3. Default 6 if not specified.")
    reply: str = Field(..., description="One short, honest sentence back to the shopper. If asked for something the catalog can't determine — popularity, ratings, 'best seller', reviews — say plainly that this isn't tracked, instead of guessing or pretending you checked.")


model = GroqModel(
    "openai/gpt-oss-20b",
    provider=GroqProvider(api_key=settings.groq_api_key),
)

agent = Agent(
    model,
    output_type=ProductFilter,
    model_settings=GroqModelSettings(groq_reasoning_effort="medium"),
    system_prompt=(
        "You translate a shopper's plain-English request into a product search filter. "
        "Only fill in fields the shopper actually mentioned; leave everything else null. "
        "Never invent a value that wasn't implied by the message. "
        "Pay close attention to 'keyword': any clothing item word the shopper names — "
        "shirt, jeans, kurti, hoodie, dress, jacket, and so on — must be captured there. "
        "Your catalog has no popularity, rating, or review data — if asked for anything "
        "like that, say so honestly in your reply rather than guessing. "
        "If this message is a follow-up in an ongoing conversation, treat it as refining "
        "the previous request: keep earlier filter values (category, keyword, colour, "
        "price range) unless this new message clearly changes or removes them."
    ),
)