import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('medical_examination.csv')


df1 = df['weight'] / ((df['height'] /100) ** 2)
df['overweight'] = (df1>25).astype(int)


df.loc[df['cholesterol'] == 1,'cholesterol'] = 0
df.loc[df['cholesterol'] > 1,'cholesterol'] = 1
df.loc[df['gluc'] == 1,'gluc'] = 0
df.loc[df['gluc'] > 1,'gluc'] = 1


def draw_cat_plot():
    
    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"]
    )
    
    
    df_cat = df_cat.groupby(["cardio", "variable", "value"], as_index=False).size()
    

    
    df_cat.rename(columns={"size": "total"}, inplace=True)


   
    fig = sns.catplot(
        x="variable",
        y="total",
        hue="value",
        col="cardio",
        data=df_cat,
        kind="bar",
        height=5,
        aspect=1.2
    ).fig

    
    fig.savefig('catplot.png')
    return fig



def draw_heat_map():
    
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975)) ]

    corr = df_heat.corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig = plt.figure(figsize=(10, 8))

    sns.heatmap(corr, annot=True, fmt=".1f", cmap='coolwarm', mask=mask, cbar_kws={'shrink': 0.8})
    
    fig.savefig('heatmap.png')
    return fig
