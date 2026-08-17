from models.post import Post


def publish_linkedin(post: Post) -> bool:
    print("💼 TEST: Odesílám příspěvek na LinkedIn")
    print(f"Název: {post.title}")
    print(f"Text: {post.text}")
    return True