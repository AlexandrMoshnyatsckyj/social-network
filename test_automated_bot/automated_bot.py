import json
import os
import random

import requests

from faker import Faker
fake = Faker()


def get_info():
    file_path = os.path.abspath('data.json')

    if not os.path.isfile(file_path):
        file_path = get_file_name()

    with open(file_path) as file_info:
        info = json.load(file_info)

    if info:
        return info
    else:
        return Exception('File is empty')


def get_file_name():

    print('Please enter file name')
    file_name = str(input())

    if os.path.abspath(file_name):
        return file_name
    else:
        print('You enter incorrect file path.')
        return get_file_name()


def sig_up(count):
    users_info = [{
        'email': 'test@gmail.com', 'username': fake.name().split(' ')[0], 'password': fake.password()}
        for _ in range(count)]

    for user in users_info:
        response = requests.post(host + '/user/', user)
        assert eval(response.text)['status'] == 201

    return users_info


def get_token(info):

    tokens = []

    for count in range(info.__len__()):
        response = requests.post(host + '/auth/jwt/create/', info[count])
        tokens.append('JWT {}'.format(eval(response.text)['token']))

    return tokens


def create_article(count, tokens):

    for token in tokens:
        for _ in range(count):
            data = {'header': fake.text(20), 'content': fake.text(200)}
            response = requests.post(host + '/api/articles/article/', data, headers={'Authorization': token})
            assert eval(response.text)['status'] == 201


def get_articles(token):

    response = requests.get(host + '/api/articles/article/', headers={'Authorization': token})
    return [article['id'] for article in json.loads(response.text)['data']]


def like_article(count, tokens):

    created_articles = get_articles(tokens[0])
    for token in tokens:
        articles = random.sample(created_articles, count)

        for article_id in articles:
            response = requests.post(host + '/api/articles/article/like/', {"article_id": str(article_id), "type": "like"},
                                     headers={'Authorization': token})
            assert eval(response.text)['status'] == 200
    print('Script finished Success')


def main():
    users_info = sig_up(bot_info['number_of_users'])
    tokens = get_token(users_info)
    create_article(bot_info['max_posts_per_user'], tokens)
    like_article(bot_info['max_likes_per_user'], tokens)


if __name__ == '__main__':

    bot_info = get_info()
    host = bot_info['host']

    main()
