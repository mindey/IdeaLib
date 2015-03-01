# IdeaLib

I [need](http://www.halfbakery.com/idea/How_20to_20Analyze_20Ideas_20Quantitatively_3f) some way to estimate the i/o of ideas. I'll describe it later. Didn't sleep tonight. :)

The example below may be easier to understand, if you look at [IDL description](http://mindey.com/IdeaLib.html) my [blog post](http://blog.mindey.com/2014/12/07/comparing-two-ideas-simple-modelling-of-growth/).

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

```
Idea([(do, get), 
      (do, get),
      ...])
```

The *do* ad *get* elements are modelled as simple dictionaries with numeric values.

```
Idea([({'peel': 1, 'time': 2, 'apple': 1}, {'peeled apple': 1}    ),
      ({'mash': 2, 'strawberry': 1},       {'strawberry jam': 0.2}),
      ...])
```

That is enough to define an idea (or rather, a simple linear plan). However, for a human, list of tuples of dictionaries is not necessarily the most convenient way. So, there is a method from_idl(), which tries to create the above-like variable (stored as self.plan) from the following kind of list:

```
Idea(r'''
add: peel 1, time 2, apple 1
get: peeled apple 1
add: mash 2, strawberry 1
get: strawberry jam 0.2
''')
```

In fact, we can use the words of any human language I/O, like the below. 

```
i = Idea(r'''
入: 剥离皮肤 1, time 2, 苹果 1
出: 苹果去皮 1
入: 捣碎 2, 草莓 1
出: 草莓酱 0.2
''')
```

Try the .to_df(), and to_df(dates=True).

```
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

```
self.plan = [({'剥离皮肤': 1, 'time': [2, 5], '苹果': 1}, {'苹果去皮': 1}    ),
             ({'捣碎': 2, '草莓': 1},       {'草莓酱': [0.2, 0.3, 0.5]})])
```

There are multiple possible I/O scenarios, here, as an example, potentially needed amount of time is expressed as [2, 5].

## Valuation of Items

One way is to provide the value for each I/O item is by simple weighting. The initial assumption is that the weights for each item are equal to 1. However, if we are not okay with the default, we can pass specific using a dictionary with coinciding keys. For example, if the value of one peeled apple is 5, and value of one mashed strawberry is 7, then we can pass it using **ow** argument in the constructor, like this:

```
Idea(r'''
add: peel 1, time 2, apple 1
get: peeled apple 1
add: mash 2, strawberry 1
get: strawberry jam 0.2
''', ow={'peeled apple': 5, 'strawberry jam': 7}).to_df(dates=True)
```

If the weights are provided, the defaults of 1 for other items are automatically reset to 0.

It is also possible to include the weights for the input items the same way, by using **iw** argument. For example, assume that we value things in dollars, and apple costs 1$, and strawberry costs 0.1$. Then we could write:

```
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




