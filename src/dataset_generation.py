"""
This file is only used to generate training data for a neural network, and thus
most not be used to download any content from https://tekstovi.net/2,0,0.html for
offline-browsing, as described in their license.
"""

import multiprocessing as mp
import os
import requests
from typing import Optional, List, Iterator

from bs4 import BeautifulSoup, element

from src.preprocessing import PreprocessingOp


BASE_URL = "https://tekstovi.net/"


class SongsPage:

    def __init__(self, url: str):
        page = requests.get(url)
        self._soup = BeautifulSoup(page.content, 'html.parser')

    @staticmethod
    def extract_text_from_element(html_element: element.Tag) -> Optional[str]:
        if not html_element:
            return None

        return html_element.text.strip()

    def singer_name(self) -> Optional[str]:
        singer_name_element = self._soup.find(class_='lyricCapt')
        return SongsPage.extract_text_from_element(singer_name_element)

    def has_content(self) -> bool:
        singer_name = self.singer_name()
        return singer_name is not None

    @staticmethod
    def scrape_song(url: str) -> Optional[str]:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        song_lyrics_element = soup.find(class_='lyric')
        return SongsPage.extract_text_from_element(song_lyrics_element)

    def parse_songs(self) -> Iterator[str]:
        for song_html in self._soup.find_all(class_='artLyrList'):
            url = f"{BASE_URL}{song_html.find('a')['href']}"
            song = SongsPage.scrape_song(url)
            if song:
                yield song


class SingerScraperWorker:

    def __init__(self, singer_id: int, output_dir: str, preprocessing_ops: List[PreprocessingOp]):
        self._singer_id = singer_id
        self._url = f"{BASE_URL}/2,{singer_id},0.html"
        self._output_dir = output_dir
        self._preprocessing_ops = preprocessing_ops

    def preprocess_song(self, song: str) -> str:
        for preprocessing_op in self._preprocessing_ops:
            song = preprocessing_op(song)
        return song

    def run(self) -> None:
        songs_page = SongsPage(self._url)
        if not songs_page.has_content():
            return

        singer_name = songs_page.singer_name()
        singer_output_file = os.path.join(self._output_dir, f"{singer_name}_{self._singer_id}.txt")

        with open(singer_output_file, 'w', encoding='utf-8') as singer_file:
            for song in songs_page.parse_songs():
                song = self.preprocess_song(song)
                singer_file.write(song)


class SongDatasetGenerator:

    def __init__(self,
                 output_dir_path: str,
                 num_singers: int = 10000,
                 num_processes: int = 32,
                 preprocessing_ops: Optional[List[PreprocessingOp]] = None):
        self._output_dir_path = output_dir_path
        self._num_processes = num_processes
        self._num_singers = num_singers
        self._preprocessing_ops = preprocessing_ops or []
        self._singers_processed = 0

        os.makedirs(self._output_dir_path, exist_ok=True)

    def run_singer_scraper_worker(self, singer_id: int):
        worker = SingerScraperWorker(
            singer_id=singer_id,
            output_dir=self._output_dir_path,
            preprocessing_ops=self._preprocessing_ops
        )
        worker.run()

    def run_singer_scraper_workers(self):
        with mp.Pool(processes=self._num_processes) as pool:
            pool.map(self.run_singer_scraper_worker, range(self._num_singers))

    def generate_dataset(self) -> None:
        self.run_singer_scraper_workers()
