from podcast.adapters.repository import AbstractRepository


def format_podcast_list(podcasts, repo=None):
    formatted_podcasts = []
    for i in range(len(podcasts)):
        about_podcast = dict()

        about_podcast["id"] = podcasts[i].id
        about_podcast["title"] = podcasts[i].title
        about_podcast["author"] = podcasts[i].author.name
        about_podcast["image_url"] = podcasts[i].image
        about_podcast["language"] = podcasts[i].language
        if repo is not None:
            if len(podcasts[i].episodes) > 0:
                audio_times = [
                    episode.episode_audio_length for episode in podcasts[i].episodes
                ]
                total_time = repo.get_total_audio_time(audio_times)
                about_podcast["duration"] = total_time.colon_format()
            else:
                about_podcast["duration"] = "8:32:25"

        category_list = [category.name for category in podcasts[i].categories]
        if len(category_list) > 1:
            category_list = " | ".join(category_list)
        else:
            category_list = podcasts[i].categories[0].name

        about_podcast["categories"] = category_list

        formatted_podcasts.append(about_podcast)

    return formatted_podcasts


def get_user_playlist_podcasts(repo_instance):
    podcasts = repo_instance.get_recently_played_list()
    formatted_podcasts = format_podcast_list(sorted(podcasts))
    return formatted_podcasts


def get_user_playlist_episodes(repo_instance):
    podcasts = repo_instance.get_new_podcasts_list()
    formatted_podcasts = format_podcast_list(sorted(podcasts))
    return formatted_podcasts
