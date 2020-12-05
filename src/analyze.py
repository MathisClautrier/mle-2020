import unittest

from src.helpers import *
from src.operations import *
from src.load_data import *

def get_most_similar(similarity, items, name, year=None, top=10, get_id= get_movie_id, get_name= get_movie_name):
    """ Take as imput similarity a matrix which represents how two items are similar
                      items the dataframe equivalent to movies
                      name a src which is the name of the item (movie)
                      year an int(optionnal) representing the associated year
                      top an int (optionnal) representing the number selected items
                      get_id a function equivalent to get_movie_id
                      get_name a funciton equivalent to get_movie_name

        The purpose of this function is select the most similar items

        return an array of most similar items
    """"
    index_items = get_id(items, name, year)
    best = similarity[index_items].argsort()[::-1]
    return [(ind, get_name(items, ind), similarity[index_items, ind]) for ind in best[:top] if ind != index_items]

def get_recommendations(user_id, items, ratings, similarity, user_id_col='user_id', sort_col='rating', get_year = get_movie_year,
                        name_col = 'title', ID = 'movie_id', get_id = get_movie_id, get_name= get_movie_name):

    top_items = ratings[ratings[user_id_col] == user_id].sort_values(by= sort_col, ascending=False).head(3)[ID]
    index=[ID, name_col, 'similarity']

    most_similars = []
    for top_item in top_items:
        most_similars += get_most_similar(similarity, items, get_name(items,top_item),year = get_year(items, top_item),
                            get_id=get_id, get_name=get_name)

    return pd.DataFrame(most_similars, columns=index).drop_duplicates().sort_values(by='similarity', ascending=False).head(5)

class TestOperationsMethods(unittest.TestCase):

    def test_operations(self):
         userLoc = "data/users.csv"
         dataLoc = "data/movies.csv"
         ratingsLoc = "data/ratings.csv"
         users,data,ratings = load_csv(userLoc,dataLoc,ratingsLoc)
         features = ["Animation", "Children's",
        'Comedy', 'Adventure', 'Fantasy', 'Romance', 'Drama',
        'Action', 'Crime', 'Thriller', 'Horror', 'Sci-Fi', 'Documentary', 'War',
        'Musical', 'Mystery', 'Film-Noir', 'Western']
         cols = ['title']+features
         newData = select_features(data,cols)
         similaritiesMatrix=similarities(newData, features)
         mostSimilar=get_most_similar(similaritiesMatrix,movies,'Toy Story')
         self.assertEqual(mostSimilar[0][0],667)
         self.assertEqual(mostSimilar[0][1],'Space Jam')
         self.assertEqual(mostSimilar[0][2],3.0)
         self.assertEqual(len(mostSimilar),9)
         df=get_recommendations(999, data, ratings, similaritiesMatrix)
         self.assertEqual(df.shape[0],5)
         self.assertEqual(df.shape[0],3)

if __name__ == '__main__':
    unittest.main()
