from typing import Any

from ..mode.base_mode import BaseMode
from ..mode.signals import ModeSignal, PushSignal
from .event_strategy import EventStrategy


class ModeLauncherStrategy[T: BaseMode](EventStrategy):
    """指定された Mode クラスをインスタンス化して PushSignal を返す汎用ランチャー戦略"""

    def __init__(self, mode_class: type[T]):
        self.mode_class = mode_class

    def execute(self, context: Any) -> ModeSignal:
        # 渡された Mode クラス（ShopMode や InnMode）を生成して PushSignal を返す！
        return PushSignal(self.mode_class(context))
