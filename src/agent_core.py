from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Protocol, runtime_checkable


@dataclass(frozen=True)
class Message:
    type: str
    payload: Dict[str, Any]


@runtime_checkable
class Agent(Protocol):
    """Agents process messages and can publish new ones via the provided publish callable.

    Agents must be stateless or manage only local state; no hidden globals.
    """

    name: str

    def on_message(self, msg: Message, publish: Callable[[Message], None]) -> None: ...


class EventBus:
    """Simple synchronous pub/sub event bus to coordinate autonomous agents.

    - Agents subscribe by message type.
    - Publishing a message fan-outs to all subscribers of that type.
    - Messages are processed synchronously in FIFO order (deterministic for this task).
    """

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Agent]] = {}
        self._queue: List[Message] = []

    def subscribe(self, message_type: str, agent: Agent) -> None:
        self._subscribers.setdefault(message_type, []).append(agent)

    def publish(self, msg: Message) -> None:
        self._queue.append(msg)

    def run(self) -> None:
        while self._queue:
            msg = self._queue.pop(0)
            for agent in list(self._subscribers.get(msg.type, [])):
                agent.on_message(msg, self.publish)
