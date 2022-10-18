import enum
import pandas as pd
import numpy as np
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


df1 = pd.read_csv('../data/tmdb_5000_credits.csv')
df2 = pd.read_csv('../data/tmdb_5000_movies.csv')



df1.columns = ['id','title','cast','crew']
df2 = df2.merge(df1[['id','cast','crew']],on='id')



C = df2['vote_average'].mean()
m = df2['vote_count'].quantile(0.9)
def weightedRating(x,m=m,C=C):
  v = x['vote_count']
  R = x['vote_average']
  return (v/(v+m)*R) + (m/(v+m)*C)

q_movies = df2.copy().loc[df2['vote_count']>=m]
q_movies['score'] = q_movies.apply(weightedRating,axis=1)
q_movies = q_movies.sort_values('score',ascending=False)


### 텍스트(컨텐츠) 분석하기
tfidf = TfidfVectorizer(stop_words='english')
df2['overview'] =df2['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(df2['overview'])


### 코사인 유사도 적용하기

cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)
indices = pd.Series(df2.index,index=df2['title']).drop_duplicates()


def get_recommendation(title,cosine_sim = cosine_sim):
  idx = indices[title]
  sim_scores = list(enumerate(cosine_sim[idx]))

  sim_scores = sorted(sim_scores,key=lambda x:x[1],reverse=True)
  sim_scores = sim_scores[1:11]

  movie_indicies = [i[0] for i in sim_scores]
  return df2['title'].iloc[movie_indicies]


if __name__ == '__main__':
    print(get_recommendation('Up'))



# 선호도를 찾을 방법,
# 1. 필터버블이라는게 개인의 선호도가 가중됨에 따라 편향적으로 나타나는 것!
# 2. 선호도가 가중된다 = 특정 사용자의 개인화된 데이터가 많아진다.
# 2. 결국 콘텐츠기반의 필터링에서 선호도 = 코사인 유사도
# 3. 코사인 유사도에 영향을 줄 리스트의 개수를 제한하기 + 다른 타입의 영화를 같이 추천하기(1~20%)
# 4. 그러면 3번에서의 리스트를 어떻게 유지시킬 것이냐
# 5. 
# 6. 