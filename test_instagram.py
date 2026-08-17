import time
import requests

from config import INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_USER_ID


IMAGE_URL ="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80"
CAPTION = "První test z Content Planneru 🚀📈"

API_VERSION = "v24.0"
BASE_URL = f"https://graph.instagram.com/{API_VERSION}"


def create_media_container() -> str:
    url = f"{BASE_URL}/{INSTAGRAM_USER_ID}/media"

    response = requests.post(
        url,
        data={
            "image_url": IMAGE_URL,
            "caption": CAPTION,
            "access_token": INSTAGRAM_ACCESS_TOKEN,
        },
        timeout=30,
    )

    if not response.ok:
        print("❌ Chyba při vytvoření containeru:")
        print(response.text)
        response.raise_for_status()

    data = response.json()
    return data["id"]


def wait_for_container(container_id: str) -> None:
    url = f"{BASE_URL}/{container_id}"

    for attempt in range(20):
        response = requests.get(
            url,
            params={
                "fields": "status_code,status",
                "access_token": INSTAGRAM_ACCESS_TOKEN,
            },
            timeout=30,
        )

        if not response.ok:
            print("❌ Chyba při kontrole containeru:")
            print(response.text)
            response.raise_for_status()

        data = response.json()

        status_code = data.get("status_code")
        status = data.get("status")

        print(
            f"⏳ Stav containeru: {status_code} "
            f"({status or 'bez detailu'})"
        )

        if status_code == "FINISHED":
            return

        if status_code in {"ERROR", "EXPIRED"}:
            raise RuntimeError(
                f"Instagram container selhal: {data}"
            )

        time.sleep(3)

    raise TimeoutError(
        "Container nebyl připraven ani po 60 sekundách."
    )


def publish_media(container_id: str) -> str:
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
        print("❌ Instagram media_publish vrátil chybu:")
        print(response.text)
        response.raise_for_status()

    data = response.json()
    return data["id"]


def main():
    print("📷 Vytvářím Instagram container...")

    container_id = create_media_container()
    print(f"✅ Container: {container_id}")

    print("⏳ Čekám, než Instagram zpracuje obrázek...")
    wait_for_container(container_id)

    print("🚀 Publikuji...")
    media_id = publish_media(container_id)

    print(f"✅ Zveřejněno! Media ID: {media_id}")


if __name__ == "__main__":
    main()