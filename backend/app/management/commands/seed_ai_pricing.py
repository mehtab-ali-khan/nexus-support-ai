# backend/app/management/commands/seed_ai_pricing.py

from django.core.management.base import BaseCommand
from app.models import AIModelPricing
from app.ai.pricing import PRICING

PROVIDER_MAP = {
    "google": AIModelPricing.Provider.GOOGLE,
    "openai": AIModelPricing.Provider.OPENAI,
    "anthropic": AIModelPricing.Provider.ANTHROPIC,
}


class Command(BaseCommand):
    help = (
        "Mirrors app/ai/pricing.py into the AIModelPricing table, purely "
        "for admin visibility/reporting. The real cost calculation reads "
        "pricing.py directly, not this table - run this after editing "
        "pricing.py to keep the admin view in sync."
    )

    def handle(self, *args, **options):
        for (provider_key, model_name), prices in PRICING.items():
            provider = PROVIDER_MAP[provider_key]
            pricing, created = AIModelPricing.objects.update_or_create(
                provider=provider,
                model_name=model_name,
                defaults={
                    "input_price_per_1k": prices["input_price_per_1k"],
                    "output_price_per_1k": prices["output_price_per_1k"],
                    "is_active": True,
                },
            )
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} pricing: {pricing}"))
