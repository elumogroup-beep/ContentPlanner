from datetime import datetime

from config import validate_config
from notion import get_posts, update_post_status
from publisher import publish_post


def process_posts() -> None:
    """Zkontroluje Notion a zpracuje připravené příspěvky."""

    posts = get_posts()

    print(f"📄 Připravených příspěvků: {len(posts)}")

    for post in posts:
        print("-" * 50)
        print(f"📄 Název: {post.title}")
        print(f"🌍 Síť: {post.network}")
        print(f"📅 Datum: {post.publish_date}")
        print(f"📌 Stav: {post.status}")

        if post.publish_date is None:
            print("⚠️ Příspěvek nemá datum publikace.")
            continue

        now = datetime.now(post.publish_date.tzinfo)

        if post.publish_date > now:
            print("⏳ Čas publikace ještě nenastal.")
            continue

        print("✅ Nastal čas publikace.")

        try:
            success = publish_post(post)

            if success:
                print("✅ Publikování proběhlo.")

                update_post_status(
                    post.id,
                    "🚀 Publikováno",
                )

                print(
                    "✅ Stav v Notionu změněn "
                    "na Publikováno."
                )

            else:
                print(
                    "❌ Publisher příspěvek "
                    "nezpracoval."
                )

        except Exception as error:
            print("❌ Chyba při zpracování příspěvku.")
            print(f"Chyba: {error}")


def main() -> None:
    print("🚀 Content Planner startuje...\n")

    validate_config()

    print("✅ Konfigurace OK")

    print("=" * 60)
    print(
        "🔎 Kontrola:",
        datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
    )

    try:
        process_posts()

    except Exception as error:
        print("❌ Kontrola skončila chybou.")
        print(f"Chyba: {error}")

    print("\n🏁 Content Planner dokončil kontrolu.")


if __name__ == "__main__":
    main()