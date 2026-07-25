# backend/app/management/commands/seed_demo_data.py

from django.core.management.base import BaseCommand

from app.ai.indexing import index_article
from app.models import Company, KnowledgeBaseArticle

DEMO_COMPANY_NAME = "Demo Electronics Co."

# Keep this content identical to frontend/public/test-website.html so the
# human-readable demo page and what the AI actually retrieves never drift
# apart. If you edit one, edit the other.
ARTICLES = [
    {
        "title": "Shipping Policy",
        "body": (
            "Standard shipping within Pakistan takes 3-5 business days and is free "
            "on orders over PKR 5,000. Orders under that have a flat shipping fee "
            "of PKR 250. Express shipping is available at checkout for an "
            "additional PKR 600 and delivers within 1-2 business days in major "
            "cities. Once your order ships, you'll receive a tracking number by "
            "email within 24 hours. Orders placed before 3 PM on business days are "
            "processed the same day; orders placed on weekends or holidays are "
            "processed the next business day."
        ),
    },
    {
        "title": "Return & Refund Policy",
        "body": (
            "We accept returns within 14 days of delivery for any item in its "
            "original, unopened packaging. To start a return, contact support "
            "with your order number and reason for return. Once we receive and "
            "inspect the item, refunds are issued to the original payment method "
            "within 5-7 business days. Original shipping costs are non-refundable, "
            "and customers cover return shipping unless the item arrived damaged "
            "or defective. Earphones and other in-ear audio products cannot be "
            "returned once the packaging seal is broken, for hygiene reasons - "
            "this applies even within the 14-day window."
        ),
    },
    {
        "title": "Warranty Policy",
        "body": (
            "All products come with a 1-year manufacturer's warranty covering "
            "defects in materials and workmanship under normal use. This does not "
            "cover accidental damage, water damage outside the product's rated "
            "resistance, unauthorized repairs, or normal wear like battery "
            "capacity loss after 12+ months of use. To make a claim, contact "
            "support with your order number, a description of the issue, and "
            "photos or a short video of the defect. Approved claims are resolved "
            "with a free repair, replacement, or store credit, at our discretion. "
            "The warranty is tied to the original purchaser and is not "
            "transferable."
        ),
    },
    {
        "title": "Order Cancellation Policy",
        "body": (
            "Orders can be cancelled free of charge within 1 hour of being "
            "placed, as long as the order hasn't entered processing yet. To "
            'cancel, go to "My Orders" and select "Cancel Order," or contact '
            "support with your order number. Once an order has shipped, it can "
            "no longer be cancelled - use the return process instead once it "
            "arrives. Pre-order items cannot be cancelled once the pre-order "
            "window has closed, even within the 1-hour rule."
        ),
    },
    {
        "title": "Payment Methods & Billing",
        "body": (
            "We accept debit/credit cards, bank transfer, and cash on delivery "
            "(COD) for orders under PKR 20,000. Card and bank transfer payments "
            "are charged in full at checkout; COD orders are paid at the time of "
            "delivery. If a card payment fails, the order is not created and no "
            "partial charge occurs. We do not store full card numbers - all card "
            "payments are processed through a PCI-compliant third-party payment "
            "gateway."
        ),
    },
]


class Command(BaseCommand):
    help = (
        "Seeds (or resets) a demo company with knowledge base articles matching "
        "test-website.html, and indexes them so the widget demo actually uses "
        "the real RAG pipeline instead of hand-typed HTML."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete and recreate the demo company's articles even if they already exist.",
        )

    def handle(self, *args, **options):
        company, created = Company.objects.get_or_create(name=DEMO_COMPANY_NAME)

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created demo company: {company.name}")
            )
        else:
            self.stdout.write(f"Using existing demo company: {company.name}")

        if options["reset"]:
            deleted_count, _ = company.knowledge_base_articles.all().delete()
            self.stdout.write(f"Deleted {deleted_count} existing article(s).")

        for entry in ARTICLES:
            article, was_created = KnowledgeBaseArticle.objects.get_or_create(
                company=company,
                title=entry["title"],
                defaults={"body": entry["body"]},
            )

            if not was_created and article.body != entry["body"]:
                article.body = entry["body"]
                article.save(update_fields=["body", "updated_at"])
                self.stdout.write(f"Updated article body: {article.title}")
            elif was_created:
                self.stdout.write(f"Created article: {article.title}")
            else:
                self.stdout.write(f"Article already up to date: {article.title}")

            index_article(article)

            article.refresh_from_db()
            if article.index_status != KnowledgeBaseArticle.IndexStatus.READY:
                self.stdout.write(
                    self.style.WARNING(
                        f"  - indexing did not succeed for '{article.title}': "
                        f"{article.index_error}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("Demo company API key (paste into test-website.html):")
        )
        self.stdout.write(str(company.api_key))
