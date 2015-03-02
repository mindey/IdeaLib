# IdeaLib

I [need](http://www.halfbakery.com/idea/How_20to_20Analyze_20Ideas_20Quantitatively_3f) some way to estimate the i/o of ideas. I'll describe it later. Didn't sleep tonight. :)

The example below may be easier to understand, if you look at [IDL description](http://mindey.com/IdeaLib.html) my [blog post](http://blog.mindey.com/2014/12/07/comparing-two-ideas-simple-modelling-of-growth/).

This is basically an idea of a library to leverage our decisions on the databases of ideas, and a language to create such databases by describing existing ideas.

# Usage

```
pip install IdeaLib
```
or simply
``wget https://raw.githubusercontent.com/Mindey/IdeaLib/master/IdeaLib/IdeaLib.py``

Dependencies: [Pandas](https://github.com/pydata/pandas) and [Numpy](https://github.com/numpy/numpy), not included in requirements.

## Create Ideas

### Minimal
```{Python}
from IdeaLib import Idea, IdeaList
Idea(r'''
: do 100
: profit 1000
''').to_df()
```

The ``: `` (colon and whitespace) is currently a separator for label of input/output.

This way, adding ``.to_df()`` immediately after an idea is a way to immediately preview your result. 

### Beyond Minimal

**General rule:** _odd_ rows are _inputs_, _even_ rows are _outputs. Prefixes are optional.

```{Python}
Idea(r'''
label1: do1 100\200, time 10\15
label2: profit 1000
label3: do2 10\15, time 15\20
label4: profit 10000\20000, waste 100\50
''').to_df(dates=True) #.plots()
```

Use ``to_df()`` or ``.to_df(dates=True, scenario='worst')`` (could be 'best', 'normal'), or calling ``.plot('best')`` or ``.plots()`` this way rather than saving Idea instance it into a variable in order to get a preview immediately as you compose the content of idea. Recommend using IPython Notebook for that.

### With Custom Weights

Weights for items can be provided as value vectors ``iw=1`` (input weights, ``ow=1`` (output weights), which are the defaults, but can be defined by providing a different scalar value, or a dictionary, for example:

```
Idea(r'''
add: peel 1, time 2, apple 1
get: peeled apple 1
add: mash 2, strawberry 1
get: strawberry jam 0.2
''', iw={'apple': 1, 'strawberry': 0.1},\
     ow={'peeled apple': 5, 'strawberry jam': 7}).to_df(dates=True, cumsum=True)
```

### Assembling lists of ideas

Assembling lists of ideas requires writing them into variables first. For example.

#### Breakfast

Idea with a realistic **relative values** in some currency:

```{Python}
idea = Idea(r'''
i1: time 0.003\0.004, loaf of black bread 1, butter grams 15, tomato 0.5, salt grams 0.4
o1: sandwitch 1
in2: eggs 2\5, scrambling actions 50\100, time 0.003\0.005
out2: scrambled egg servings 1
input3: coffee teaspoon 1\2, liters of water 0.2\0.3, time 0.003\0.005
output3: cup of coffee 1\1.5
''', iw={'time': 10, 'loaf of black bread': 0.1, 'butter grams': 0.01, \
    'tomato': 0.2, 'salt grams': 0.001, 'eggs': 0.2, \
    'coffee teaspoon': 0.002, 'liters of water': 0.001}, \
     ow={'scrambled egg servings': 5, 'cup of coffee': 7, 'sandwitch': 5})
```

It is possible also to define the start time for idea, example:
```
idea.start_date = datetime.datetime(2014,1,1,14,15)
```
The default is "now".

#### Strawberry Jam
Just another idea with default **relative values** of "1" per every item.
```{Python}
idea2 = Idea(r'''
入: 剥离皮肤 1, time 2\4, 苹果 1
出: 苹果去皮 1
入: 捣碎 2, 草莓 1, time 1\3
出: 草莓酱 0.2
''')
```

## Generate scenarios

```{Python}
idea.to_df(scenario='normal')
idea.to_df(scenario='best', dates=True)
idea.to_df(scenario='worst', dates=True)
```
Recommend using ``dates=True`` whenever you have **time** in at least one of your inputs.

## Generate plots
```{Python}
idea.plot()
idea2.plot(scenario='best')
```

Plotting all scenarios in one graph:
```{Python}
idea.plots()
```

Call .plot() or .plots() for several ideas in the same execution cell in IPython Notebook to combine them automagically.

## Combine ideas into lists
```{Python}
ideas = IdeaList([idea, idea2])
```

## Choose from ideas (not yet available!)
```{Python}
ideas.choice(preferences={'sandwitch': 0.1, 'coffee': 0.9}, capital=100)
```
(produce weighted lists of which ideas to invest to, in what proportions)

# Syntax
```
i1: time 0.003\0.004, loaf of black bread 1, butter grams 15, tomato 0.5, salt grams 0.4
o1: sandwitch 1
i2: eggs 2\5, scrambling actions 50\100, time 0.003\0.005
o2: scrambled egg servings 1
i3: coffee teaspoon 1\2, liters of water 0.2\0.3, time 0.003\0.005
o3: cup of coffee 1\1.5
```

Name precedes value. Name-value pairs are separated by commas.

Backslash signs indicate different scenarios. E.g., in best case scenario, we expect spending 0.003 day for making sandwitch, in worst -- 0.004 day.

The default for **time** is "days", because it is a convenient timescale for both long-term project (e.g., 1825 days business plan), and short term-projects (0.04 days lecture), and it is the only reserved word, that is occasionally treated differently, for example, is used in ``.to_df()`` method to compute dates, however, you can change it by updating ``i.time_unit`` attribute with a ``datetime.timedelta()`` object.

The default assumption is that the project starts now, but you can change that by updating ``i.start_time`` attribute with a ``datetime.datetime()`` object.

The default value weights for the value of i/o (input/output) are considered to be equal to "1", and ``iw, ow`` params are optional. You can redefine them by providing the weighting vectors with ``iw`` and ``ow`` parameters, in the Idea constructor. Defining at least one of the values resets the defaults of others to "0". for example: 

```{Python}
iw={'time': 10, 'loaf of black bread': 0.1, 'butter grams': 0.01, \
    'tomato': 0.2, 'salt grams': 0.001, 'eggs': 0.2, 'scrambling actions': 0, \
    'coffee teaspoon': 0.002, 'liters of water': 0.001}
ow={'scrambled egg servings': 5, 'cup of coffee': 7, 'sandwitch': 5}
```

So, here you would not necessarily need to type in ``'scrambling actions': 0``, because it (and all other defaults) would be reset to "0", if at least one value in ``iw`` dictionary is provided.

# Idea Definition Language

**Idea Definition Language (IDL)** is supposed to be a language to describe simple ideas that are encoded as lists of actions and their outcomes.

Ideas are assumed to be objects that contain an ordered map between action and their expected non-cumulative results.

```
f: 
do_x1 -> get_y1
do_x2 -> get_y2
...
```

Internally, we define this ordered map as list of tuples:

```{Python}
Idea([(do, get), 
      (do, get),
      ...])
```

The *do* ad *get* elements are modelled as simple dictionaries with numeric values.

```{Python}
Idea([({'peel': 1, 'time': 2, 'apple': 1}, {'peeled apple': 1}    ),
      ({'mash': 2, 'strawberry': 1},       {'strawberry jam': 0.2}),
      ...])
```

That is enough to define an idea (or rather, a simple linear plan). However, for a human, list of tuples of dictionaries is not necessarily the most convenient way. So, there is a method from_idl(), which tries to create the above-like variable (stored as self.plan) from the following kind of list:

```{Python}
Idea(r'''
add: peel 1, time 2, apple 1
get: peeled apple 1
add: mash 2, strawberry 1
get: strawberry jam 0.2
''')
```

In fact, we can use the words of any human language I/O, like the below. 

```{Python}
i = Idea(r'''
入: 剥离皮肤 1, time 2, 苹果 1
出: 苹果去皮 1
入: 捣碎 2, 草莓 1
出: 草莓酱 0.2
''')
```

Try the .to_df(), and to_df(dates=True).

```{Python}
i.to_df(dates=True)
```

## Multiple Scenarios

It is often the case that investables and deliverables of an idea cannot be described by a single number. We often have interval estimates rather than point estimates for a value. We start from the support of multiple scenarios.

For example, the expression { '草莓酱': [0.2, 0.3, 0.5] } will mean that

 * 0-th scenario is we get 0.2 strawberry jam
 * 1-th scenario is we get 0.3 strawberry jam
 * 2-th scenario is we get 0.5 strawberry jam

In the IDL, we use backslash to generate such a JSON internally: 

```
入: 剥离皮肤 1, time 2\5, 苹果 1
出: 苹果去皮 1
入: 捣碎 2, 草莓 1
出: 草莓酱 0.2\0.3\0.5
```

The reason why I chose the backslash, is that I will want to define formulas for distributions on intervals, and will want to use division sign (/), not limiting myself with countable number of scenarios, but for now, let's continue with the multiple scenario case.

The IDL input above generates the following data is encoded like this:

```{Python}
self.plan = [({'剥离皮肤': 1, 'time': [2, 5], '苹果': 1}, {'苹果去皮': 1}    ),
             ({'捣碎': 2, '草莓': 1},       {'草莓酱': [0.2, 0.3, 0.5]})])
```

There are multiple possible I/O scenarios, here, as an example, potentially needed amount of time is expressed as [2, 5].

## Valuation of Items

One way is to provide the value for each I/O item is by simple weighting. The initial assumption is that the weights for each item are equal to 1. However, if we are not okay with the default, we can pass specific using a dictionary with coinciding keys. For example, if the value of one peeled apple is 5, and value of one mashed strawberry is 7, then we can pass it using **ow** argument in the constructor, like this:

```{Python}
Idea(r'''
add: peel 1, time 2, apple 1
get: peeled apple 1
add: mash 2, strawberry 1
get: strawberry jam 0.2
''', ow={'peeled apple': 5, 'strawberry jam': 7}).to_df(dates=True)
```

If the weights are provided, the defaults of 1 for other items are automatically reset to 0.

It is also possible to include the weights for the input items the same way, by using **iw** argument. For example, assume that we value things in dollars, and apple costs 1$, and strawberry costs 0.1$. Then we could write:

```{Python}
Idea(r'''
add: peel 1, time 2, apple 1
get: peeled apple 1
add: mash 2, strawberry 1
get: strawberry jam 0.2
''', iw={'apple': 1, 'strawberry': 0.1},\
     ow={'peeled apple': 5, 'strawberry jam': 7}).to_df(dates=True)
```

Soon, it will be possible to define the values for the items at each step. We may use the at (@) sign for that. For example:

```
入: 剥离皮肤 1, time 2\5, 苹果 1, money 2 @ 1\1
出: 苹果去皮 1, money 1 @ 1
入: 捣碎 2, 草莓 1, money 2 @ 4,, 2\1
出: 草莓酱 0.2\0.3\0.5, money 4 @ 10
```

More info: [http://mindey.com/IdeaLib.html](http://mindey.com/IdeaLib.html)

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
* Clean up and generalize code to the degree that it is easily usable inside any app. (Primary focus: powerful expressive and easy IDL, a protocol, could be used by humans and computers.)
* Think of a more elegant way to resample generated dataframe by amounts of time specified.
* Possibility to pass probabilities along with the list of values, e.g., 50:.12\200:.48\400:.4
* Consider the possibility to branch into non-linear plan. (ie., STRIPS)
* Consider the possibility to interpolate multinomial distribution provided.
* Possibility to provide two value:probability pairs as probabilities as analytical functions, e.g., v:p(v), where v is value, and p is probability function, e.g., v1:p1(sqrt(v1))\v2:p2(v2)\v3:p3(v3).
* Make rational cumsum(), e.g., ``Idea.to_df(icumsum=True, ocumsum=True)``. By default we want to assume these to be True, because it is often so that we just think of the last change, yet we want to approximate result.
* There should be a way to add exception to cumsum in language from cumsuming, or decay time, or half-life or just any function defining the decay over time or over iterations or conditions satisfied for decay to by specific margin to occur. The distribution of margins and condition sets associated with margin, is the subject of decay-condition distribution.
* Once we have all ideas in a db, we could create the IdeaList.choice() method. This choice(deliverables) method would take ideas and, find ideas best suited to bring deliverables with smallest input/shortest time (imagine having the database of all ideas in an idea bank, and defining your goal criteria, by deliverables, to choose ideas to invest). Sure, we would want to have IdeaList.investables and IdeaList.deliverables attributes.
* Refactor scenario generation, or make a separate scenario generation class.
* Describe usage in documentation and good examples, may rename some variables.

