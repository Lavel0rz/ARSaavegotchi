import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
st.title('ARS Experiment')
import requests
from pprint import pprint



def run_query(query):
    request = requests.post('https://subgraph.satsuma-prod.com/tWYl5n5y04oz/aavegotchi/aavegotchi-core-matic/api',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))

import requests
import datetime
import pandas as pd

query = '''
{
 aavegotchis(orderBy:gotchiId,first:1000,where:{gotchiId_gt:0}) {
  gotchiId
  modifiedNumericTraits
  collateral
  hauntId
  level
  name
  owner {
    id
  }
 }
}


'''
def prepro(data):
    newdic = data.get('data',0)
    newdic2 = newdic.get('aavegotchis')
    nuevos = []
    new = []
    new2 = []
    new3 = []
    new4 = []
    new5 = []
    new6 = []
    new7 = []
    for i in newdic2:
        nuevos.append(i)
    for i in nuevos:
        new.append(i.get('collateral'))
        new2.append(i.get('gotchiId'))
        new3.append(i.get('modifiedNumericTraits'))
        new4.append(i.get('owner'))
        new5.append(i.get('name'))
        new6.append(i.get('hauntId'))
        new7.append(i.get('level'))
    df = pd.DataFrame(columns = ['NRG','AGG','SPK','BRN','EYES','EYEC'],data = new3)
    df['Collateral']=new
    df['ID']= new2
    df['Owner']= new4
    df['Name']= new5
    df['Haunt']=new6
    df['Level']=new7
    df=df.dropna()
    return df
@st.cache
def get_trait_visualizer_data_frame():
        result = run_query(query)
        df = prepro(result)
        df['Owner'] = df['Owner'].map(lambda x: x.get('id'))
        currentquery = 'gotchiId_gt:0'
        ultimo = (df.iloc[-1]['ID'])
        nextquery = query.replace(currentquery, 'gotchiId_gt:' + ultimo)
        df2 = prepro(run_query(nextquery))
        df2['Owner'] = df2['Owner'].map(lambda x: x.get('id'))
        df3 = pd.concat([df, df2])
        while len(df) != 0:
            ultimo = (df3.iloc[-1]['ID'])
            nextquery = query.replace(currentquery, 'gotchiId_gt:' + ultimo)
            df = prepro(run_query(nextquery))
            df['Owner'] = df['Owner'].map(lambda x: x.get('id'))
            df3 = pd.concat([df3, df])
        return df3

df3 = get_trait_visualizer_data_frame()
import pandas as pd
import numpy as np
df3 = df3[df3['Haunt']!='0']
# Define the conditions and corresponding class types
conditions = [
    ((df3['NRG'] > 50) & (df3['AGG'] > 50) & (df3['SPK'] <= 50) & (df3['BRN'] > 50)),
    ((df3['NRG'] <= 50) & (df3['AGG'] > 50) & (df3['SPK'] <= 50) & (df3['BRN'] > 50)),
    ((df3['NRG'] > 50) & (df3['AGG'] > 50) & (df3['SPK'] > 50) & (df3['BRN'] > 50)),
    ((df3['NRG'] > 50) & (df3['AGG'] <= 50) & (df3['SPK'] <= 50) & (df3['BRN'] > 50)),
    ((df3['NRG'] <= 50) & (df3['AGG'] <= 50) & (df3['SPK'] <= 50) & (df3['BRN'] > 50)),
    ((df3['NRG'] <= 50) & (df3['AGG'] > 50) & (df3['SPK'] > 50) & (df3['BRN'] > 50)),
    ((df3['NRG'] > 50) & (df3['AGG'] <= 50) & (df3['SPK'] > 50) & (df3['BRN'] > 50)),
    ((df3['NRG'] <= 50) & (df3['AGG'] <= 50) & (df3['SPK'] > 50) & (df3['BRN'] > 50)),
    ((df3['NRG'] > 50) & (df3['AGG'] > 50) & (df3['SPK'] <= 50) & (df3['BRN'] <= 50)),
    ((df3['NRG'] <= 50) & (df3['AGG'] > 50) & (df3['SPK'] <= 50) & (df3['BRN'] <= 50)),
    ((df3['NRG'] > 50) & (df3['AGG'] > 50) & (df3['SPK'] > 50) & (df3['BRN'] <= 50)),
    ((df3['NRG'] > 50) & (df3['AGG'] <= 50) & (df3['SPK'] <= 50) & (df3['BRN'] <= 50)),
    ((df3['NRG'] <= 50) & (df3['AGG'] <= 50) & (df3['SPK'] <= 50) & (df3['BRN'] <= 50)),
    ((df3['NRG'] <= 50) & (df3['AGG'] > 50) & (df3['SPK'] > 50) & (df3['BRN'] <= 50)),
    ((df3['NRG'] > 50) & (df3['AGG'] <= 50) & (df3['SPK'] > 50) & (df3['BRN'] <= 50)),
    ((df3['NRG'] <= 50) & (df3['AGG'] <= 50) & (df3['SPK'] > 50) & (df3['BRN'] <= 50))
]

