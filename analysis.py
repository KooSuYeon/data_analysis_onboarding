import pandas as pd

# 데이터 셋 상위 5개 데이터
# def get_sample_from_dataset(file):
#     csv_ = pd.read_csv(file)
#     return (csv_.head(5))

# print(get_sample_from_dataset("dataset.csv"))


csv_ = pd.read_csv("dataset.csv")
df = pd.DataFrame(csv_)

"""
1. 7월 3일~12월 31일까지, 인텔리픽의 취업코칭 서비스를 한 번 이상 활용한 인원은 몇명인가요?
-> 7월 3일부터 12월 31일까지의 인원 수 : 789명
"""
def get_silver_before_2024(dataframe):
    dataframe['createdat'] = pd.to_datetime(dataframe['createdat'], format='%y/%m/%d %H:%M', errors='coerce')
    filtered_df = dataframe[(dataframe['createdat'] >= '2023-07-03') & (dataframe['createdat'] <= '2023-12-31')]
    user_counts = filtered_df["userid"].nunique()

    return user_counts

# 답 : 789명
# print(get_silver_before_2024(df))

"""
2-1. 해당 데이터에서 최종합격한 인원은 몇명이고, 최종 합격 그룹의 이력서 진단 / 면접 코칭 신청 평균 횟수는 몇 회 인가요?
-> status가 "최종합격"인 모든 인원 : 241
"""
def get_final_pass(dataframe):

    filtered_df = dataframe.loc[dataframe["status"] == "최종합격"]
    user_counts = filtered_df["userid"].nunique()
    return user_counts

# 답 : 241명
# print(get_final_pass(df))


"""
2-2. 최종 합격 그룹의 이력서 진단 / 면접 코칭 신청 평균 횟수는 몇 회 인가요?
-> 최종합격 인원들의 평균 신청 횟수
"""
def get_average_among_final_pass(dataframe):
    final_pass_rows = dataframe.loc[dataframe["status"] == "최종합격"]
    
    # 중복된 id라도 다른 상태 (이력서 진단/면접 코칭 신청이라면 다르게 처리)
    user_counts = final_pass_rows["userid"].value_counts()
    average_count = user_counts.mean()
    
    return average_count

# 답 : 3.975103734439834
# print(get_average_among_final_pass(df))


"""
3. 이력서 진단 + 면접 코칭을 가장 많이 활용한 인원의 각 횟수는 몇번이며, 해당 인원의 id 값은 무엇인가요?
"""
def get_top_count_and_user_id_by_type(dataframe):
    type_user_counts = dataframe.groupby('type')['userid'].value_counts()
    
    # 각 'type'별로 가장 많이 이용한 사용자와 그 횟수 찾기
    top_users_by_type = type_user_counts.groupby('type').apply(lambda x: x.idxmax())
    top_counts_by_type = type_user_counts.groupby('type').max()

    top_users_by_type = top_users_by_type.apply(lambda x: x[1])
    result = pd.DataFrame({
        'Top User ID': top_users_by_type,
        'Top Count': top_counts_by_type
    }).reset_index()

    return result

# 답
"""
        type     Top User ID  Top Count
0  interview  223856945edb24          7
1     resume  142c51345184f1         11
"""
# print(get_top_count_and_user_id_by_type(df))



