# backend/app/ai/pricing.py

"""
Static AI model pricing table.

This lives in code (not the database) on purpose: it's read on EVERY
single AI call to calculate cost, so it must be fast - a database query
here would mean an extra DB round-trip per customer message. Prices also
barely ever change (maybe a few times a year), so there's no real
downside to storing it here instead of a table.

To update a price or add a new model: edit this dict and deploy - same
as changing any other constant in the codebase. Keep this in sync with
seed_ai_pricing.py, which populates the AIModelPricing table used only
for admin visibility/reporting, not for the actual cost math.
"""

from decimal import Decimal

PRICING = {
    ("google", "gemini-3.1-flash-lite"): {
        "input_price_per_1k": Decimal("0.00025"),  # $0.25 per 1M input tokens
        "output_price_per_1k": Decimal("0.0015"),  # $1.50 per 1M output tokens
    },
    ("google", "gemini-2.5-flash-lite"): {
        "input_price_per_1k": Decimal("0.0001"),  # $0.10 per 1M input tokens
        "output_price_per_1k": Decimal("0.0004"),  # $0.40 per 1M output tokens
    },
    ("google", "gemini-2.5-flash"): {
        "input_price_per_1k": Decimal("0.0003"),  # $0.30 per 1M input tokens
        "output_price_per_1k": Decimal("0.0025"),  # $2.50 per 1M output tokens
    },
    ("google", "gemini-embedding-001"): {
        "input_price_per_1k": Decimal("0.00015"),  # $0.15 per 1M input tokens
        "output_price_per_1k": Decimal("0.0"),  # embeddings have no output cost
    },
    ("openai", "gpt-4o-mini"): {
        "input_price_per_1k": Decimal("0.00015"),  # $0.15 per 1M input tokens
        "output_price_per_1k": Decimal("0.0006"),  # $0.60 per 1M output tokens
    },
    ("anthropic", "claude-haiku-4-5-20251001"): {
        "input_price_per_1k": Decimal("0.001"),  # $1.00 per 1M input tokens
        "output_price_per_1k": Decimal("0.005"),  # $5.00 per 1M output tokens
    },
}


def get_pricing(provider: str, model_name: str) -> dict | None:
    """
    Looks up pricing for one provider/model pair. Returns None if not
    found - the caller decides what to do (log with cost=0, same as today).
    """
    return PRICING.get((provider, model_name))
