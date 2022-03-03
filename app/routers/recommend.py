import copy

import numpy as np

from fastapi import APIRouter, Depends
# import cosine_similarity from sklearn library
from sklearn.metrics.pairwise import cosine_similarity

from scipy import spatial

from sqlalchemy.orm import Session

from ..models.item import Item
from ..models.reaction import Reaction

from ..util.math import calculate_cosine_similarity

from ..dependecies.database import get_db

router = APIRouter()


def getNormalizedRating(normalized_matrix, user_id, item_id):
    result = 0
    for reaction in normalized_matrix:
        if reaction[0] == user_id and reaction[1] == item_id:
            return reaction[2]

    return result


def getVectorOfUser(items, user_id, normalized_matrix):
    item_rating_vector_of_user = []
    for item in items:
        item_rating_vector_of_user.append(
            {'item_id': item, 'normalized_rating': getNormalizedRating(normalized_matrix, user_id, item)})

    print(f'============Vector of user: {user_id}============', item_rating_vector_of_user)
    return item_rating_vector_of_user


def getAllRatingItemOfUser(items, user_id, matrix):
    item_rating_vector_of_user = []
    for item in items:
        item_rating_vector_of_user.append(
            {'item_id': item, 'rating': getNormalizedRating(matrix, user_id, item)})

    print(f'ALL RATING FOR ITEM OF USER {user_id}', item_rating_vector_of_user)
    return item_rating_vector_of_user


# def getNormalizedRatingItemVetor(user_id,item_id, normalizedMatrix )


def getAvgRatingOfUser(avg, user_id):
    for i in avg:
        if i['user_id'] == user_id:
            return i['avg_rating']


def get_recommend(stars, user_id):
    # !/usr/bin/python
    # -*- coding: utf-8 -*-

    user_ratings = list(set([reaction[0] for reaction in stars]))

    items = list(set([reaction[1] for reaction in stars]))

    print(user_ratings, items)

    '''
       check if user suggest do not rating 
       TODO : // suggest another solution
       '''

    if user_id not in user_ratings:
        return []

    avg_plus = [{'user_id': user, 'avg_rating': 0.00} for user in user_ratings]

    # avg_plus = {}

    normalized_matrix = copy.deepcopy(stars)

    for i in range(len(avg_plus)):
        count = 0
        sum = 0
        for reaction in stars:
            if reaction[0] == avg_plus[i]['user_id']:
                count += 1
                sum += reaction[2]
        if count != 0:
            avg_plus[i]['avg_rating'] = round(sum / count, 2)

    print('=======AVG RATING=======', avg_plus)

    # normalized utility matrix
    for i in range(len(stars)):
        # matrix[i][2] -= avg_plus[matrix[i][0]]
        # if(matrix[i][0] == avg_plus[])

        for user_avg_rating in avg_plus:
            if user_avg_rating['user_id'] == stars[i][0]:
                normalized_matrix[i][2] -= user_avg_rating['avg_rating']

    print('========MATRIX========', np.array(stars))
    print('========NORMALIZED MATRIX===========', np.array(normalized_matrix))

    # init similarity matrix
    similarity = []

    # get id of user suggest
    user_suggest = user_id

    # get number of neighborhood is validate
    k = 2

    '''
    Get vector of item_rating_of_user_suggest
    '''
    item_rating_vector_of_user_suggest = getVectorOfUser(items, user_suggest, normalized_matrix)

    print('item_rating_vector_of_user_suggest', item_rating_vector_of_user_suggest)

    for user_id in user_ratings:
        if user_id != user_suggest:
            user_suggest_vector = [i['normalized_rating'] for i in item_rating_vector_of_user_suggest]
            user_similar_vector = [i['normalized_rating'] for i in getVectorOfUser(items, user_id, normalized_matrix)]
            print('user_suggest_vector', user_suggest_vector)
            print('user_similar_vector', user_similar_vector)
            similarity.append({
                'user_id': user_id,
                'cosine': calculate_cosine_similarity(user_suggest_vector, user_similar_vector)
            })

    similarity = sorted(similarity, key=lambda i: i['cosine'], reverse=True)

    similarity = similarity[:k]
    print('========SIMILARITY OF USER SUGGEST=========', similarity)

    suggest_item = []

    '''
    Fill missing star for suggest user
    '''

    # get normalized star by user_id and item_id
    def get_star(user_id, item_id, matrix):
        for item in matrix:
            if item[0] == user_id and item[1] == item_id:
                return item[2]
        return -1

    avg_rating_of_suggest_user = getAvgRatingOfUser(avg_plus, user_suggest)
    print('========AVG RATING OF USER SUGGEST=========', avg_rating_of_suggest_user)

    all_rating_of_user = getAllRatingItemOfUser(items, user_suggest, stars)
    print('=============ALL RATING OF USER SUGGEST===============', all_rating_of_user)

    for item in all_rating_of_user:
        if item['rating'] == 0:
            count = 0
            numerator = 0
            denominator = 0

            for i in similarity:

                star = get_star(i['user_id'], item['item_id'], normalized_matrix)
                if star != -1:
                    numerator += i['cosine'] * star
                    denominator += abs(i['cosine'])
                    count += 1
            if denominator > 0:
                predict_star = numerator / denominator + avg_rating_of_suggest_user
                if predict_star >= 3:
                    suggest_item.append({
                        'id': item,
                        'predict_rating': predict_star
                    })

    print(suggest_item)

    suggest_item = sorted(suggest_item, key=lambda x: x['predict_rating'], reverse=True)

    print('final highest predict rating suggest item', suggest_item)

    return suggest_item


@router.get('/items')
def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    print(type(items[0]))
    return items


@router.get('/recommend/{user_id}')
def get_items(db: Session = Depends(get_db), user_id: int = 5):
    reactions = db.query(Reaction).all()

    matrix = [[reaction.user_id, reaction.item_id, reaction.star] for reaction in reactions]

    print(matrix)
    print(type(reactions[0]))
    result = get_recommend(matrix, user_id=user_id)

    return result
#
