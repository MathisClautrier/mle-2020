import unittest
import pandas as pd


def load_csv(userLoc:str,dataLoc:str,ratingsLoc:str):
    users=pd.read_csv(userLoc)
    data=pd.read_csv(dataLoc)
    ratings=pd.read_csv(ratingsLoc)
    return users,data,ratings

def select_features(df:pd.core.frame.DataFrame,columns:list,ID='ID'):
    """ It is assumed that the given columns name begin by the expected ID"""
    newdf=df[columns]
    id = newdf.columns[0]
    if 'ID' != id:
        newdf=newdf.rename(columns={id:ID})
    return newdf

def similarUsers(user_id,users,delta=5):
    userAge=users[users['user_id']==user_id]['age'].values[0]
    newUsers=users[users['age']>userAge-5]
    newUsers=newUsers[newUsers['age']<userAge+5]
    return newUsers['user_id'].values

def newFeature(ratings,users,data,simUsers,id='movie_id'):
    similarUsers=users.iloc[simUsers]
    ratingsSimilar=pd.merge(similarUsers,ratings,how='inner',on='user_id')
    n=data.shape[0]
    newFeature=[0 for i in range(n)]
    for i in range(n):
        newFeature[i]=ratingsSimilar[ratingsSimilar[id]==i]['rating'].mean()/5
    return newFeature


class TestLoadMethods(unittest.TestCase):

    def test_loader(self):
        userLoc = "data/users.csv"
        dataLoc = "data/movies.csv"
        ratingsLoc = "data/ratings.csv"
        users,data,ratings = load_csv(userLoc,dataLoc,ratingsLoc)
        self.assertEqual(type(users),pd.core.frame.DataFrame )
        self.assertEqual(type(data),pd.core.frame.DataFrame )
        self.assertEqual(type(ratings),pd.core.frame.DataFrame )

    def test_select_features(self):
        userLoc = "data/users.csv"
        dataLoc = "data/movies.csv"
        ratingsLoc = "data/ratings.csv"
        users,data,ratings = load_csv(userLoc,dataLoc,ratingsLoc)
        cols = ["title","Animation", "Children's",
       'Comedy', 'Adventure', 'Fantasy', 'Romance', 'Drama',
       'Action', 'Crime', 'Thriller', 'Horror', 'Sci-Fi', 'Documentary', 'War',
       'Musical', 'Mystery', 'Film-Noir', 'Western']
        newData = select_features(data,cols)
        newColumns = newData.columns
        self.assertEqual(newColumns[0],'ID')
        self.assertEqual(data.shape[0],newData.shape[0])
        for i in range(1,19):
            self.assertEqual(newColumns[i],cols[i])

if __name__ == '__main__':
    unittest.main()
