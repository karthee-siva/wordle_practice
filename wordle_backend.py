# import packages
import numpy as np
import pandas as pd
import random


class wordle_backend:
        
    def create_answer(self,dat,target_word_len):
        """Return  answer word, which can't just be a 4 letter word with an "s" at the end; for now, no duplicate letters either"""
        answer_word = random.choice(dat)
        while answer_word[-1]=="s" or len(set(answer_word)) != target_word_len:
            answer_word = random.choice(dat)
        return(answer_word)
    
    
    def in_dictionary(self,guess,dat):
        """Determines if guess is valid word in dictionary"""
        if guess in dat:
            return(True)
        else:
            return(False)
            
    # return colors for guess
    def give_colors(self,guess,answer_word,perfect,move_spot,absent):
        """Returns colors for each letter of guess based on presence in answer_word"""
        guess_colors = []
        for i in range(len(guess)):
            letter = guess[i]
            if letter in answer_word:
                if answer_word.index(letter)==i:
                    guess_colors.append(perfect)
                else:
                    guess_colors.append(move_spot)
            else:
                guess_colors.append(absent)
        return(guess_colors)
    
    def check_win(self,guess_colors,win_colors):
        """Returns whether guess meets win condition (all letters in right place)"""
        if guess_colors == win_colors:
            return(True)
        else:
            return(False)

