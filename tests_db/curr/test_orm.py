import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from podcast.domainmodel.model import (
    Author,
    Podcast,
    Category,
    User,
    PodcastSubscription,
    Episode,
    AudioTime,
    Comment,
    Review,
    Playlist,
)


# ORM Tests Config

def insert_user(empty_session, values=None):
    new_name = "Meow"
    new_password = "Testing235"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT user_id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT user_id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_author(empty_session, values=None):
    new_id = 1
    new_name = "Meow"

    if values is not None:
        new_id = values[0]
        new_name = values[1]

    empty_session.execute('INSERT INTO authors (author_id, name) VALUES (:author_id, :name)',
                          {'author_id': new_id, 'name': new_name})
    row = empty_session.execute('SELECT author_id from authors where name = :name',
                                {'name': new_name}).fetchone()
    return row[0]


def insert_authors(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO authors (author_id, name) VALUES (:author_id, :name)',
                              {'author_id': value[0], 'name': value[1]})
    rows = list(empty_session.execute('SELECT author_id from authors'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_podcast(empty_session):
    empty_session.execute(
        'INSERT INTO podcasts (podcast_id, title, image_url, description, language, website_url) VALUES '
        '(100, "Joe Toste Podcast - Sales Training Expert", '
        '"https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus", '
        '"The first case of coronavirus has been confirmed in New Zealand  and authorities are now scrambling to track down people who may have come into contact with the patient.", '
        '"https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus", '
        '"https://resources.stuff.co.nz/content/dam/images/1/z/e/3/w/n/image.related.StuffLandscapeSixteenByNine.1240x700.1zduvk.png/1583369866749.jpg")'
    )
    row = empty_session.execute('SELECT podcast_id from podcasts').fetchone()
    return row[0]


def insert_categories(empty_session):
    empty_session.execute(
        'INSERT INTO categories (category_name) VALUES ("Society & Culture"), ("Professional")'
    )
    rows = list(empty_session.execute('SELECT id from categories'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_podcast_categories_associations(empty_session, podcast_key, category_keys):
    stmt = 'INSERT INTO podcast_categories (podcast_id, category_id) VALUES (:podcast_id, :category_id)'
    for category_key in category_keys:
        empty_session.execute(stmt, {'podcast_id': podcast_key, 'category_id': category_key})


def make_user():
    return User(1, "Shyamli", "Testing235")


def make_author():
    return Author(1, "Joe Toste")


def make_podcast():
    my_author = make_author()
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


# ORM Tests

# User Tests

def test_loading_of_users(empty_session):
    users = list()
    users.append((1, "Shaymli", "Testing235"))
    users.append((2, "Asma", "Testing111"))
    insert_users(empty_session, users)

    expected = [
        User(1, "Shaymli", "Testing235"),
        User(2, "Asma", "Testing111")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("shyamli", "Testing235")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("shyamli", "Testing1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(1,"shyamli", "Testing111")
        empty_session.add(user)
        empty_session.commit()

# Author Tests

def test_loading_of_authors(empty_session):
    authors = list()
    authors.append((1, "Shaymli"))
    authors.append((2, "Asma"))
    insert_authors(empty_session, authors)

    expected = [
        Author(1, "Shaymli"),
        Author(2, "Asma")
    ]

    assert empty_session.query(Author).all() == expected


def test_saving_of_authors(empty_session):
    author = make_author()
    empty_session.add(author)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT author_id, name FROM authors'))

    assert rows == [(1, 'Joe Toste')]


def test_saving_of_authors_with_common_name(empty_session):
    insert_author(empty_session, (1, 'Joe Toste'))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        author = Author(1,'Joe Toste')
        empty_session.add(author)
        empty_session.commit()

# Podcast Tests

def test_loading_of_podcasts(empty_session):
    podcast_key = insert_podcast(empty_session)
    expected_podcast = make_podcast()
    fetched_podcast = empty_session.query(Podcast).one()

    assert expected_podcast == fetched_podcast
    assert podcast_key == fetched_podcast.id


def test_saving_of_podcast(empty_session):
    podcast = make_podcast()
    empty_session.add(podcast)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT podcast_id, title, image_url, description, language, website_url FROM podcasts'))

    assert rows == [(100, 'Joe Toste Podcast - Sales Training Expert', None, '', 'Unspecified', '')]





