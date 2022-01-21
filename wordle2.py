import numpy as np
import pandas as pd
import random
import streamlit as st
from wordle_backend import wordle_backend

st.title("Wordle")
st.text("by Tejal Patwardhan")

st.markdown(""" 

## Rules:
* Letter in the right place is green
* Letter in the wrong place is yellow
* Letter not in the answer is grey

""")

backend = wordle_backend()

# upload list of all scrabble words
dat = pd.read_csv("scrabbledictionary.csv",header=None)
dat.columns = ["Word"]
dat["Word"] = dat["Word"].astype('str')

# color code the guess
perfect = "green"
move_spot = "yellow"
absent = "grey"

# win condition
win_colors = [perfect, perfect, perfect, perfect, perfect]

# use only 5-letter words
target_word_len = 5

# ensure dictionary only has target length words and convert to list
dat = dat[dat['Word'].apply(lambda x: len(x)==target_word_len)]
dat = dat['Word'].tolist()

answer_word = backend.create_answer(dat,target_word_len)

with st.form(key="form"):
    guess = st.text_input("Guess a 5 letter word")
    st.text(f"(Example: payer)")

    submit_button = st.form_submit_button(label='Submit guess')

    if submit_button:
        with st.spinner("Determining validity..."):
            guess_validity = backend.in_dictionary(guess,dat)
        st.text("Guess validity: ")
        st.text(guess_validity)
        
        if (guess_validity):
            guess_colors = backend.give_colors(guess,answer_word,perfect,move_spot,absent)
            st.markdown("____")
            st.text("Colors for your guess: ")
            st.text(guess_colors)
            
            st.text("Did you guess the wordle?")
            win_check = backend.check_win(guess_colors,win_colors)
            st.text(win_check)
            
            
            
        else:
            st.text("Please enter a real 5 letter word to proceed.")


with st.form(key="form for answer"):
    if st.form_submit_button(label='Reveal answer'):
        st.text("Answer: " + answer_word)
