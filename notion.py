from notion_client import Client

from config import NOTION_DATABASE_ID, NOTION_TOKEN
from models.post import Post
from scheduler import parse_date


notion_client = Client(auth=NOTION_TOKEN)


def get_data_source_id() -> str:
    database = notion_client.databases.retrieve(
        database_id=NOTION_DATABASE_ID
    )

    data_sources = database.get("data_sources", [])

    if not data_sources:
        raise RuntimeError(
            "Databáze neobsahuje dostupný data source."
        )

    return data_sources[0]["id"]


def get_title(prop: dict | None) -> str:
    if not prop:
        return ""

    return "".join(
        item.get("plain_text", "")
        for item in prop.get("title", [])
    )


def get_rich_text(prop: dict | None) -> str:
    if not prop:
        return ""

    return "".join(
        item.get("plain_text", "")
        for item in prop.get("rich_text", [])
    )


def get_select(prop: dict | None) -> str:
    if not prop:
        return ""

    property_type = prop.get("type")

    if property_type == "select":
        selected = prop.get("select")
        return selected.get("name", "") if selected else ""

    if property_type == "multi_select":
        return ", ".join(
            item.get("name", "")
            for item in prop.get("multi_select", [])
        )

    return ""


def get_date(prop: dict | None) -> str | None:
    if not prop:
        return None

    date_value = prop.get("date")

    if not date_value:
        return None

    return date_value.get("start")


def get_media(prop: dict | None) -> list[str]:
    if not prop:
        return []

    media_urls: list[str] = []

    for item in prop.get("files", []):
        item_type = item.get("type")
        url = None

        if item_type == "external":
            url = item.get("external", {}).get("url")

        elif item_type == "file":
            url = item.get("file", {}).get("url")

        if url:
            media_urls.append(url)

    return media_urls


def page_to_post(page: dict) -> Post:
    properties = page.get("properties", {})

    date_string = get_date(properties.get("Date"))

    return Post(
        id=page.get("id", ""),
        title=get_title(properties.get("Name")),
        text=get_rich_text(properties.get("Text")),
        network=get_select(properties.get("Sit")),
        publish_date=parse_date(date_string),
        status=get_select(properties.get("Stav")),
        media=get_media(properties.get("Files & media")),
    )


def get_posts() -> list[Post]:
    data_source_id = get_data_source_id()

    response = notion_client.data_sources.query(
        data_source_id=data_source_id,
        page_size=100,
        filter={
            "property": "Stav",
            "select": {
                "equals": "✅ Připraveno"
            },
        },
    )

    return [
        page_to_post(page)
        for page in response.get("results", [])
    ]
def update_post_status(page_id: str, status: str) -> None:
    """Změní hodnotu sloupce Stav u příspěvku v Notionu."""

    notion_client.pages.update(
        page_id=page_id,
        properties={
            "Stav": {
                "select": {
                    "name": status
                }
            }
        },
    )