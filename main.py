import time
from datetime import datetime

from config import validate_config
from notion import get_posts, update_post_status
from publisher import publish_post


CHECK_INTERVAL = 60  # kontrola Notionu každých 60 sekund


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
    print("🚀 Content Planner Worker startuje...\n")

    validate_config()

    print("✅ Konfigurace OK")
    print(
        f"🔄 Notion kontroluji každých "
        f"{CHECK_INTERVAL} sekund."
    )
    print("🟢 Worker běží. CTRL+C = ukončení.\n")

    while True:
        try:
            print("=" * 60)
            print(
                "🔎 Kontrola:",
                datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            )

            process_posts()

        except Exception as error:
            # Jedna chyba nesmí shodit celý worker.
            print("❌ Kontrola skončila chybou.")
            print(f"Chyba: {error}")

        print(
            f"\n💤 Další kontrola za "
            f"{CHECK_INTERVAL} sekund...\n"
        )

        try:
            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n🛑 Content Planner ukončen.")
            break


if __name__ == "__main__":
    main()