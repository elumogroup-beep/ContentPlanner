from datetime import datetime


def parse_date(date_string: str | None) -> datetime | None:
    if not date_string:
        return None

    return datetime.fromisoformat(
        date_string.replace("Z", "+00:00")
    )


def is_ready_to_publish(
    publish_date: datetime | None,
) -> bool:
    if publish_date is None:
        return False

    current_time = datetime.now(publish_date.tzinfo)

    return publish_date <= current_time