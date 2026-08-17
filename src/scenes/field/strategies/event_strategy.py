from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..mode.base_mode import FieldContext
from ..mode.signals import ModeSignal


@dataclass
class BaseEventData:
    """イベントデータの基底クラス"""

    name: str = ""


class EventStrategy[T: BaseEventData](ABC):
    """イベントアクションの戦略（Strategy）基底クラス"""

    @abstractmethod
    def execute(self, context: FieldContext) -> ModeSignal:
        """イベント実行ロジック。必要に応じて ModeSignal (PushSignal等) を返す"""
