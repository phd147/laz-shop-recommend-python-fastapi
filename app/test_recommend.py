#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

# get lastest id of user
n_user = 7

# get lastest id of item
n_item = 5

# get data in ratting table
stars = [  # user, item, star
    [0, 0, 5],
    [0, 1, 4],
    [0, 3, 2],
    [0, 4, 2],
    [1, 0, 5],
    [1, 2, 4],
    [1, 3, 2],
    [1, 4, 0],
    [2, 0, 2],
    [2, 2, 1],
    [2, 3, 3],
    [2, 4, 4],
    [3, 0, 0],
    [3, 1, 0],
    [3, 3, 4],
    [4, 0, 1],
    [4, 3, 4],
    [5, 1, 2],
    [5, 2, 1],
    [6, 2, 1],
    [6, 3, 4],
    [6, 4, 5],
]

# print result to check
# matrix = [[0 for x in range(n_user)] for y in range(n_item)]
# for item in stars:
#   matrix[item[1]][item[0]] = item[2]
# for i in matrix:
#   print(i)

# init average of star of user, which user rate for all item
avg = [0] * n_user

# find average
for i in range(n_user):
    count = 0
    sum = 0
    for star in stars:
        if star[0] == i:
            count += 1
            sum += star[2]
    if count != 0:
        avg[i] = sum / count

# normalized utility matrix
for i in range(len(stars)):
    stars[i][2] -= avg[stars[i][0]]

# print result to check
# matrix = [[0 for x in range(n_user)] for y in range(n_item)]
# for item in stars:
#   matrix[item[1]][item[0]] = item[2]
# for i in matrix:
#   print(i)

# init similarity matrix
similarity = []

# get id of user suggest
user_suggest = 4

# get number of neighborhood is validate
k = 2

# get input ratting of user suggest for cosine_similarity
item_of_user_suggest = [0] * n_item
for item in stars:
    if item[0] == user_suggest:
        item_of_user_suggest[item[1]] = item[2]
item_of_user_suggest = [item_of_user_suggest]

# import cosine_similarity from sklearn library
from sklearn.metrics.pairwise import cosine_similarity

# calculator for similarity matrix
for i in range(n_user):
    if i != user_suggest:
        item_of_user = [0] * n_item
        for item in stars:
            if item[0] == i:
                item_of_user[item[1]] = item[2]
        item_of_user = [item_of_user]
        similarity.append({'id': i,
                           'cosine': cosine_similarity(item_of_user_suggest,
                                                       item_of_user)[0][0]})


# get ratting star by user_id and item_id
def get_star(user_id, item_id, stars):
    for item in stars:
        if item[0] == user_id and item[1] == item_id:
            return item[2]
    return -1


similarity = sorted(similarity, key=lambda i: i['cosine'], reverse=True)

# check similarity matrix
# for i in similarity:
#   print(i)

item_of_user_suggest = item_of_user_suggest[0]

suggest_item = []

# fill star missing for user suggest
for item_id in range(len(item_of_user_suggest)):
    if item_of_user_suggest[item_id] == 0:
        count = 0
        top = 0
        bot = 0
        for simi in similarity:
            star = get_star(simi['id'], item_id, stars)
            if star != -1:
                top += simi['cosine'] * star
                bot += abs(simi['cosine'])
                count += 1
                if count >= k: break
        if bot > 0:
            predit_star = top / bot + avg[user_suggest]
            if predit_star >= 3:
                suggest_item.append({
                    'id': item_id,
                    'star': predit_star
                })

print(suggest_item)
