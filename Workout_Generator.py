import streamlit as st
import pandas as pd
import random

def GenerateExercises(selected_exercises, number):
    count=0
    exercise_list = pd.DataFrame(columns=['name', 'type', 'description', 'reps'])
    while count < number:
        rand = random.randrange(0,len(selected_exercises)) #choose a random number from range of selected exercise list length
        if selected_exercises.iloc[rand]['name'] not in exercise_list['name'].tolist():
            exercise_list.loc[len(exercise_list)] = selected_exercises.iloc[rand]
            count = count + 1
    return exercise_list 

exercises = pd.read_csv('Data/Exercises.csv') #load exercise file
types = st.multiselect('Which muscle groups do you want to hit', options=['Chest', 'Shoulders', 'Arms', 'Back', 'Legs', 'Core'])
selected_exercises = exercises[exercises['type'].isin(types)] #filtered exercise list
number = st.number_input("Number Of Exercises", step=1, min_value=0, max_value=len(selected_exercises))

if st.button('Generate'):
    exercise_list = GenerateExercises(selected_exercises, number)
    for index, row in exercise_list.iterrows():
        st.write(f'**{row['name']}**')
        st.write(f'**Muscle Group: {row['type']}**')
        st.write(f'**Reps: {row['reps']}**')
        with st.expander('description'):
            st.markdown(row['description'])
            st.video('Data/ExerciseVids/' + row['name'].lower().replace(" ", "") + '.MOV', loop=True, autoplay=True, muted=True)