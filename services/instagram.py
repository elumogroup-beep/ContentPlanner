import time
import requests

from models.post import Post
from config import INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_USER_ID


API_VERSION = "v24.0"
BASE_URL = f"https://graph.instagram.com/{API_VERSION}"


def create_media_container(image_url: str, caption: str) -> str:
    """Vytvoří Instagram media container."""

    url = f"{BASE_URL}/{INSTAGRAM_USER_ID}/media"

    response = requests.post(
        url,
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": INSTAGRAM_ACCESS_TOKEN,
        },
        timeout=30,
    )

    if not response.ok:
        print("❌ Instagram: nepodařilo se vytvořit container.")
        print(response.text)
        response.raise_for_status()

    return response.json()["id"]


def wait_for_container(container_id: str) -> None:
    """Počká, dokud Instagram nezpracuje obrázek."""

    url = f"{BASE_URL}/{container_id}"

    for _ in range(20):
        response = requests.get(
            url,
            params={
                "fields": "status_code,status",
                "access_token": INSTAGRAM_ACCESS_TOKEN,
            },
            timeout=30,
        )

        if not response.ok:
            print("❌ Instagram: chyba při kontrole containeru.")
            print(response.text)
            response.raise_for_status()

        data = response.json()

        status_code = data.get("status_code")
        status = data.get("status")

        print(
            f"⏳ Instagram container: "
            f"{status_code} ({status or 'bez detailu'})"
        )

        if status_code == "FINISHED":
            return

        if status_code in {"ERROR", "EXPIRED"}:
            raise RuntimeError(
                f"Instagram container selhal: {data}"
            )

        time.sleep(3)

    raise TimeoutError(
        "Instagram container nebyl připraven do 60 sekund."
    )


def publish_media(container_id: str) -> str:
    """Publikuje připravený Instagram container."""

    url = f"{BASE_URL}/{INSTAGRAM_USER_ID}/media_publish"

    response = requests.post(
        url,
        data={
            "creation_id": container_id,
            "access_token": INSTAGRAM_ACCESS_TOKEN,
        },
        timeout=30,
    )

    if not response.ok:
        print("❌ Instagram: publikování selhalo.")
        print(response.text)
        response.raise_for_status()

    return response.json()["id"]


def publish_instagram(post: Post) -> bool:
    """Zveřejní příspěvek z Content Planneru na Instagram."""

    try:
        print("📷 Připravuji Instagram příspěvek...")
        print(f"📄 Název: {post.title}")

        if not post.media:
            print("❌ Instagram příspěvek nemá obrázek.")
            return False

        image_url = post.media[0]

        caption = post.text.strip()

        if post.title and not caption:
            caption = post.title.strip()

        print(f"🖼️ Obrázek: {image_url}")
        print(f"📝 Text: {caption}")

        container_id = create_media_container(
            image_url=image_url,
            caption=caption,
        )

        print(f"✅ Instagram container: {container_id}")

        wait_for_container(container_id)

        print("🚀 Publikuji na Instagram...")

        media_id = publish_media(container_id)

        print(f"✅ Instagram zveřejněn. Media ID: {media_id}")

        return True

    except Exception as error:
        print("❌ Instagram publikování selhalo.")
        print(f"Chyba: {error}")
        return False