"""
4-1. 첫 취업코칭 신청 이후, 다음 코칭을 받기 까지의 평균 어느정도의 기간이 걸렸나요?
-> 첫 취업코칭 신청 이후, 다음 코칭을 받기 까지의 평균 7 일 11 시간 22 분 18 초가 소요됩니다.
"""
def get_average_first_interval(dataframe):
    # 'createdat' 컬럼을 datetime 타입으로 변환
    dataframe['createdat'] = pd.to_datetime(dataframe['createdat'], format='%y/%m/%d %H:%M', errors='coerce')
    
    # 'userid'별로 데이터를 그룹화하여 'createdat'을 기준으로 정렬
    user_groups = dataframe.groupby('userid')['createdat'].apply(lambda x: x.sort_values().reset_index(drop=True))
    # 단일 createdAt은 제외
    user_groups = user_groups.groupby('userid').filter(lambda group: len(group) > 1)
    # 첫번째 TimeStamp와 두번째 TimeStamp만 다루도록
    user_groups = user_groups[user_groups.index.get_level_values(1) < 2]

    # 각 유저의 첫 번째와 두 번째 'createdat' 간의 차이 계산
    intervals = []
    for user_id, group in user_groups.groupby('userid'):

        first_time = group.iloc[0]  # 첫 번째 'createdat' 값
        second_time = group.iloc[1]  # 두 번째 'createdat' 값

        print(first_time, second_time)
        interval = (second_time - first_time).total_seconds()  # 초 단위로 계산
        intervals.append(interval)
        
    
    # 평균 계산 (초 단위)
    if intervals:
        average_interval_seconds = sum(intervals) / len(intervals)
        
        # 초를 일, 시간, 분, 초로 변환
        days = average_interval_seconds // (24 * 3600)
        hours = (average_interval_seconds % (24 * 3600)) // 3600
        minutes = (average_interval_seconds % 3600) // 60
        seconds = average_interval_seconds % 60

        return f"첫 취업코칭 신청 이후, 다음 코칭을 받기 까지의 평균 {int(days)} 일 {int(hours)} 시간 {int(minutes)} 분 {int(seconds)} 초가 소요됩니다."
    else:
        return "첫 취업코칭만 진행된 상태입니다."  # 두 개 이상의 'createdat' 값이 없는 경우
    
# 답 : 첫 취업코칭 신청 이후, 다음 코칭을 받기 까지의 평균 7 일 11 시간 22 분 18 초가 소요됩니다.
# print(get_average_first_interval(df))

"""
4-2. 어떤 방식으로 평균 기간을 도출했나요?

1. 
createdat 컬럼을 datetime으로 변환: dataframe['createdat'] = pd.to_datetime(dataframe['createdat'], format='%y/%m/%d %H:%M', errors='coerce')을 사용하여 
createdat이 문자열 형태일 경우 이를 datetime 형식으로 변환합니다. 이 과정에서 변환 불가능한 값은 NaT로 처리됩니다.

2. 
userid별로 데이터를 그룹화: groupby('userid')를 사용하여 각 사용자별로 createdat을 기준으로 데이터를 그룹화하고, 
.sort_values()로 각 사용자별로 createdat 날짜 순으로 데이터를 정렬합니다. 그런 후 reset_index(drop=True)를 사용하여 인덱스를 재설정합니다.

3. 
단일 createdat 값은 제외: filter(lambda group: len(group) > 1)을 통해 각 사용자에게 두 개 이상의 createdat 값이 있을 경우만 필터링합니다.

4.
createdat의 첫 번째와 두 번째 차이를 구하기: 각 사용자별로 첫 번째와 두 번째 createdat의 차이를 계산하고, 이를 초 단위로 intervals 리스트에 추가합니다. 
(second_time - first_time).total_seconds()를 사용하여 두 시간의 차이를 초 단위로 구합니다.

5. 
평균 기간 계산: 초 단위로 구한 intervals의 평균을 구합니다. 이를 통해 모든 사용자에 대한 첫 번째와 두 번째 createdat 간의 평균 차이를 계산합니다.

6.
결과 형식 변환: 평균 초 값을 일, 시간, 분, 초로 변환합니다. 예를 들어 60초는 1분으로, 3600초는 1시간으로 변환하여 최종적으로 
f"첫 취업코칭 신청 이후, 다음 코칭을 받기 까지의 평균 {int(days)} 일 {int(hours)} 시간 {int(minutes)} 분 {int(seconds)} 초가 소요됩니다." 형식으로 반환합니다.
"""

