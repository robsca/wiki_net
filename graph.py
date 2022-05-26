from pyvis.network import Network
import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Find and analize data
@st.cache
def find_correlated_words(word):
    '''
    Review the section that choose the paragraph - See also - Not needed, sufficient number of outputs
    '''
    # Connect and get data
    url = f'https://en.wikipedia.org/wiki/{word}'
    data = requests.get(url)
    # Obtain data from html, filter taking only the text
    soup = BeautifulSoup(data.text, 'html.parser')
    texts = soup.findAll(text=True)

    # Define indexes for research in texts
    index, start_index, end_index = 0, 0, 0
    for t in texts:
        if t == 'See also':
            #print(f'See also: {index}')
            start_index = index
        if t == 'References':
            #print(f'Reference : {index}')
            end_index = index
        index +=1

    # Take the needed values 
    data = texts[start_index: end_index]

    # Define the useless values -> Move this variable in other file, or find a better system as filter.
    from no_words import useless_words
    no_word = useless_words()
    
    # Filter the words for a cleaner data list -
    # minimum lenght value, first letter is Capital, Not in no_words list
    correlated_words = [str(items) for items in data if not len(items.split()) > 4 and items[0].isupper() and no_word.count(items.strip(' . ')) == 0]
    return word, correlated_words

def nodes(word,n, depth):
    # if the word is not in list then do this
    '''This is the working one'''
    counter = 0
    big_container = []
    word, correlated_words = find_correlated_words(word)

    if depth == 1:
        for w in correlated_words:
            if len(big_container)<n:
                print(f'Words Connected :{counter}')
                counter +=1
                word, correlated_ = find_correlated_words(w)
                big_container.append([w, correlated_])
                for e in correlated_:
                    if len(big_container)<n:
                        print(f'Words Connected :{counter}')
                        counter +=1
                        
                        word, correlated_w = find_correlated_words(e)
                        big_container.append([e, correlated_w])
                        for a in correlated_w:
                            if len(big_container)<n:
                                print(f'Words Connected :{counter}')
                                counter +=1
                                
                                word, correlated__ = find_correlated_words(a)
                                big_container.append([a, correlated__])

                                for b in correlated__:
                                    if len(big_container)<n:
                                        print(f'Words Connected :{counter}')
                                        counter +=1
                                        
                                        word, correlated___ = find_correlated_words(b)
                                        big_container.append([b, correlated___])
    if depth == 2:
        for w in correlated_words:
            if len(big_container)<n:
                print(f'Words Connected :{counter}')
                counter +=1
                word, correlated_ = find_correlated_words(w)
                big_container.append([w, correlated_])
                for e in correlated_:
                    if len(big_container)<n:
                        print(f'Words Connected :{counter}')
                        counter +=1
                        
                        word, correlated_w = find_correlated_words(e)
                        big_container.append([e, correlated_w])
                        for a in correlated_w:
                            if len(big_container)<n:
                                print(f'Words Connected :{counter}')
                                counter +=1
                                
                                word, correlated__ = find_correlated_words(a)
                                big_container.append([a, correlated__])

                                for b in correlated__:
                                    if len(big_container)<n:
                                        print(f'Words Connected :{counter}')
                                        counter +=1
                                        word, correlated___ = find_correlated_words(b)
                                        big_container.append([b, correlated___])

                                        for c in correlated___:
                                            if len(big_container)<n:
                                                print(f'Words Connected :{counter}')
                                                counter +=1
                                                
                                                word, correlated____ = find_correlated_words(c)
                                                big_container.append([c, correlated____])
    if depth == 3:
        for w in correlated_words:
            if len(big_container)<n:
                print(f'Words Connected :{counter}')
                counter +=1
                word, correlated_ = find_correlated_words(w)
                big_container.append([w, correlated_])
                for e in correlated_:
                    if len(big_container)<n:
                        print(f'Words Connected :{counter}')
                        counter +=1
                        
                        word, correlated_w = find_correlated_words(e)
                        big_container.append([e, correlated_w])
                        for a in correlated_w:
                            if len(big_container)<n:
                                print(f'Words Connected :{counter}')
                                counter +=1
                                
                                word, correlated__ = find_correlated_words(a)
                                big_container.append([a, correlated__])

                                for b in correlated__:
                                    if len(big_container)<n:
                                        print(f'Words Connected :{counter}')
                                        counter +=1
                                        word, correlated___ = find_correlated_words(b)
                                        big_container.append([b, correlated___])

                                        for c in correlated___:
                                            if len(big_container)<n:
                                                print(f'Words Connected :{counter}')
                                                counter +=1
                                                word, correlated____ = find_correlated_words(c)
                                                big_container.append([c, correlated____])

                                                for d in correlated____:
                                                    if len(big_container)<n:
                                                        print(f'Words Connected :{counter}')
                                                        counter +=1
                                                        
                                                        word, correlated_____ = find_correlated_words(d)
                                                        big_container.append([d, correlated_____])       
    # else
    # open csv, take the csv file and return that as big container

    return big_container

def rank(parola,n, depth):
    container = nodes(parola,n,depth)

    # Add value to relations
    words = [word[0] for word in container]
    correlations = [word[1] for word in container]

    rank = []
    for word in words:
        counter = 0
        for relat in correlations:
            counter += relat.count(word)
        rank.append([counter, word])

    rank = sorted(rank)
    max_value = rank[-1][0]
    import pandas as pd
    rank = pd.DataFrame(rank[::-1])
    rank.columns = ['Count', 'Word']
    rank = rank[['Word', 'Count']]
    rank = rank.drop_duplicates()
    return rank, max_value, container

def create_graph(got_data):
    got_net = Network(height='750px', width='100%', bgcolor='white', font_color='grey')
    got_net.force_atlas_2based()

    sources = got_data['Source']
    targets = got_data['Target']
    weights = got_data['Weight']

    edge_data = zip(sources, targets, weights)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        got_net.add_node(src, src, title=src, color = 'blue')
        got_net.add_node(dst, dst, title=dst, color = 'green')
        got_net.add_edge(src, dst, value=w)

    neighbor_map = got_net.get_adj_list()

    # add neighbor data to node hover data
    for node in got_net.nodes:
        node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
        node['value'] = len(neighbor_map[node['id']])


    got_net.show('graph.html')