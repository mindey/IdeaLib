# IdeaLib

I need some way to estimate the i/o of ideas. I'll describe it later. Didn't sleep tonight. :)

The example below may be easier to understand, if you look at my [blog post](http://blog.mindey.com/2014/12/07/comparing-two-ideas-simple-modelling-of-growth/).

```{python}
from IdeaLib import Idea, IdeaList

a = Idea([({'time': 10,'money': 0, 'action': '+= idea1'}, {'oranges': [20, 30], 'apples': [30, 11]}), 
         ({'time': [1,3],'money': 10, 'action':'+= 1000 seconds + extracting seeds'}, {'orange seeds': 200, 'apple seeds': 150}),
         ({'time': 3653,'money': 15,'action':'+= planting field + 1 day of labor + 10 years of care'}, {'orange trees': 150, 'apple trees': 100}),
         ({'time': 365,'money': 1, 'action': '+= 1 year of waiting'}, {'oranges': 15000, 'apples': 10000})])

b = Idea([({'time': 0, 'money': 0, 'action': '+= idea2'}, {}),
          ({'time': 180, 'money': 0, 'action': 'waiting'}, {'right conditions for travel': 1, 'number of days there is resources to survive': 30}),
          ({'time': 30, 'money': 0, 'action': 'days in travel'}, {'bananas': 100000, 'apples': 0, 'oranges': 100000})])

x = IdeaList([a,b])

x.plot()
```

# Done:

* Custom scenarios
* Mean/median scenarios
* Best case scenarios
* Worst case scenarios
* Alignment by time
* Aligment by money and custom dimensions
* Weighting quantities by constant value

# ToDo:

* Write examples of the above
* Weighting Quantites by Changing Market Value
* Make a pip install

## Idea Definition Language Syntax Parsing
```{python}
from IdeaLib import Idea
x = Idea('''+= idea1
-> oranges 20, apples 30
+= seconds 1000, extracting_seeds 1, time 1
-> orange_seeds 200, apple_seeds 150
+= planting_field 1, days_of_labor 1, years_of_care 10, time 3650
-> orange_trees 50, apple_trees 100
+= years_of_waiting 1, time 365
-> oranges 5000, apples 10000
''')
x.to_df(dates=True,value=True)
```

