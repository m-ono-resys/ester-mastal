from abc import ABC, abstractmethod

class BaseState(ABC):
    def __init__(self, app):
        self.app = app  # main.py の App インスタンスへの参照

    @abstractmethod
    def update(self):
        """毎フレームのロジック更新"""
        pass

    @abstractmethod
    def draw(self):
        """毎フレームの画面描画"""
        pass