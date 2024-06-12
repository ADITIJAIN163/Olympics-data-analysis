import numpy as np
def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby(by='region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    return medal_tally

def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country=np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country


def data_year_country_wise(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year=='Overall' and country=='Overall':
        tempdf= medal_df
    if year!='Overall' and country=='Overall':
        tempdf= medal_df[medal_df['Year']==int(year)]
    if year=='Overall' and country!='Overall':
        flag=1
        tempdf= medal_df[medal_df['region']==country]
    if year!='Overall' and country!='Overall':
        tempdf= medal_df[(medal_df['Year']==int(year)) & (medal_df['region']==country)]
    
    if flag==1:
        x=tempdf.groupby(by='Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=tempdf.groupby(by='region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()    
    x['Total']=x['Gold']+x['Silver']+x['Bronze']
    return(x)

def data_over_years(df,col):
    data_over_years=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index(name='index').sort_values('index')
    data_over_years=data_over_years.rename(columns={'index':col,'Year':'Edition'})
    return data_over_years



def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def country_yearwise(df,country):
   y=df[df['region']==country].drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
   y.dropna(subset='Medal',inplace=True)
   cc=y.groupby('Year').count()['Medal'].reset_index()
   return cc

def heatmap_countrywise_sport(df,country):
    y=df.dropna(subset=['Medal'])
    y.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_y=y[y['region']==country]
    pt=new_y.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x
def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final