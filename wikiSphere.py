import streamlit as st
st.set_page_config(layout="wide")
import streamlit.components.v1 as components  # Import Streamlit

#import the functions
from graph import *

# Streamlit Template
st.sidebar.title('WikiLinks')
a, b = '', ''
# Word 1
with st.sidebar.expander(f'Word 1{a}'):
    a = st.text_input('Insert Word')
    n = st.slider('Insert max connections', min_value=100, max_value=5000, step = 100)
    depth = st.slider('Depth of research', min_value=1, max_value=3, step = 1)
# Word 2
with st.sidebar.expander(f'Word 2{b}'):
    b = st.text_input('Insert another word')
    n1 = st.slider('Insert number of links', min_value=100, max_value=5000, step = 100)
    depth1 = st.slider('Depth of research 1', min_value=1, max_value=3, step = 1)

# Start button and Logic
start = st.sidebar.button('Press')
if start:
    # Logic
    ranking, max_value, container = rank(a, n, depth)
    ranking1, max_value1, container1 = rank(b,n1, depth1)
   
    ranking = ranking.dropna()
    ranking = pd.DataFrame(ranking, index = [i for i in range(len(ranking))])
    
    # word1
    word__1 = pd.DataFrame([a for i in range(len(ranking.iloc[::]))], columns=['word'])
    frame = [word__1, ranking]
    ranking = pd.concat(frame, axis=1)
    ranking = ranking.dropna()
    ranking1 = pd.DataFrame(ranking1, index = [i for i in range(len(ranking1))])
    
    # word2
    word__2 = pd.DataFrame([b for i in range(len(ranking1.iloc[::]))], columns=['word'])
    frame = [word__2, ranking1]
    ranking1 = pd.concat(frame, axis=1)
    ranking1 = ranking1.dropna()

    # unify the dataframes
    frame = [ranking, ranking1]
    df = pd.concat(frame, axis=0)
    df.columns = ['Source', 'Target', 'Weight']
    create_graph(df)

    # open html file
    with open("graph.html", "r") as f:
        components.html(f.read(),
                width=800, height=300)

    # Visualize tabs
    c1, c2 = st.columns(2)  
    with c1:  
        with st.expander(f'Visualize results {a}'):
                st.table(ranking)
    with c2:
        with st.expander(f'Visualize results {b}'):
                st.table(ranking1)
import os
if '__main__' == __name__:
    # run only once
    if not st._is_running_with_streamlit:
       os.system("streamlit run wikiSphere.py") # run streamlit