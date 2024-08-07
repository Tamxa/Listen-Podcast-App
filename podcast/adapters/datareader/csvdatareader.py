import os
import csv
from datetime import datetime

from podcast.domainmodel.model import Podcast, Episode, Author, Category, AudioTime


class CSVDataReader:
    def __init__(self):
        self._podcasts, self._episodes = [], []
        self._authors, self._categories = dict(), dict()
        self._podcasts_by_category = {}

        self.create_podcasts("../data/podcasts.csv")
        self.create_episodes("../data/episodes.csv")

    def read_csv(self, input_file: str):
        with open(input_file, mode='r') as file_in:
            csv_data = csv.reader(file_in, delimiter=',')
            headers = next(csv_data)  # read the headers

            for row in csv_data:
                # Strip any leading/trailing white space.
                row = [item.strip() for item in row]
                yield row

    def create_podcasts(self, podcast_file):
        a_id = 1
        try:
            for row in self.read_csv(podcast_file):
                # pc = podcast - using these variables as keyword arguments for better readability
                pc_id, pc_title = int(row[0]), row[1]
                pc_image, pc_description = row[2], row[3]
                pc_language = row[4]
                pc_categories, pc_website = row[5], row[6]
                pc_author, pc_itunes_id = row[7], int(row[8])

                # Create Author Object if it doesn't already exist
                if pc_author not in self._authors:
                    author = Author(
                        author_id=a_id,
                        name=pc_author if len(pc_author) > 0 else "Author Not Provided"
                    )
                    a_id += 1
                    self._authors[pc_author] = author

                # Create Podcast Object
                new_podcast = Podcast(
                    podcast_id=pc_id, title=pc_title,
                    image=pc_image, description=pc_description,
                    language=pc_language,
                    website=pc_website, author=self._authors[pc_author],
                    itunes_id=pc_itunes_id
                )

                # Create Categories
                c_id = 1
                for c in pc_categories.split(' | '):
                    category: Category = None
                    if c in self._categories:
                        category = self._categories[c]
                    else:
                        category = Category(
                            category_id=c_id,
                            name=c
                        )
                        c_id += 1
                        self._categories[c] = category

                    if c in self._podcasts_by_category:
                        self._podcasts_by_category[c].append(new_podcast)
                    else:
                        self._podcasts_by_category[c] = [new_podcast]

                    # Add Category to Podcast
                    new_podcast.add_category(category)

                # Add podcast to authors podcast list
                self._authors[pc_author].add_podcast(new_podcast)
                self._podcasts.append(new_podcast)
        except ValueError as e:
            print(f"Skipping row (invalid data): {e}")

    def create_episodes(self, episode_file: str):
        a_id = 1
        try:
            for row in self.read_csv(episode_file):
                # ep = episode
                ep_id, pc_id = int(row[0]), int(row[1])
                ep_title, ep_audio_link = row[2], row[3]
                ep_audio_length = row[4]
                ep_description, ep_pub_date = row[5], row[6]

                ep_pub_date = ep_pub_date.replace('+00', '+0000')
                ep_pub_date_object = datetime.strptime(ep_pub_date, "%Y-%m-%d %H:%M:%S%z")

                hours = int(ep_audio_length) // 3600
                minutes = (int(ep_audio_length) % 3600) // 60
                seconds = int(ep_audio_length) % 60
                ep_audio_length_object = AudioTime(hours, minutes, seconds)

                for pcast in self._podcasts:
                    if pcast.id == pc_id:
                        episode_pcast = pcast

                # Create Episode Object
                new_episode = Episode(
                    episode_id=ep_id, episode_podcast=episode_pcast,
                    episode_title=ep_title,
                    episode_audio_link=ep_audio_link,
                    episode_audio_length=ep_audio_length_object,
                    episode_description=ep_description,
                    episode_publish_date=ep_pub_date_object
                )

                self._episodes.append(new_episode)

        except Exception as e:
            print(f"Skipping row (invalid data): {e}")

        # for ep in range(0, 12):
        #     print(self._episodes[ep])

        # print(self._episodes[10].episode_podcast == self._episodes[11].episode_podcast)


a = CSVDataReader()
