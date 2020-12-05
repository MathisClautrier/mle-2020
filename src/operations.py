import unittest
import pandas
import numpy

from src.load_data import *

def vectorize(df,features:list,frame:str):
    return df.loc[df.ID==frame][features].iloc[0]

def similarity(df,features:list,frame1:str,frame2:str):
    vec1=vectorize(df,features,frame1)
    vec2=vectorize(df,features,frame2)
    return (vec1*vec2).sum()

def similarities(df, features:list):
    return df[features].values.dot(df[features].values.T)

def top_similar_items(similarityMatrix,df, index, top=10):
    similarityWithIndex=similarityMatrix[index]
    for i in range(10):
        print(f"Similarity between {df.iloc[index]['ID']} and {df.iloc[i]['ID']} (index {i}) is {similarityWithIndex[i]}")

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
         vec = vectorize(newData, features, 'Toy Story')
         self.assertEqual(type(vec),pandas.core.series.Series)
         self.assertEqual(vec.sum(),3.0)
         sim = similarity(newData, features, 'Toy Story', 'Pocahontas')
         self.assertEqual(sim, 2.0)
         sims = similarities(newData, features)
         self.assertEqual(type(sims),numpy.ndarray)
         self.assertEqual(sims.shape[0],3883)
         self.assertEqual(sims.shape[1],3883)

if __name__ == '__main__':
    unittest.main()
