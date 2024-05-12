from api.models import APIMessageRawDatagram, MessageMeta


def save_to_input_queue(message: APIMessageRawDatagram, meta: MessageMeta) -> int:
    id = 0

    return id


def update_input_queue(db_id: int, task_id: str) -> None:
    pass
