# %%
from chord import *

# %%
data = [
    [0, 2, 1, 0, 4],
    [0, 0, 0, 8, 0],
    [3, 0, 0, 0, 5],
    [0, 2, 0, 0, 0],
    [0, 0, 7, 0, 0]
]

names = ['A', 'B', 'C', 'D', 'E']

# %%
Chord(data, names).show()
Chord(data, names).to_html()

# %%