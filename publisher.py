from models.post import Post
from services.facebook import publish_facebook
from services.instagram import publish_instagram
from services.linkedin import publish_linkedin
from services.threads import publish_threads


def publish_post(post: Post) -> bool:
    network = post.network.strip().lower()

    if network == "instagram":
        return publish_instagram(post)

    if network == "facebook":
        return publish_facebook(post)

    if network == "threads":
        return publish_threads(post)

    if network == "linkedin":
        return publish_linkedin(post)

    print(f"⚠️ Nepodporovaná sociální síť: {post.network}")
    return False