class_types = [
    'Ranged Sprinter',
    'Healthy Ranged Sprinter',
    'Ethereal Ranger',
    'Stone Ranger',
    'Diamond Ranger',
    'Explosive Ranger',
    'Ethereal Stone Ranger',
    'Ethereal Diamond Ranger',
    'Sprinter Warrior',
    'Healthy Sprinter Warrior',
    'Ethereal Warrior',
    'Stone Warrior',
    'Diamond Warrior',
    'Explosive Warrior',
    'Ethereal Stone Warrior',
    'Ethereal Diamond Warrior'
]

# Assign the class types based on the conditions
df3['Types'] = np.select(conditions, class_types, default='OTHER')


# Function to map the numeric value to the corresponding rarity type
def map_rarity(value):
    if value >= 98:
        return "Mythical High"
    elif value <= 1:
        return "Mythical Low"
    elif 10 <= value <= 24:
        return "Uncommon Low"
    elif 75 <= value <= 90:
        return "Uncommon High"
    elif 2 <= value <= 9:
        return "Rare Low"
    elif 91 <= value <= 97:
        return "Rare High"
    elif 25 <= value <= 74:
        return "Common"
    else:
        return "Unknown"  # Or a default rarity if value doesn't fall within any range

# Map rarity for each column in the DataFrame
df3['NRG_Rarity'] = df3['NRG'].apply(map_rarity)
df3['AGG_Rarity'] = df3['AGG'].apply(map_rarity)
df3['SPK_Rarity'] = df3['SPK'].apply(map_rarity)
df3['BRN_Rarity'] = df3['BRN'].apply(map_rarity)


df3 = df3.reset_index().drop('index',axis=1)


st.subheader('Total Gotchis Trait Distribution')

import plotly.express as px
trait = st.radio('Select Trait',['NRG','BRN','AGG','SPK'])


# Replace `df3['NRG_Rarity']` with your actual column name
value_counts = df3[trait+'_Rarity'].value_counts()

# Create a Plotly bar chart
fig = px.bar(x=value_counts.index, y=value_counts.values)

# Set labels and title
fig.update_layout(xaxis_title=f'{trait}+"_Rarity"', yaxis_title='Count', title=f'Value Counts of {trait}')
st.plotly_chart(fig)
st.subheader('Different Gotchi Classes')
col_mk, col_mk2 = st.columns(2)

with col_mk:
    st.markdown('''
    NRG + AGG + SPK - BRN + ---------- Sprinter Ranger\n
    NRG - AGG + SPK - BRN + ---------- Healthy Sprinter Ranger\n
    NRG + AGG + SPK + BRN + ---------- Ethereal Ranger\n
    NRG + AGG - SPK - BRN + ---------- Stone Ranger\n
    NRG - AGG - SPK - BRN + ---------- Diamond Ranger\n
    NRG - AGG + SPK + BRN + ---------- Explosive Ranger\n
    NRG + AGG - SPK + BRN + ---------- Ethereal Stone Ranger\n
    NRG - AGG - SPK + BRN + ---------- Ethereal Diamond Ranger\n
    ''')

with col_mk2:
    st.markdown('''
    NRG + AGG + SPK - BRN - ---------- Sprinter Warrior\n
    NRG - AGG + SPK - BRN - ---------- Healthy Sprinter Warrior\n
    NRG + AGG + SPK + BRN - ---------- Ethereal Warrior\n
    NRG + AGG - SPK - BRN - ---------- Stone Warrior\n
    NRG - AGG - SPK - BRN - ---------- Diamond Warrior\n
    NRG - AGG + SPK + BRN - ---------- Explosive Warrior\n
    NRG + AGG - SPK + BRN - ---------- Ethereal Stone Warrior\n
    NRG - AGG - SPK + BRN - ---------- Ethereal Diamond Warrior\n
    ''')


value_counts_types = df3['Types'].value_counts()
fig2 =px.bar(x=value_counts_types.index, y=value_counts_types.values)
fig2.update_layout(xaxis_title='Types', yaxis_title='Count', title=f'Value Counts of each Type')
st.plotly_chart(fig2)
st.subheader('Trait distribution per Type')
type = st.selectbox('Select Type',df3['Types'].unique())
type_trait = st.radio('Select Trait For Type',['NRG','BRN','AGG','SPK'])

value_counts_per_type= df3[df3['Types']==type][type_trait+'_Rarity'].value_counts()
fig3 =px.bar(x=value_counts_per_type.index, y=value_counts_per_type.values)
fig3.update_layout(xaxis_title='Traits', yaxis_title='Count', title=f'{type_trait} value counts for {type}')
st.plotly_chart(fig3)
