import unittest

from src.helpers import *
from src.operations import *
from src.load_data import *
from src.analyze import *

def evaluation(recommendations,ratings,user_id,item_id='movie_id',explore=True):
    """ Take as imput recommendations a dataframe of recommended items
                      ratings the ratings dataframe
                      user_id an integer the ID of the user
                      item_id a src which denotes the associated columns name is in the case of a different dataset than movie
                      explore a boolean, to precise if we encourage new items

        The purpose of this function is to evaluation at which point is a recommendation efficient

        return n, an integer which is as greater as the recommendations if efficient
    """
    userRatings=ratings[ratings['user_id']==user_id]
    movies_ids_recommanded=recommendations[item_id].values
    ratedmovies=userRatings['movie_id'].values
    n=0
    for x in movies_ids_recommanded:
        if x in ratedmovies:
            n+=userRatings[userRatings['movie_id']==x]['rating'].values[0]/5
        elif explore:
            n+=1
    return n

class TestHelpersMethods(unittest.TestCase):

    def test_helpers(self):
        userLoc = "data/users.csv"
        dataLoc = "data/movies.csv"
        ratingsLoc = "data/ratings.csv"
        users,data,ratings = load_csv(userLoc,dataLoc,ratingsLoc)
        cols = ["title","Animation", "Children's",
       'Comedy', 'Adventure', 'Fantasy', 'Romance', 'Drama',
       'Action', 'Crime', 'Thriller', 'Horror', 'Sci-Fi', 'Documentary', 'War',
       'Musical', 'Mystery', 'Film-Noir', 'Western']
        newData = select_features(data,cols)
        similaritiesMatrix=similarities(newData, features)
        recommendations=get_recommendations(1176,movies,ratings,similaritiesMatrix)
        self.assertEqual(evaluation(recommendations,ratings,0),5)
        self.assertEqual(evaluation(recommendations,ratings,0,explore=False),0)


if __name__ == '__main__':
    unittest.main()
