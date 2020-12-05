import unittest

from src.operations import *
from src.load_data import *

def get_movie_id(df, title:str, year=None):
    res = df[df['title'] == title]
    if year:
        res = res[res['year'] == year]

    if len(res) > 1:
        print("Ambiguous: found")
        print(f"{res['title']} {res['year']}")
    elif len(res) == 0:
        print('not found')
    else:
        return res.index[0]

def get_movie_name(df, index):
    return df.iloc[index].title

def get_movie_year(df, index):
    return df.iloc[index].year

class TestHelpersMethods(unittest.TestCase):

    def test_helpers(self):
        userLoc = "data/users.csv"
        dataLoc = "data/movies.csv"
        ratingsLoc = "data/ratings.csv"
        users,data,ratings = load_csv(userLoc,dataLoc,ratingsLoc)
        n1 = get_movie_id(data,'King Kong')
        n2 = get_movie_id(data, 'King Kong', year=1933)
        n3= get_movie_id(data, 'Sherlock Holmes 3')
        self.assertEqual(n1,None)
        self.assertEqual(n2,2297)
        self.assertEqual(n3,None)
        name = get_movie_name(data,n2)
        year = get_movie_year(data,n2)
        self.assertEqual(name,'King Kong')
        self.assertEqual(year, 1993)

if __name__ == '__main__':
    unittest.main()
