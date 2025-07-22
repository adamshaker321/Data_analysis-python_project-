import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st
from collections import Counter

st.set_page_config(page_title='Tips dashboard',
                   page_icon=None, layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)

# Load dataset
df = pd.read_csv("cleaned-Titanic-Dataset.csv")

# Sidebar
st.sidebar.header('🛳 Titanic data analysis')
st.sidebar.image('titanic.png')
st.sidebar.markdown('Made by Eng .[Adam shaker](https://github.com/adamshaker321)')
column = st.sidebar.selectbox('Filter by', ['Sex', 'Pclass'])
his = st.sidebar.selectbox('Filter price distribution by', ['all classes', '1st Class', '2nd Class', '3rd Class'])

# Row 1: Metrics
a0, a1, a2 = st.columns(3)
a0.metric('Mean of Ages in Titanic', round(df['Age'].mean(), 2))
a1.metric('Mean Ticket Fare', round(df['Fare'].mean(), 2))
a2.metric('Most Common Class', df['Pclass'].mode()[0])

# Row 2: Top 10 Richest
a3, = st.columns(1)
a3.write("### 💰 The Ten Richest Passengers")
a3.dataframe(df.sort_values(by='Fare', ascending=False).head(10))

# Row 3: Age Distribution
a4, a5 = st.columns(2)
with a4:
    fig1, ax1 = plt.subplots()
    st.subheader('Age Distribution')
    ax1.hist(df['Age'].dropna(), bins=20, color='pink', label='Age')
    ax1.set_xlabel('Age')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

with a5:
    st.subheader('')
    if column is not None:
        count = Counter(df[column])
        fig2, ax2 = plt.subplots()
        ax2.pie(
            count.values(),
            labels=count.keys(),
            explode=[0]*len(count),
            shadow=True,
            autopct='%1.1f%%',
            colors=plt.cm.Paired.colors
        )
        ax2.set_title(f'Distribution by {column}')
        centre_circle = plt.Circle((0, 0), 0.40, fc='white')
        fig2.gca().add_artist(centre_circle)
        st.pyplot(fig2)
    else:
        st.info('Please select a column from the sidebar to view distribution.')
a6, a7 = st.columns(2)
with a6:
    plt.style.use('dark_background')
    fig3, ax3 = plt.subplots()
    age_counts = df['Age'].astype(int).value_counts().sort_index()
    ax3.plot(age_counts.index, age_counts.values, marker='o', color='cyan')
    ax3.set_title('Number of Passengers by Age')
    ax3.set_xlabel('Age')
    ax3.set_ylabel('Number of Passengers')
    ax3.grid(True)
    st.pyplot(fig3)

# Row 4: Price Distribution by class
with a7:
    st.subheader('Price Distribution by Class')
    fig4, ax4 = plt.subplots()

    if his == '1st Class':
        class_data = df[df['Pclass'] == 1]
    elif his == '2nd Class':
        class_data = df[df['Pclass'] == 2]
    elif his == '3rd Class':
        class_data = df[df['Pclass'] == 3]
    else:
        class_data = df  # Show all if no selection

    ax4.hist(class_data['Fare'], bins=20, color='orange', edgecolor='black')
    ax4.set_xlabel('Fare')
    ax4.set_ylabel('Count')
    ax4.set_title(f'Fare Distribution: {his if his else "All Classes"}')
    ax4.grid(True)
    st.pyplot(fig4)
