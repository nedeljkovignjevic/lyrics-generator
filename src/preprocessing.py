from abc import ABC, abstractmethod
from typing import List, Optional


START_OF_SONG_TOKEN = '<SOS>'
END_OF_SONG_TOKEN = '<EOS>'
START_OF_VERSE_TOKEN = '<SOV>'
END_OF_VERSE_TOKEN = '<EOV>'


class PreprocessingOp(ABC):

    @abstractmethod
    def preprocess(self, text: str) -> str:
        pass

    def __call__(self, text: str) -> str:
        return self.preprocess(text)


class ToLowercaseOp(PreprocessingOp):

    def preprocess(self, text: str) -> str:
        return text.lower()


class RemoveSubstringOp(PreprocessingOp):

    def __init__(self, substring: str):
        self._substring = substring

    def preprocess(self, text: str) -> str:
        return text.replace(self._substring, '')


class TokenizerOp(PreprocessingOp):

    def __init__(self,
                 lines_to_remove: Optional[List[str]] = None,
                 start_of_song_token: str = START_OF_SONG_TOKEN,
                 end_of_song_token: str = END_OF_SONG_TOKEN,
                 start_of_verse_token: str = START_OF_VERSE_TOKEN,
                 end_of_verse_token: str = END_OF_VERSE_TOKEN):
        self._lines_to_remove = set(lines_to_remove or [])
        self._start_of_song_token = start_of_song_token
        self._end_of_song_token = end_of_song_token
        self._start_of_verse_token = start_of_verse_token
        self._end_of_verse_token = end_of_verse_token

    def is_line_for_removal(self, line: str) -> bool:
        return line.isspace() or any(line.startswith(prefix) for prefix in self._lines_to_remove)

    def preprocess(self, text: str) -> str:
        song = [self._start_of_song_token, self._start_of_verse_token, '\n']
        song_lines = text.split('\n')
        for song_line in song_lines:
            song_line = song_line.strip()
            if self.is_line_for_removal(song_line):
                continue
            song.append(f"{song_line}\n")
        song.extend([self._end_of_verse_token, self._end_of_song_token])
        return ''.join(song)
