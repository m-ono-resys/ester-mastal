from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import App


class BaseScene(ABC):
    def __init__(self, app: App):
        self.app = app  # main.py の App インスタンスへの参照

    @abstractmethod
    def update(self):
        """毎フレームのロジック更新"""

    @abstractmethod
    def draw(self):
        """毎フレームの画面描画"""
