# modes/signals.py
from dataclasses import dataclass
from typing import Any


class ModeSignal:
    """基本シグナル（何もしない）"""

class PopSignal(ModeSignal):
        """スタックから自分（現在のモード）を取り除いて1つ前へ戻る命令"""

@dataclass
class PushSignal(ModeSignal):
    """新しいモードをスタックに積む命令"""
    new_mode: Any