"""
4-3. 위의 답변에 대한 근거

1. 
user_groups 데이터프레임: user_groups는 각 사용자별로 createdat 값이 정렬된 데이터입니다. 
각 사용자의 createdat 값들이 두 개 이상 있는 경우에만 그들 간의 차이를 계산하고, 그 값을 초 단위로 계산하여 intervals 리스트에 저장됩니다.

2. 
두 번째와 첫 번째 createdat 차이 계산: 각 사용자에 대해 첫 번째와 두 번째 createdat 간의 차이를 계산하여 intervals 리스트에 초 단위로 추가합니다.
예를 들어, 2023-09-22 13:42:00과 2023-09-26 01:12:00 사이의 차이는 초 단위로 계산됩니다

3.
초를 일/시간/분/초로 변환: 평균 초 값을 구한 후 이를 일, 시간, 분, 초 단위로 변환합니다. 이 변환은 다음 공식을 기반으로 합니다:

1일 = 24 * 3600초
1시간 = 3600초
1분 = 60초
예를 들어, intervals 값이 61200초라면:

61200초는 0일 17시간 0분 0초로 변환됩니다.
위의 평균 초 값을 일/시간/분/초로 변환한 결과는 7일 11시간 22분 18초입니다.

데이터 비교:
코드에서는 여러 userid별로 여러 createdat을 비교하며, 각 userid의 첫 번째와 두 번째 createdat 값 간의 차이를 초 단위로 구하고, 이를 평균화한 후, 결과를 일/시간/분/초로 변환하여 출력합니다.

따라서, "첫 취업코칭 신청 이후, 다음 코칭을 받기 까지의 평균 7 일 11 시간 22 분 18 초가 소요됩니다."라는 답은 여러 사용자의 createdat 값들 간의 차이(첫 번째와 두 번째)들을 평균화하여 구한 값입니다

"""


"""
5-1. 인텔리픽 서비스 이용자 중, course별 최종 합격인원은 각각 몇 명, 몇 퍼센트인가요? 그들은 다른 이용자들과 어떤 차이점을 보이고 있나요?  
"""
def get_final_pass_groupby_course(dataframe):

    filtered_df = dataframe.loc[dataframe["status"] == "최종합격"]

    user_counts = filtered_df["userid"].nunique()
    course_counts = filtered_df.groupby('course')['userid'].nunique()  
    course_percentages = (course_counts / user_counts) * 100  
    
    result = pd.DataFrame({
        'Final Pass Count': course_counts,
        '%': course_percentages
    }).reset_index()
    
    return result

# 답
"""
    course  Final Pass Count          %
0  Hanghae               106  43.983402
1   NBCamp               135  56.016598
"""
# print(get_final_pass_groupby_course(df))


"""
5-2. 그들은 다른 이용자들과 어떤 차이점을 보이고 있나요? 

최종 합격된 사용자의 마지막 서비스 사용일자로 합격 시기를 비교해보았습니다.

평균 합격일자

NBCamp의 평균 createdat이 Hanghae보다 약 5일 정도 늦습니다. 이는 NBCamp에서 최종 합격한 사용자들이 대체로 늦은 시점에 합격한 경향이 있음을 시사합니다. 
반면 Hanghae는 약간 더 이른 시점에 최종 합격한 사용자들이 존재함을 알 수 있습니다.

첫 합격일자

두 그룹 모두 첫 합격일자가 동일한 날짜인 2023-07-04로 나타나지만, NBCamp의 첫 합격일자는 Hanghae보다 11시간 1분 뒤에 기록되었습니다. 
이는 두 그룹이 같은 날 시작되었지만, NBCamp에서 첫 합격자가 조금 더 늦게 발생했음을 나타냅니다.

마지막 합격일자
NBCamp는 마지막 합격일자가 Hanghae보다 7일 더 늦은 2023-12-29입니다.
이로 인해 NBCamp에서는 최종 합격자들이 비교적 늦은 시점에 최종 합격을 받았음을 알 수 있습니다. 반면 Hanghae는 더 빨리 최종 합격자가 기록되었습니다.

결론적으로, NBCamp의 최종 합격자들이 후반기에 집중된 반면, Hanghae의 최종 합격자들은 초반에 집중된 것으로 보입니다. NBCamp는 그만큼 더 긴 시간이 소요된 것으로 해석할 수 있습니다.
또한 이는 캠프별 같은 일자에 시작하여 같은 주기로 관리되었다는 가정이므로 구체적인 주기에 따라 해당 해석은 달라질 수 있습니다.

(예를 들어 NBCamp가 더 긴 기간 동안 진행되었을 수 있습니다. 
그런 경우, NBCamp에서 후반에 합격자가 몰린 것이 캠프의 진행 기간이나 속도에 따른 결과일 수 있습니다.)

"""
def get_diff_between_hanghae_and_nbc(dataframe):
    # 'createdat'을 datetime 형식으로 변환
    dataframe['createdat'] = pd.to_datetime(dataframe['createdat'], format='%y/%m/%d %H:%M', errors='coerce')

    # 'status'가 '최종합격'인 데이터 필터링
    filtered_df = dataframe.loc[dataframe["status"] == "최종합격"]
    final_users = filtered_df["userid"].drop_duplicates()
    final_df = filtered_df[filtered_df["userid"].isin(final_users)]
    
    # 'course'별로 그룹화하여 평균, 최소값, 최대값 계산
    course_avg_createdat = final_df.groupby('course')['createdat'].mean()
    course_min_createdat = final_df.groupby('course')['createdat'].min()
    course_max_createdat = final_df.groupby('course')['createdat'].max()

    result = pd.DataFrame({
        'avg_createdat': course_avg_createdat,
        'min_createdat': course_min_createdat,
        'max_createdat': course_max_createdat
    })
    
    return result


