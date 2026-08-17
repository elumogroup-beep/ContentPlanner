import requests

from config import (
    FACEBOOK_PAGE_ACCESS_TOKEN,
    FACEBOOK_PAGE_ID,
)
from models.post import Post


API_VERSION = "v26.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


def debug_facebook_token():
    token = FACEBOOK_PAGE_ACCESS_TOKEN or ""

    print("🔑 Facebook token diagnostika:")
    print(f"   délka: {len(token)}")

    if len(token) >= 10:
        print(f"   začátek: {token[:6]}...")
        print(f"   konec: ...{token[-6:]}")
    else:
        print("   ❌ Token je prázdný nebo příliš krátký.")


def publish_text_post(message: str) -> str:
    url = f"{BASE_URL}/{FACEBOOK_PAGE_ID}/feed"

    response = requests.post(
        url,
        data={
            "message": message,
            "access_token": FACEBOOK_PAGE_ACCESS_TOKEN,
        },
        timeout=30,
    )

    if not response.ok:
        print("❌ Facebook API chyba:")
        print(response.text)
        response.raise_for_status()

    return response.json()["id"]


def publish_photo_post(image_url: str, caption: str) -> str:
    url = f"{BASE_URL}/{FACEBOOK_PAGE_ID}/photos"

    response = requests.post(
        url,
        data={
            "url": image_url,
            "caption": caption,
            "published": "true",
            "access_token": FACEBOOK_PAGE_ACCESS_TOKEN,
        },
        timeout=60,
    )

    if not response.ok:
        print("❌ Facebook API chyba při publikování obrázku:")
        print(response.text)
        response.raise_for_status()

    data = response.json()

    return data.get("post_id") or data.get("id", "")


def publish_facebook(post: Post) -> bool:
    try:
        print("📘 Připravuji Facebook příspěvek...")

        debug_facebook_token()

        message = post.text.strip()

        if not message:
            message = post.title.strip()

        print(f"📄 Název: {post.title}")
        print(f"📝 Text: {message}")

        if post.media:
            image_url = post.media[0]

            print(f"🖼️ Obrázek: {image_url}")
            print("🚀 Publikuji obrázek na Facebook...")

            post_id = publish_photo_post(
                image_url=image_url,
                caption=message,
            )

        else:
            print("🚀 Publikuji text na Facebook...")

            post_id = publish_text_post(message)

        print(f"✅ Facebook zveřejněn. Post ID: {post_id}")

        return True

    except Exception as error:
        print("❌ Publikování na Facebook selhalo.")
        print(f"Chyba: {error}")

        return False