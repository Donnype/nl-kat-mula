from .services import HTTPService


class Rocky:
    name = "rocky"

    def __init__(self, *args, **kwargs):
        pass


class RockyV1(HTTPService):
    name = "rocky"
