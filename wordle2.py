# import packages
import numpy as np
import pandas as pd
import random
import streamlit as st
from streamlit import caching
from wordle_backend import wordle_backend

# landing page
st.set_page_config(page_title="Wordle Sandbox", page_icon=":book:", layout="centered", initial_sidebar_state="expanded", menu_items=None)
st.sidebar.title("Wordle Practice - Desktop Only")
st.sidebar.text("by Tejal Patwardhan")

with st.sidebar.expander("Rules"):
     st.text("""
        Guess the answer in 6 tries.
        Letters will be color-coded:
        * Green: Letter placed correctly
        * Yellow: Letter in wrong place
        * Grey: Wrong letter
        """)


# load in backend
backend = wordle_backend()

# upload list of words from Scrabble word dictionary
dat = pd.read_csv("scrabbledictionary.csv",header=None)
dat.columns = ["Word"]
dat["Word"] = dat["Word"].astype('str')

# color code the guess
perfect = "#6aaa64" #"green"
move_spot = "#c9b458" #yellow"
absent = "#787c7e" #"grey"

# win condition
win_colors = [perfect, perfect, perfect, perfect, perfect]

# use only 5-letter words
target_word_len = 5

# ensure dictionary only has target length words and convert to list
dat = dat[dat['Word'].apply(lambda x: len(x)==target_word_len)]
dat = dat['Word'].tolist()

# create answer
if 'answer_word' not in st.session_state:
    st.session_state.answer_word = backend.create_answer(dat,target_word_len)

# initialize container for guessing
form_container = st.container()

# initialize grid for letters
col1, col2, col3, col4, col5 = st.columns(5)
cols_list = [col1, col2, col3, col4, col5]

# store letters/colors guessed so far
if 'guesses_to_date' not in st.session_state:
    st.session_state.guesses_to_date = []
if 'guess_colors_to_date' not in st.session_state:
    st.session_state.guess_colors_to_date = []
if 'guess_counter' not in st.session_state:
    st.session_state.guess_counter = 0
if 'reset_needed' not in st.session_state:
    st.session_state.reset_needed = 0

# guess a word
with form_container.form(key="guess_form"):
    
    # submit guess
    guess = st.text_input("Guess a 5 letter word, e.g., 'payer'").lower()
    submit_button = st.form_submit_button(label='Submit guess')

    if submit_button:
    
        # check whether guess is in dictionary of valid guesses
        guess_validity = backend.in_dictionary(guess,dat)
        
        # only proceed if valid guess
        if (guess_validity==False):
            st.text("Please enter a real 5 letter word to proceed.")
            
            # everyone should still see words
            for i in range(len(st.session_state.guesses_to_date)):
                for j in range(len(st.session_state.guesses_to_date[i])):
                    with cols_list[j]:
                        st.markdown(f'<h1 style="background-color:{st.session_state.guess_colors_to_date[i][j]};color:black;font-size:18px;border-radius:5%;"><center>{st.session_state.guesses_to_date[i][j]}</center></h1></br>', unsafe_allow_html=True)
        
        else:
            # increase counter of guesses by 1
            st.session_state.guess_counter += 1
            
            # add guess and guess colors to session state
            st.session_state.guesses_to_date.append(guess)
            guess_colors = backend.give_colors(guess,st.session_state.answer_word,perfect,move_spot,absent)
            st.session_state.guess_colors_to_date.append(guess_colors)
            
            # everyone should still see words
            for i in range(len(st.session_state.guesses_to_date)):
                for j in range(len(st.session_state.guesses_to_date[i])):
                    with cols_list[j]:
                        st.markdown(f'<h1 style="background-color:{st.session_state.guess_colors_to_date[i][j]};color:black;font-size:18px;border-radius:5%;"><center>{st.session_state.guesses_to_date[i][j]}</center></h1></br>', unsafe_allow_html=True)
                        
            # see if user has won yet, if they win say Congrats and reset
            win_check = backend.check_win(guess_colors,win_colors)
            if win_check == True:
                st.sidebar.text("Congrats!")
                st.session_state.reset_needed = 1

# see answer word
with st.sidebar.form(key="form for answer"):
    if st.form_submit_button(label="Reveal answer"):
        st.text("Answer: " + st.session_state.answer_word)
        
        # everyone should still see words
        for i in range(len(st.session_state.guesses_to_date)):
            for j in range(len(st.session_state.guesses_to_date[i])):
                with cols_list[j]:
                    st.markdown(f'<h1 style="background-color:{st.session_state.guess_colors_to_date[i][j]};color:black;font-size:18px;border-radius:5%;"><center>{st.session_state.guesses_to_date[i][j]}</center></h1></br>', unsafe_allow_html=True)

# if guess_counter hits 6, reset
if st.session_state.guess_counter == 6:
    st.session_state.reset_needed = 1

# reset game
if st.session_state.reset_needed == 1:
    st.sidebar.text("Answer: " + st.session_state.answer_word)
    st.sidebar.text("Play again with a new word")
    for key in st.session_state.keys():
        del st.session_state[key]
