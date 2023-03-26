from abc import ABC, abstractmethod
from typing import List, Optional


class PreprocessingOp(ABC):

    @abstractmethod
    def preprocess(self, text: str) -> str:
        pass

    def __call__(self, text: str) -> str:
        return self.preprocess(text)


class NewLinePadderOp(PreprocessingOp):

    def preprocess(self, text: str) -> str:
        return f"{text}\n"


class ToLowercaseOp(PreprocessingOp):

    def preprocess(self, text: str) -> str:
        return text.lower()


class RemoveSubstringOp(PreprocessingOp):

    def __init__(self, substring: str):
        self._substring = substring

    def preprocess(self, text: str) -> str:
        return text.replace(self._substring, '')


class FilterLinesOp(PreprocessingOp):

    def __init__(self, lines_to_remove: Optional[List[str]] = None):
        self._lines_to_remove = lines_to_remove or []

    def preprocess(self, text: str) -> str:
        lines = text.split('\n')
        return ''.join([
            line for line in lines if not line.isspace() and not any([line.strip().startswith(x)
                                                                      for x in self._lines_to_remove])
        ])
