import os

from dotenv import load_dotenv


load_dotenv(override=True)


# =========================
# FACEBOOK
# =========================

FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv(
    "FACEBOOK_PAGE_ACCESS_TOKEN"
)


# =========================
# INSTAGRAM
# =========================

INSTAGRAM_ACCESS_TOKEN = os.getenv(
    "INSTAGRAM_ACCESS_TOKEN"
)
INSTAGRAM_USER_ID = os.getenv(
    "INSTAGRAM_USER_ID"
)


# =========================
# THREADS
# =========================

THREADS_ACCESS_TOKEN = os.getenv(
    "THREADS_ACCESS_TOKEN"
)

THREADS_USER_ID = os.getenv(
    "THREADS_USER_ID"
)


# =========================
# NOTION
# =========================

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv(
    "NOTION_DATABASE_ID"
)


def validate_config() -> None:
    """Zkontroluje, zda jsou vyplněné potřebné hodnoty."""

    missing = []

    # Facebook
    if not FACEBOOK_PAGE_ID:
        missing.append("FACEBOOK_PAGE_ID")

    if not FACEBOOK_PAGE_ACCESS_TOKEN:
        missing.append(
            "FACEBOOK_PAGE_ACCESS_TOKEN"
        )

    # Notion
    if not NOTION_TOKEN:
        missing.append("NOTION_TOKEN")

    if not NOTION_DATABASE_ID:
        missing.append("NOTION_DATABASE_ID")

    # Instagram
    if not INSTAGRAM_ACCESS_TOKEN:
        missing.append(
            "INSTAGRAM_ACCESS_TOKEN"
        )

    if not INSTAGRAM_USER_ID:
        missing.append(
            "INSTAGRAM_USER_ID"
        )

    # Threads
    if not THREADS_ACCESS_TOKEN:
        missing.append(
            "THREADS_ACCESS_TOKEN"
        )

    if not THREADS_USER_ID:
        missing.append(
            "THREADS_USER_ID"
        )

    if missing:
        raise RuntimeError(
            f"V souboru .env chybí: {', '.join(missing)}"
        )