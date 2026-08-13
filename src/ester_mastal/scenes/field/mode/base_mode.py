from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .signals import ModeSignal

if TYPE_CHECKING:
    from ..field_scene import FieldScene


@dataclass
class FieldContext:
    """全モード間で共有する共通コンテキスト（データやリソースのバケツ）"""

    scene: FieldScene


@dataclass
class BaseModeData:
    """イベントデータの基底クラス"""

    name: str | None = None


class BaseMode(ABC):
    """すべてのフィールドモード（探索・メニュー・ショップ等）の基底クラス"""

    def __init__(self, context: FieldContext):
        self._context = context  # 共有データを受け取って保持
        self._scene = self._context.scene
        self._app = self._scene.app
        self._wm = self._scene.window_manager

    @abstractmethod
    def update(self) -> ModeSignal:
        """
        毎フレームの入力処理・更新ロジック。
        戻り値としてスタック操作命令（ModeSignal, PushSignal, PopSignal など）を返す。
        """

    @abstractmethod
    def draw(self) -> None:
        """毎フレームのUI・画面描画処理"""
