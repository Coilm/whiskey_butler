

import pandas
import streamlit as st
print(st.__version__)
import pandas as pd
import numpy as np
import sqlite3
from sklearn.neighbors import NearestNeighbors
import streamlit_analytics_mod as streamlit_analytics

from streamlit.script_run_context import get_script_run_ctx

SEARCH_CLICKED = False
st.set_page_config(layout="wide")

def search_in_db(db_file, whiskey_name):
    db = sqlite3.connect(db_file)
    mycursor = db.cursor()
    mycursor.execute("SELECT `Whiskey Name` FROM whiskeys WHERE `Whiskey Name` LIKE '%{}%';".format(whiskey_name.lower().strip()))
    list_whiskeys_input = mycursor.fetchall()

    return list_whiskeys_input

def find_similar(db_file, whiskey_name, simil_number=10):
    db = sqlite3.connect(db_file)
    mycursor = db.cursor()

    mycursor.execute("SELECT name FROM PRAGMA_TABLE_INFO('whiskeys');")
    whiskeys_col = mycursor.fetchall()
    mycursor.execute("SELECT name FROM PRAGMA_TABLE_INFO('type');")
    type_col = mycursor.fetchall()
    mycursor.execute("SELECT name FROM PRAGMA_TABLE_INFO('words');")
    words_col = mycursor.fetchall()

    whiskeys_col = [r[0] for r in whiskeys_col]
    type_col = [r[0] for r in type_col]
    words_col = [r[0] for r in words_col]

    mycursor.execute("SELECT whiskeys.*, type.*, words.* FROM whiskeys INNER JOIN type ON whiskeys.id=type.id INNER JOIN words ON whiskeys.id=words.id;")
    result_merge = mycursor.fetchall()

    index_word = len(whiskeys_col) + len(type_col)
    mycursor.execute("SELECT * from urls")
    urls = mycursor.fetchall()

    df_urls = pd.DataFrame(urls, columns=(['id', 'Whiskey Name', 'urls']))
    df = pd.DataFrame(result_merge, columns=whiskeys_col+type_col+words_col)
    print(df.keys()[index_word:])
    df.drop('id', axis=1, inplace=True)
    X = df.select_dtypes(include=np.number)

    df_urls['Whiskey Name'] = df_urls['Whiskey Name'].str.strip().str.lower()

    nbrs = NearestNeighbors(n_neighbors=11, algorithm='ball_tree').fit(X)

    val_index = df[df['Whiskey Name'] == whiskey_name.replace('_', ' ')].index
    closest_neighbors = nbrs.kneighbors(np.array(X.iloc[val_index]).reshape(1,-1), 1+simil_number)[1]
    list_similar = []
    top_words = []
    for idx, i in enumerate(closest_neighbors[0]):
        list_similar.append((df['Whiskey Name'].iloc[i]))#.capitalize())
        keywords = df.iloc[i].T[df.keys()[index_word:]].sort_values(ascending=False).head(5).index
        top_words.append(keywords)

    initial_top_words = top_words[0]
    initial = list_similar[0]
    top_words = top_words[1:]

    list_similar = df_urls.loc[df_urls['Whiskey Name'].isin(list_similar[1:])]

    urls_tmp = list_similar.groupby('Whiskey Name')['urls'].transform(lambda x: ';'.join(x))
    list_similar.drop_duplicates('Whiskey Name', inplace=True)
    list_similar['urls'] = urls_tmp

    return initial, list_similar, top_words, initial_top_words


streamlit_analytics.start_tracking()

option = ''
st.title('Your Personal Whiskey Butler')
user_input = st.text_input(label='Please write the name of the whiskey you want to search.', value='')

quantity = st.select_slider("How many similar whiskey do you want to find?", options=range(1, 51), value=10)


if user_input != '':
    if user_input == '':
        st.warning('Please fill the box above')

    else:
        DATABASE = 'whiskey_database.db'

        list_whiskeys_input = search_in_db(DATABASE, user_input)
        list_whiskeys_input = [whiskey[0] for whiskey in list_whiskeys_input]

        if len(list_whiskeys_input) > 1:
            option = st.selectbox(
                'We found multiple matches, please select the one you want.',
                list_whiskeys_input)
        elif len(list_whiskeys_input) == 0:
            st.warning('No whiskey with this name was found in the database')
            option = ''
        else:
            option = list_whiskeys_input[0]

if st.button('Find Similar Whiskeys'):
    if option != '':
        with st.spinner('Finding similar whiskeys...'):
            initial, result, keywords, initial_top_words = find_similar(DATABASE, option, quantity)
        #result = list(result_name['Whiskey Name'])
        #reviews = list(result_name['reviews'])

        st.title(initial)
        keyword_str = '***keywords: ***'
        for keyword in initial_top_words:
            keyword_str += keyword + ', '
        st.subheader(keyword_str[:-2])
        num_col = int(np.ceil(len(result) / 10))

        columns = st.columns(num_col)
        current_col_idx = -1
        for i, (idx, val) in enumerate(result.iterrows()):
            if i % 10 == 0:
                current_col_idx += 1

            with columns[current_col_idx]:
                with st.expander(str(i + 1) + '. ' + val['Whiskey Name'].capitalize()):
                    keyword_str = '***keywords: ***'
                    for keyword in keywords[i]:
                        keyword_str += keyword + ', '

                    st.write(keyword_str[:-2] + '\n')
                    for url in val['urls'].split(';'):
                        if url[-2:] == '/?':
                            url = url[:-2]
                        if url[-1] == '/':
                            url += '?sort=old'
                        else:
                            url += '/?sort=old'

                        st.write('* ' + '[' + url.split('/')[-2].replace('_', ' ') + '](' + url + ')\n')

    else:
        st.warning('No whiskey with this name was found in the database')

streamlit_analytics.stop_tracking()