# 답
"""
                        avg_createdat       min_createdat       max_createdat
course                                                                       
Hanghae 2023-09-24 21:18:48.641425408 2023-07-04 00:46:00 2023-12-22 15:55:00
NBCamp  2023-09-29 03:30:14.381139456 2023-07-04 11:47:00 2023-12-29 00:57:00
"""
# print(get_diff_between_hanghae_and_nbc(df))



"""
(5-1) 위의 답변에 대한 근거는 무엇인가요? 어떤 데이터를 비교하셨나요?

status가 '최종합격'인 데이터를 필터링하여 최종 합격자들만 추출했습니다.
user_counts: 최종 합격한 고유 사용자 수를 구했습니다. 이를 위해 drop_duplicates()를 사용하여 중복된 사용자 ID를 제거하고 count()로 고유 사용자 수를 셌습니다.
course_counts: 각 **course**별로 최종 합격자의 고유 사용자 수를 구했습니다. 이를 위해 groupby('course')['userid'].nunique()를 사용하여 각 캠프(course)별로 중복되지 않는 사용자 수를 계산했습니다.
course_percentages: 각 **course**별 최종 합격자 수를 전체 최종 합격자 수로 나누어 퍼센트를 계산했습니다. (course_counts / user_counts) * 100을 사용하여 비율을 구했습니다.
마지막으로, course_counts와 course_percentage를 DataFrame 형태로 반환했습니다.

Final Pass Count: 각 캠프(course)별 최종 합격자 수를 계산한 값으로, 각 캠프에서 몇 명이 최종 합격했는지를 나타냅니다. 이는 캠프별로 합격자가 얼마나 분포되어 있는지를 보여주는 지표입니다.

% (퍼센트): 각 캠프에서 최종 합격자 비율을 계산한 값입니다. 전체 최종 합격자 중 각 캠프에서 최종 합격한 인원이 차지하는 비율을 보여줍니다. 이는 각 캠프가 최종 합격자들 사이에서 얼마나 중요한 비중을 차지하는지를 나타냅니다.


(5-2) 위의 답변에 대한 근거는 무엇인가요? 어떤 데이터를 비교하셨나요?

createdat 컬럼을 datetime 형식으로 변환하여 날짜/시간 데이터를 처리할 수 있도록 했습니다.
이후, status가 '최종합격'인 데이터만 필터링하여, 최종 합격자들을 추출했습니다.
course별로 데이터를 그룹화한 후, 각 그룹별로 createdat의 평균(평균 취업코칭 진행 시간), 최소값(가장 빠른 최종 합격 시간), 최대값(가장 늦은 최종 합격 시간)을 계산했습니다.
각 결과를 **pd.DataFrame**으로 구성하여 반환했습니다.
"""

