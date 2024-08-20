from pathlib import Path

from podcast.adapters.repository import AbstractRepository, RepositoryException
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.domainmodel.model import (Author, Podcast, Category, User, PodcastSubscription, Episode, AudioTime,
                                       Comment, Review, Playlist)


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self._podcasts = []
        self._episodes = []
        self._authors = {}
        self._categories = {}
        self._podcasts_by_category = {}

    # Getter for _podcasts
    @property
    def podcasts(self):
        return self._podcasts

    # Setter for _podcasts
    @podcasts.setter
    def podcasts(self, value):
        self._podcasts = value

    # Getter for _episodes
    @property
    def episodes(self):
        return self._episodes

    # Setter for _episodes
    @episodes.setter
    def episodes(self, value):
        self._episodes = value

    # Getter for _authors
    @property
    def authors(self):
        return self._authors

    # Setter for _authors
    @authors.setter
    def authors(self, value):
        self._authors = value

    # Getter for _categories
    @property
    def categories(self):
        return self._categories

    # Setter for _categories
    @categories.setter
    def categories(self, value):
        self._categories = value

    # Getter for _podcasts_by_category
    @property
    def podcasts_by_category(self):
        return self._podcasts_by_category

    # Setter for _podcasts_by_category
    @podcasts_by_category.setter
    def podcasts_by_category(self, value):
        self._podcasts_by_category = value

    def get_n_podcasts(self, n):
        raise NotImplementedError

    def get_podcast(self, pc_id):
        return self._podcasts[pc_id-1]

    def get_popular_categories(self):
        popular_categories = list(self._categories.values())[5:8]
        return popular_categories

    def get_editor_picks(self):
        return self._podcasts[112:115]

    def get_podcast_search_list(self):
        return self._podcasts[90:94]

    def get_podcasts_in_category(self, category_name):
        return self._podcasts_by_category[category_name]

    def get_all_podcasts(self):
        return self._podcasts

    def get_all_categories(self):
        all_categories = list(self._categories.values())
        return all_categories

    def get_top_podcasts(self):
        recently_played_podcasts = self._podcasts[:4]
        return recently_played_podcasts

    def get_recently_played(self):
        recently_played_podcasts = self._podcasts[4:8]
        return recently_played_podcasts

    def get_new_podcasts(self):
        recently_played_podcasts = self._podcasts[8:12]
        return recently_played_podcasts

    def get_continue_listening_podcasts(self):
        continue_listening_podcasts = self._podcasts[18:22]
        return continue_listening_podcasts

    def get_top_authors(self):
        top_authors = list(self._authors.keys())[:3]
        return top_authors


def populate(data_path: Path, repo: MemoryRepository):
    # create instance of csvreader
    podcasts_csv_path = data_path / "podcasts.csv"
    episodes_csv_path = data_path / "episodes.csv"

    csvdatareader_instance = CSVDataReader(podcasts_csv_path, episodes_csv_path)

    repo.podcasts = csvdatareader_instance.podcasts
    repo.episodes = csvdatareader_instance.episodes
    repo.authors = csvdatareader_instance.authors
    repo.categories = csvdatareader_instance.categories
    repo.podcasts_by_category = csvdatareader_instance.podcasts_by_category
