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

# Introduction to Idea Definition Language (IDL)

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

In fact, we can use the words of any language I / O, like the below. 

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

However, a language can have other usefulness. In order to define several possible values, in the native data structure we use lists as values of dictionaries. 

## Expressing different possible I / O scenarios
For example, the expression { '草莓酱': [0.2, 0.3, 0.5] } means that

 * 0-th scenario is we get 0.2 strawberry jam
 * 1-th scenario is we get 0.3 strawberry jam
 * 2-th scenario is we get 0.5 strawberry jam

Inside the IDL, this is defined as follows: 

```
入: 剥离皮肤 1, time 2\5, 苹果 1
出: 苹果去皮 1
入: 捣碎 2, 草莓 1
出: 草莓酱 0.2\0.3\0.5
```
Each of the values in such a list define a possible scenario. The data is encoded like this:

```
self.plan = [({'剥离皮肤': 1, 'time': [2, 5], '苹果': 1}, {'苹果去皮': 1}    ),
             ({'捣碎': 2, '草莓': 1},       {'草莓酱': [0.2, 0.3, 0.5]})])
```

There are multiple possible I/O scenarios, here, as an example, potentially needed amount of time is expressed as [2, 5].

## Expressing values of things

One way is to provide the value for each I/O item. The initial assumption is that the values of each item are equal to 1. However, if the actual values are not all equal to 1, we can pass their values once we know the column names, like, say if value of one peeled apple is 5, and value of one mashed strawberry is 7, then we can pass it like this:

```
Idea(r'''
add: peel 1, time 2, apple 1
get: peeled apple 1
add: mash 2, strawberry 1
get: strawberry jam 0.2
''', ow={'peeled apple': 5, 'strawberry jam': 7}).to_df(dates=True)
```

If the weights are provided, the defaults of 1 for other items are automatically reset to zero, and only the objects with value are considered.

It is also possible to include the weights for the input items the same way. For example, assume that we value things in dollars,, and apple costs 1$, and strawberry costs 0.1$. Then we could write:

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




