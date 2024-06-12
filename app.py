import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
df=pd.read_csv("athlete_events.csv")
region_df=pd.read_csv("noc_regions.csv")

df=preprocessor.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://i.pinimg.com/564x/20/57/36/20573645235c519e42a9b4a5672c0575.jpg')

user_menu=st.sidebar.radio(
    'Select an option',("Medal Tally", "Overall-analysis","Country wise analysis","Athelete wise analysis")
             
)
if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    medal_tally=helper.data_year_country_wise(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Overall Tally")
    if selected_year!='Overall' and selected_country=='Overall':
        st.title(f"{selected_year} Tally")
    if selected_year!='Overall' and selected_country!='Overall':
        st.title(f"{selected_year} \t {selected_country}\tTally")
    if selected_year=='Overall' and selected_country!='Overall':
        st.title(f"{selected_country} Tally")
    st.table(medal_tally)

if user_menu=='Overall-analysis':

    
   
    st.title("Top Statistics")
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    atheletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)    
    with col3:
        st.header("Atheletes")
        st.title(atheletes)
    

    
    st.header("Participating nations over the years")
    nations_over_years=helper.data_over_years(df,'region')
    fig=px.line(nations_over_years,x="level_0",y="region")
    st.plotly_chart(fig)

    st.header("Events held over the years")
    events_over_years=helper.data_over_years(df,'Event')
    fig=px.line(events_over_years,x="level_0",y="Event")
    st.plotly_chart(fig)
    
    st.header("Atheletes participated over the years")
    atheletes_over_years=helper.data_over_years(df,'Name')
    fig=px.line(atheletes_over_years,x="level_0",y="Name")
    st.plotly_chart(fig)

    st.header("Sports over time")
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0),annot=True)
    st.pyplot(fig)
    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)



if user_menu=='Country wise analysis':
    st.sidebar.title('Country wise analysis')
    countries=df['region'].dropna().unique().tolist()
    countries.sort()  
    selected_country=st.sidebar.selectbox('Select a country',countries)

    st.header(f"{selected_country} performance over the years")
    country_yearwise_data=helper.country_yearwise(df,selected_country)
    fig=px.line(country_yearwise_data,x="Year",y="Medal")
    st.plotly_chart(fig)

    st.header(f"{selected_country} excels in the following sports")
    fig,ax=plt.subplots(figsize=(20,20))
    y=helper.heatmap_countrywise_sport(df,selected_country)
    ax=sns.heatmap(y,annot=True)
    st.pyplot(fig)

    x = helper.most_successful_countrywise(df,selected_country)
    st.table(x)

if user_menu=='Athelete wise analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


