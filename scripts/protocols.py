from typing import Protocol, Any


class GameProtocol(Protocol):
    """Describes the interface that game objects must provide to scripts."""
    assets: dict[str, Any]