"""
6-1.
인텔리픽 서비스를 통해 최종 합격률을 높이기 위해, 어떤 액션을 시도할 수 있을까요?

사용자가 자신 있는 분야(type)에 맞는 과정(course)을 선택하도록 유도하는 접근 제시!

1. 최종 합격률에 대한 데이터 분석을 통한 인사이트 제공
데이터에서 각 과정(course)별로 최종 합격자 비율(Final Pass Count, %)을 분석해 보면, 각 과정의 합격률에 차이가 있음을 확인할 수 있습니다. 

예를 들어, 특정 과정에서 합격률이 상대적으로 낮다면, 해당 과정에 적합한 사용자는 어떤 유형(type)의 학습자가 될 수 있는지에 대한 데이터를 비교할 수 있습니다.
예시로, interview 유형의 사용자가 NBCamp에서 높은 합격률을 보이고, resume 유형의 사용자가 Hanghae에서 높은 합격률을 보인다면, 해당 정보를 바탕으로 각 유형에 맞는 과정을 추천할 수 있습니다.

2. 자신 있는 분야에 맞는 과정 선택 유도
자신 있는 분야(type)를 선택한 사용자가 해당 과정(course)에서 더 높은 합격률을 기록한다는 분석 결과는, 사용자가 더 잘 알고, 더 편안하게 학습할 수 있는 과정을 선택하도록 유도하는 데 중요한 근거가 됩니다. 
예를 들어:
resume 유형의 사용자는 Hanghae에서 높은 합격률을 보였기 때문에, 해당 유형의 사용자가 Hanghae 과정을 선택하도록 유도하면 더 높은 합격 가능성을 제공할 수 있습니다.
반대로, interview 유형의 사용자는 NBCamp에서 더 높은 합격률을 보였다면, 이 사용자에게는 NBCamp 과정을 추천함으로써 더 높은 합격률을 기대할 수 있습니다.

사용자들에게 자신 있는 type에 맞는 course를 선택하도록 유도하는 것은 개인화된 학습 경험을 제공하며, 그 결과 최종 합격률을 높이는 데 중요한 역할을 할 수 있습니다. 
각 type과 course별 합격률 데이터를 분석하고, 사용자가 자신의 특성에 맞는 과정을 선택할 수 있도록 지원하는 것은 인텔리픽 서비스의 효율성을 극대화하는 전략이 될 것입니다.
"""
def get_pass_probability_by_type_and_course(dataframe):
    # 최종 합격한 데이터 필터링
    final_pass_df = dataframe.loc[dataframe["status"] == "최종합격"]

    # 전체 사용자 수 (각 type별)
    total_users_by_type = dataframe.groupby("type")["userid"].nunique()

    # 각 type별 course에서 최종 합격한 user 수
    pass_counts = final_pass_df.groupby(["type", "course"])["userid"].nunique()

    # 확률 계산
    pass_probabilities = (pass_counts / total_users_by_type) * 100

    # DataFrame 변환
    result = pass_probabilities.reset_index().rename(columns={"userid": "Pass Probability (%)"})
    
    return result

# print(get_pass_probability_by_type_and_course(df))

def get_suitable_course_depends_on_type(dataframe, user_type):
    # 최종 합격한 데이터만 필터링
    filtered_df = dataframe.loc[(dataframe["status"] == "최종합격") & (dataframe["type"] == user_type)]
    
    # 각 과정별(user_type) 합격한 user 수
    course_counts = filtered_df.groupby('course')['userid'].nunique()
    total_users = filtered_df['userid'].nunique()
    
    # 합격률 계산
    course_percentages = (course_counts / total_users) * 100
    
    # 결과 DataFrame 생성
    result = pd.DataFrame({
        'Final Pass Count': course_counts,
        '%': course_percentages
    }).reset_index()
    
    # 합격률이 가장 높은 course 선택
    best_course = result.loc[result['%'].idxmax(), 'course'] if not result.empty else None
    
    return best_course

# print(get_suitable_course_depends_on_type(df, "resume"))

