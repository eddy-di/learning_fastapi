import uuid


def generate_uuid() -> str:
    """Generates new uuid for new models instances."""

    return str(uuid.uuid4())
