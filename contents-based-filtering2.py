import pandas as pd
import sys
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






### 아래 문단은 하나의 데이터 줄로도 여러개 영화에 대입 가능하다는 의미
cosine_sim_ex = linear_kernel(tfidf_matrix[0],tfidf_matrix) ## 0번째 영화와 matrix에 대한 코사인 유사도 구하기
idx = indices['Avatar']
sim_score = list(enumerate(cosine_sim_ex[0]))
sim_score = sorted(sim_score,key=lambda x:x[1],reverse=True)
sim_score = sim_score[1:11]
movie_indicies = [i[0] for i in sim_score]




### 평점 가중치 구하기
C = df2['vote_average'].mean()
m = df2['vote_count'].quantile(0.7) ## 상위 10%에 해당하는 평가수를 가진 영화만 검색
q_movies = df2.copy().loc[df2['vote_count']>=m] # 상위 10% 영화만 담은 리스트 생성

def weighted_rating(x,m=m,C=C):
  v = x['vote_count']
  R = x['vote_average']
  return (v/(v+m)*R) + (m/(v+m)*C)

## 평점가중치가 적용된 영화리스트 ! (상위 10% 이상의 추천수를 받은 영화만 가지고 있음)
q_movies['score'] = q_movies.apply(weighted_rating,axis=1)

def get_recommendation2(movieList,cosine_sim=cosine_sim):
  ## 입력된 문자열을 리스트로 변환
  if(type(movieList)==str):
    movieList = movieList.split(',')
  movieList = list(map(int, movieList))

  ## 추천리스트의 모든 영화에 대한 줄거리를 하나의 문자열로 만들기
  temp = df2['overview'].copy()
  temp2 = q_movies['overview'].copy()
   
  total_overview = ''
  total_overview2 = ''
  for x in movieList:
    total_overview += str(df2['overview'].loc[df2['id']==x])
    total_overview2 += str(q_movies['overview'].loc[q_movies['id']==x])
  temp[temp.size-1] = total_overview ## temp의 마지막에 total_overview 추가
  temp2[temp2.size-1] = total_overview2

  # 영화 줄거리에 대한 벡터값 구하기
  total_matrix = tfidf.fit_transform(temp)
  total_matrix2 = tfidf.fit_transform(temp2)
  # 벡터값에 대한 코사인 유사도 구하고 내림차순 정렬
  total_sim = linear_kernel(total_matrix[temp.size-1],total_matrix)
  total_sim2 = linear_kernel(total_matrix2[temp2.size-1],total_matrix2)

  total_score = list(enumerate(total_sim[0]))
  total_score2 = list(enumerate(total_sim2[0]))
  total_score = sorted(total_score,key=lambda x:x[1],reverse=True)
  total_score2 = sorted(total_score2,key=lambda x:x[1],reverse=True)
  total_score = total_score[1:9]+total_score[-3:-1]
  total_score2 = total_score2[1:9]+total_score2[-3:-1]
  
  movie_indicies = [i[0] for i in total_score]
  movie_indicies2 = [i[0] for i in total_score2]
  
  print(q_movies[['id','title']].iloc[movie_indicies2])
if __name__ == '__main__':

  get_recommendation2(sys.argv[1])

# 선호도를 찾을 방법,
# 1. 필터버블이라는게 개인의 선호도가 가중됨에 따라 편향적으로 나타나는 것!
# 2. 선호도가 가중된다 = 특정 사용자의 개인화된 데이터가 많아진다.
# 2. 결국 콘텐츠기반의 필터링에서 선호도 = 코사인 유사도
# 3. 코사인 유사도에 영향을 줄 리스트의 개수를 제한하기 + 다른 타입의 영화를 같이 추천하기(1~20%)
# 4. 단순하게 밀어내기 




# !!!!!!!!!!!!!!!!! sys.agrv[1]이 문자열로 입력된다 -> 리스트로 바꿔줘야함 10/26일 바꿔주기 완료

## 10월 31일 유사도 하위 2개의 영화를 리스트에 넣기 
## 11월 1일 평점가중치 적용한 리스트 생성

## 할 일 1. 안쓰는 코드들 정리하고 주석처리


