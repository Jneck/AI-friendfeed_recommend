import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

def Main_Friend(User):
    Following_df = pd.read_excel("Following.xlsx")
    Following_df['Score']=Following_df['View'] + (Following_df['Hunny']*2)
    Following_df2 = Following_df.sort_values(by=['UserName', 'Score'], ascending=[True, False])
    Main_friend_list = list(Following_df2[Following_df2['UserName'] == User]['Following'].values)
    return print(Main_friend_list)

def Friend_recommend(User):
    Following_df = pd.read_excel("Following.xlsx")
    Follower_df = pd.read_excel("Follower.xlsx")
    Following_df['Score'] = Following_df['View'] + (Following_df['Hunny'] * 2)
    title_user = Following_df.pivot_table('Score', index='UserName', columns='Following')
    title_user.fillna(0, inplace=True)
    user_based_collab = cosine_similarity(title_user, title_user)
    user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index, columns=title_user.index)
    Follower_list = list(Follower_df[Follower_df['UserName'] == 'Alice']['Follower'].values)
    Following_collab_list=list(user_based_collab[User].sort_values(ascending=False)[:7].index)

    recommand_list = []
    for i in Following_collab_list:
        if i not in Follower_list:
            recommand_list.append(i)
    recommand_list
    return print(recommand_list[1:])


Friend_recommend("Alice")


