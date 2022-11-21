import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import json
# 자기 주변 6명의 친구들 불러오는 함수
def Main_Friend(User):
    Following_df = pd.read_excel("friend_recommend/Following.xlsx")
    Following_df['Score']=Following_df['View'] + (Following_df['Hunny']*2)
    Following_df2 = Following_df.sort_values(by=['UserName', 'Score'], ascending=[True, False])
    Main_friend_list = list(Following_df2[Following_df2['UserName'] == User]['Following'].values)
    return Main_friend_list

# 친구 추천 목록에서 친구를 추천해주는 함수
def Friend_recommend(User):
    Following_df = pd.read_excel("friend_recommend/Following.xlsx")
    Follower_df = pd.read_excel("friend_recommend/Follower.xlsx")
    Following_df['Score'] = Following_df['View'] + (Following_df['Hunny'] * 2)
    title_user = Following_df.pivot_table('Score', index='UserName', columns='Following')

    title_user.fillna(0, inplace=True)
    user_based_collab = cosine_similarity(title_user, title_user)
    user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index, columns=title_user.index)
    Follower_list = list(Follower_df[Follower_df['UserName'] == User]['Follower'].values)
    Following_collab_list=list(user_based_collab[User].sort_values(ascending=False)[:7].index)

    recommand_list = []
    for i in Following_collab_list:
        if i not in Follower_list:
            recommand_list.append(i)
    recommand_list
    return recommand_list[1:]


def Friend_recommend2(User_DB):
    Friend_df = pd.DataFrame(User_DB)
    Friend_df = Friend_df.astype('str')
    # Friend_df.transpose()
    Guest_list = Friend_df['Guest']
    Guest_unique = Guest_list.unique()
    Friend_df['Score'] = Friend_df['lifing_count'] + (Friend_df['roomIn_count'] * 4) + (
                Friend_df['guestbook_count'] * 5) + Friend_df['chatting']
    Score_df = Friend_df.pivot_table('Score', index='Guest', columns='User_id')
    Score_df.fillna(0, inplace=True)

    # 유저와 유저 간의 유사도
    user_based_collab = cosine_similarity(Score_df, Score_df)
    user_based_collab = pd.DataFrame(user_based_collab, index=Score_df.index, columns=Score_df.index)
    friend_dict = {}

    for i in sorted(Guest_unique):
        Following_collab_list = list(user_based_collab[i].sort_values(ascending=False).index)
        friend_dict[i] = Following_collab_list[1:]


    return friend_dict
