import pandas as pd
import sys
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import linear_kernel

## 데이터 불러오기
df2 = pd.read_csv('../data/tmdb_5000_movies.csv')


### 텍스트(컨텐츠) 분석하기
tfidf = TfidfVectorizer(stop_words='english')

df2['overview'] =df2['overview'].fillna('') ## null은 공백으로 바꿔주기
tfidf_matrix = tfidf.fit_transform(df2['overview'])
### 코사인 유사도 적용하기
cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)
indices = pd.Series(df2.index,index=df2['title']).drop_duplicates()


## 평점 가중치 계산



# ### 평점 가중치 구하기
# C = df2['vote_average'].mean()
# m = df2['vote_count'].quantile(0.7) ## 상위 10%에 해당하는 평가수를 가진 영화만 검색
# q_movies = df2.copy().loc[df2['vote_count']>=m] # 상위 10% 영화만 담은 리스트 생성

# def weighted_rating(x,m=m,C=C):
#   v = x['vote_count']
#   R = x['vote_average']
#   return (v/(v+m)*R) + (m/(v+m)*C)

# ## 평점가중치가 적용된 영화리스트 ! (상위 10% 이상의 추천수를 받은 영화만 가지고 있음)
# q_movies['score'] = q_movies.apply(weighted_rating,axis=1)


## 날씨 데이터셋
sun = 'sun sulight daylight glare shine sunburst'


def get_recommendation2(weather,cosine_sim=cosine_sim):
  ## 입력된 문자열을 리스트로 변환

  ## 추천리스트의 모든 영화에 대한 줄거리를 하나의 문자열로 만들기
  temp = df2['overview'].copy()

  if weather in ['Rain','Mist','Haze']:
     total_overview = 'rain rainfall storm downpour wet rainstorm thunderstorm procipitation weather deluge shower cloudburst downfall thundershower drizzle mist spit sprinkle mizzle scud'
  elif weather in ['Snow','blizzard']:
    total_overview = 'snow blizzard snowfall powder snowflake'
  else:
    total_overview = 'sun sulight daylight glare shine sunburst'
  
  ## 날씨 관련 단어셋
  # 기준 : 맑고 시원한 산들바람이 붐, 핵더움, 비옴, 눈옴 
  ## 아래 페이지 참조
  ## https://www.teachstarter.com/us/teaching-resource/weather-word-wall-vocabulary-us/ 
  ##
  
  temp[temp.size-1] = total_overview ## temp의 마지막에 total_overview 추가

  # 영화 줄거리에 대한 벡터값 구하기
  total_matrix = tfidf.fit_transform(temp)
  # 벡터값에 대한 코사인 유사도 구하고 내림차순 정렬
  total_sim = linear_kernel(total_matrix[temp.size-1],total_matrix)

  total_score = list(enumerate(total_sim[0]))
  total_score = sorted(total_score,key=lambda x:x[1],reverse=True)
  total_score = total_score[1:13]
  
  movie_indicies = [i[0] for i in total_score]
  print(df2[['id','title']].iloc[movie_indicies])
if __name__ == '__main__':
  
  get_recommendation2(sys.argv[1])

## 날씨에 따른 영화추천해주기 구현