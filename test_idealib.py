import unittest
import pytest
import pandas as pd
from IdeaLib import Idea, IdeaList


# Sample Idea instances for testing
def create_sample_idea():
    return Idea(r'''
i1: time 0.003\0.004, loaf of black bread 1, butter grams 15, tomato 0.5, salt grams 0.4
o1: sandwich 1
i2: eggs 2\5, scrambling actions 50\100, time 0.003\0.005
o2: scrambled egg servings 1
i3: coffee teaspoon 1\2, liters of water 0.2\0.3, time 0.003\0.005
o3: cup of coffee 1\1.5
    ''')

def create_sample_idea_with_weights():
    return Idea(r'''
add: peel 1, time 2, apple 1
get: peeled apple 1
add: mash 2, strawberry 1
get: strawberry jam 0.2
''', iw={'apple': 1, 'strawberry': 0.1},\
     ow={'peeled apple': 5, 'strawberry jam': 7}) #.to_df(dates=True, cumsum=True)

def create_sample_idea_list():
    idea1 = create_sample_idea()
    idea2 = Idea(r'''
入: 剥离皮肤 1, time 2\4, 苹果 1
出: 苹果去皮 1
入: 捣碎 2, 草莓 1, time 1\3
出: 草莓酱 0.2
''')
    return IdeaList([idea1, idea2])

# Test cases
def test_idea_creation():
    idea = create_sample_idea()
    df = idea.to_df()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_idea_weights():
    idea = create_sample_idea_with_weights()
    df = idea.to_df(dates=True)
    assert 'peeled apple' in df.columns
    assert df['ovalue'].iloc[0] == 5  # Check the output value

def test_idea_list_creation():
    ideas = create_sample_idea_list()
    assert len(ideas) == 2  # Check that we have two ideas in the list

def test_combined_idea_output():
    ideas = create_sample_idea_list()
    ideas.align()
    ideas.merge()
    assert isinstance(ideas.df, pd.DataFrame)

def test_choice_method():
    ideas = create_sample_idea_list()
    top_idea = ideas.choice(capital=100)
    assert isinstance(top_idea, Idea)

if __name__ == '__main__':
    pytest.main()
