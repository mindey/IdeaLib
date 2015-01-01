# IdeaLib

I need some way to estimate the i/o of ideas. I'll describe it later. Didn't sleep tonight. :)

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
get: peeled_apple 1
add: mash 2, strawberry 1
get: strawberry_jam 0.2
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
i.to_df(dates=True,value=True)
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
(not yet working, use native format for now)

Each of the values in such a list define a possible scenario. The data is encoded like this:

```
self.plan = [({'剥离皮肤': 1, 'time': [2, 5], '苹果': 1}, {'苹果去皮': 1}    ),
             ({'捣碎': 2, '草莓': 1},       {'草莓酱': [0.2, 0.3, 0.5]})])
```

There are multiple possible I/O scenarios, here, as an example, potentially needed amount of time is expressed as [2, 5].

## Expressing values of things

One way is to include the money attribute at each step, which summarizes the value of the obtained items.

```
入: 剥离皮肤 1, time 2\5, 苹果 1, money 2
出: 苹果去皮 1, money 1
入: 捣碎 2, 草莓 1, money 2
出: 草莓酱 0.2\0.3\0.5, money 4
```

Another way is to provide the value for each time. The initial assumption is that the values of each item are equal to 1. However, if values are not all equal to 1, we can pass their values once we know the column names, like, say if value of one peeled apple is 5, and value of one mashed strawberry is 7, then we can pass it like this:

```
i.to_df().columns #苹果去皮, 草莓酱
i.to_df(value=[5, 7])
```

Instead of writing like this, we can give the values of things immediately in the IDL:

```
入: 剥离皮肤 1, time 2\5, 苹果 1, money 2 @ 1\1
出: 苹果去皮 1, money 1 @ 1
入: 捣碎 2, 草莓 1, money 2 @ 4,, 2\1
出: 草莓酱 0.2\0.3\0.5, money 4 @ 10
```

More info: 




