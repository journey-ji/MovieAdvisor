import enum
import pandas as pd
import numpy as np
import sys
import json
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import linear_kernel

## 데이터 불러오기
df1 = pd.read_csv('../data/tmdb_5000_credits.csv')
df2 = pd.read_csv('../data/tmdb_5000_movies.csv')


## 데이터 병합
df1.columns = ['id','title','cast','crew']
df2 = df2.merge(df1[['id','cast','crew']],on='id')


## 평점 가중치 계산
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

df2['overview'] =df2['overview'].fillna('') ## null은 공백으로 바꿔주기
tfidf_matrix = tfidf.fit_transform(df2['overview'])
### 코사인 유사도 적용하기
cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)
indices = pd.Series(df2.index,index=df2['title']).drop_duplicates()


## movieList의 줄거리를 전부 연결하고, 그에 대한 유사도 구하기
temp = df2['overview'].copy()
movieList = [19995,285,206647,49026,49529,559,38757,99861,767,209112]
total_overview = ''
for x in movieList:
  total_overview += str(df2['overview'].loc[df2['id']==x])
temp[temp.size-1] = total_overview ## temp의 마지막에 total_overview 추가

total_matrix = tfidf.fit_transform(temp)
total_sim = linear_kernel(total_matrix[temp.size-1],total_matrix)
total_score = list(enumerate(total_sim[0]))
total_score = sorted(total_score,key=lambda x:x[1],reverse=True)
total_score = total_score[1:11]
movie_indicies = [i[0] for i in total_score]
print(df2[['id','title']].iloc[movie_indicies])


### 아래 문단은 하나의 데이터 줄로도 여러개 영화에 대입 가능하다는 의미
cosine_sim_ex = linear_kernel(tfidf_matrix[0],tfidf_matrix) ## 0번째 영화와 matrix에 대한 코사인 유사도 구하기
idx = indices['Avatar']
sim_score = list(enumerate(cosine_sim_ex[0]))
sim_score = sorted(sim_score,key=lambda x:x[1],reverse=True)
sim_score = sim_score[1:11]
movie_indicies = [i[0] for i in sim_score]
##print('This')
##print(df2[['id','title']].iloc[movie_indicies])
##print('That')
###

def get_recommendation(title,cosine_sim = cosine_sim):
  idx = indices[title]
  sim_scores = list(enumerate(cosine_sim[idx]))

  
  sim_scores = sorted(sim_scores,key=lambda x:x[1],reverse=True)
  sim_scores = sim_scores[1:11]
  
  movie_indicies = [i[0] for i in sim_scores]
  return df2[['id','title']].iloc[movie_indicies]


if __name__ == '__main__':
  print('hi')
# 선호도를 찾을 방법,
# 1. 필터버블이라는게 개인의 선호도가 가중됨에 따라 편향적으로 나타나는 것!
# 2. 선호도가 가중된다 = 특정 사용자의 개인화된 데이터가 많아진다.
# 2. 결국 콘텐츠기반의 필터링에서 선호도 = 코사인 유사도
# 3. 코사인 유사도에 영향을 줄 리스트의 개수를 제한하기 + 다른 타입의 영화를 같이 추천하기(1~20%)
# 4. 단순하게 밀어내기 