import requests

from config import (
    THREADS_ACCESS_TOKEN,
    THREADS_USER_ID,
)
from models.post import Post


API_VERSION = "v1.0"
BASE_URL = f"https://graph.threads.net/{API_VERSION}"


def create_text_container(text: str) -> str:
    """Vytvoří textový Threads container."""

    url = f"{BASE_URL}/{THREADS_USER_ID}/threads"

    response = requests.post(
        url,
        data={
            "media_type": "TEXT",
            "text": text,
            "access_token": THREADS_ACCESS_TOKEN,
        },
        timeout=30,
    )

    if not response.ok:
        print("❌ Threads: vytvoření textového containeru selhalo.")
        print(response.text)
        response.raise_for_status()

    return response.json()["id"]


def create_image_container(
    image_url: str,
    text: str,
) -> str:
    """Vytvoří Threads příspěvek s obrázkem."""

    url = f"{BASE_URL}/{THREADS_USER_ID}/threads"

    response = requests.post(
        url,
        data={
            "media_type": "IMAGE",
            "image_url": image_url,
            "text": text,
            "access_token": THREADS_ACCESS_TOKEN,
        },
        timeout=30,
    )

    if not response.ok:
        print("❌ Threads: vytvoření image containeru selhalo.")
        print(response.text)
        response.raise_for_status()

    return response.json()["id"]


def publish_container(container_id: str) -> str:
    """Zveřejní vytvořený Threads container."""

    url = f"{BASE_URL}/{THREADS_USER_ID}/threads_publish"

    response = requests.post(
        url,
        data={
            "creation_id": container_id,
            "access_token": THREADS_ACCESS_TOKEN,
        },
        timeout=30,
    )

    if not response.ok:
        print("❌ Threads: publikování selhalo.")
        print(response.text)
        response.raise_for_status()

    return response.json()["id"]


def publish_threads(post: Post) -> bool:
    """Publikuje Notion příspěvek na Threads."""

    try:
        print("🧵 Připravuji Threads příspěvek...")

        text = post.text.strip()

        if not text:
            text = post.title.strip()

        if not text:
            print("❌ Threads příspěvek nemá žádný text.")
            return False

        print(f"📄 Název: {post.title}")
        print(f"📝 Text: {text}")

        if post.media:
            image_url = post.media[0]

            print(f"🖼️ Obrázek: {image_url}")

            container_id = create_image_container(
                image_url=image_url,
                text=text,
            )

        else:
            container_id = create_text_container(
                text=text,
            )

        print(f"✅ Threads container: {container_id}")
        print("🚀 Publikuji na Threads...")

        thread_id = publish_container(container_id)

        print(f"✅ Threads zveřejněn. ID: {thread_id}")

        return True

    except Exception as error:
        print("❌ Publikování na Threads selhalo.")
        print(f"Chyba: {error}")

        return False