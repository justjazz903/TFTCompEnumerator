# TFTCompEnumerator
Extract TFT comps by your grading strategies. This enumerator iterates through all possible comps in TFT and gives each comp a score by the grading strategy defined in `namespace.graph.grader` and extract those comps with the highest score. The project is written in pure python. This doc is for TFT set 5.5.

## Dependencies

`numpy`

`math`

`copy`

`itertools`

`json`

`pickle`

`networkx`

`os`

`concurrent`

`shutil`

`sys`

Make sure you have all the above packages installed before running the code. Most of the packages are pre-installed with python, the only two things that might need manual installation are `numpy` and `itertools`.

## How To Use

To simply put, open a terminal and go to the directory `./TFTCompEnumerator/`, then run the following command:

`python graph_constructor.py`

Wait till the running is over and results will be in `./graph/` folder. The pickle file is a networkx graph object for coding use and the graphml file is for visualization in graph related software like Cytoscape. I have already provided the results of the two grading strategies I came up with. You can try tuning the parameters in `graph_constructor.py` or you can try your own grading strategies. I will explain them later.

**Note:** The running time for the script takes long. The project uses multi-processing computation, a full enumeration with full CPU computation power from level 5 comps through level 9 comps on a 6-core Intel i5-9500 3GHz CPU  takes roughly **48 hours**. Remember to close all other unnecessary processes before running the script. You need about **80GB** free hard drive space (depends on the scale of comps you enumerate) to run the code, but the project won't takes that much space because it is only  caching some data to the hard drive during the run time and then delete them later. So if you run into some permission error, it's probably because of saving and deleting data from the hard drive. Chang your directory's permission accordingly.

## Data Representation

To custom your own grading strategies, you need to know how the data are represented.

### Champions and Traits

Raw-human-readable data are saved in `TFTDataSet.json` file. Formatted like this:

```json
{
   "champions":[
      {
         "name":"aatrox",
         "cost":1,
         "traits":[
            "redeemed",
            "legionnaire"
         ]
      },
      ...
   ],
   "traits":[
      {
         "name":"abomination",
         "level":[
            3,
            4,
            5
         ],
         "champions":4
      },
      ...
   ]
}
```

I then use the `get_data_matrix()` method in `namespace.graph.json_processor` to convert the json data into matrices. I won't bother you with matrix operations. The thing to remember here is that both champions and traits are stored in array(list) and I use the **index number** in the array to refer to each champion and trait.

### Comp

Let's consider this comp `['garen', 'gragas', 'hecarim', 'heimerdinger', 'ivern', 'kled', 'sejuani', 'teemo', 'thresh']`. One of the numerical way to represent this comp is to use the **index number** I mentioned earlier: `[9, 10, 12, 13, 15, 22, 39, 44, 45]` which I refer to as the variable name `comp_id` in the project. However, for the massive number of comps, a list of integers will takes up too much memories. So comp has another representation called `bit_code` for memory saving purpose. Here, a `bit_code` is a 64-bit integer. Since there are only 57 champions in the current set 5.5, I use bit representation to put a comp into a 64-bit integer. As in the i-th bit of the `bit_code` will be set to 1 if the champion with the i-th index is presented in the comp. The `bit_code` for our example in the binary format will be:

`0b 00000000 00000000 00110000 10000000 00000000 01000000 10110110 00000000`

The 9-th(garen), 10-th(gragas), 12-th(hecarim)... bits are set to 1 and the rest are zeroes. In decimal is 53326318188032.

Methods are provided in `namespace.graph.coder` to translate between different representations of comp.

### Trait

Traits of a comp is a bit more tricky since we not only need to count the traits of each champion in the comp but we also need to determine how many traits are actually activated.

Again, to customize your own grading strategy, you only need to know how the traits of a comp is represented, so I won't bother you with the details.

Let's take a look at our old example `['garen', 'gragas', 'hecarim', 'heimerdinger', 'ivern', 'kled', 'sejuani', 'teemo', 'thresh']`. The activated traits for this example is `['brawler: 2', 'caretaker: 1', 'cavalier: 3', 'cruel: 1', 'dawnbringer: 2', 'forgotten: 2', 'hellion: 2', 'invoker: 2', 'knight: 2', 'renewer: 2', 'victorious: 1']`. We already know that we can use the index to represent each trait, such as 2 for brawler, 4 for caretaker. 

But how do we represent the trait's "level"? Through out all sets in TFT game play, the trait's "level" are determined by the number of present champions with the same trait. In set 5.5, take "dawnbringer" trait as an example, it has **4 levels**: [2, 4, 6, 8], we will see what level means by this. If we have **2 or 3 champions** with the "dawnbringer" trait, then we have a **level 1**  "dawnbringer" trait activated. If we have **4 or 5 champions** with the "dawnbringer" trait, then we have a **level 2** "dawnbringer" trait activated. If we have **8 or more champions** with the "dawnbringer" trait, then we have a **level 4** "dawnbringer" trait activated. It is important that we distinguish "trait level" from the number of champions.

In our example, the numerical way to represent the traits of our comp is: `[0 0 1 0 1 2 1 1 0 1 1 0 1 0 1 0 0 0 0 0 1 0 0 1 0 0]`. The dimension of this matrix is (26 * 1) because there is a total of 26 traits in current set 5.5. Each element represent the trait level of that trait. The third element 1 means that we have a **level 1 brawler** trait activated.

To summarize our example:

| comp                 | ['garen', 'gragas', 'hecarim', 'heimerdinger', 'ivern', 'kled', 'sejuani', 'teemo', 'thresh'] |
| -------------------- | ------------------------------------------------------------ |
| **trait**            | **['brawler: 2', 'caretaker: 1', 'cavalier: 3', 'cruel: 1', 'dawnbringer: 2', 'forgotten: 2', 'hellion: 2', 'invoker: 2', 'knight: 2', 'renewer: 2', 'victorious: 1']** |
| **comp_id**          | **[9, 10, 12, 13, 15, 22, 39, 44, 45]**                      |
| **bit_code**         | **53326318188032**                                           |
| **trait(numerical)** | **[0 0 1 0 1 2 1 1 0 1 1 0 1 0 1 0 0 0 0 0 1 0 0 1 0 0]**    |

### champion_matrix

There are 57 champions and 26 traits in set 5.5. The champion_matrix is a (57 * 27) matrix with each of its row represents a champion. The first 26 elements represents the traits of the champion in the way that if the i-th element is 1 means the champion has the trait with index i as its trait. The last element denotes the cost of the champion. The champion_matrix looks like this:
$$
\left(\begin{array}{cc}
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 1\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 5\\
& & & & & & & & & & & & & .\\
& & & & & & & & & & & & & .\\
& & & & & & & & & & & & & .\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 3
\end{array}\right)
$$
Take the 0-th trait (first row, we use 0-indexing all the way) as an example which represents the champion Aatrox . Its cost is 1 so the last element is 1. Aatrox has redeemed and legionnaire as its traits so the 15-th and 19-th elements are set to 1.

### trait_matrix

The trait_matrix is a (26 * 10) matrix with each of its row represents a trait. The i-th element of the 10 elements in each row will be set to 1 if exactly i champions can activate some level of the current trait, otherwise 0. The trait_matrix looks like this:
$$
\left(\begin{array}{cc}
0 & 0 & 0 & 1 & 1 & 1 & 0 & 0 & 0 & 0\\
0 & 0 & 1 & 0 & 1 & 0 & 1 & 0 & 0 & 0\\
& & & & & .\\
& & & & & .\\
& & & & & .\\
0 & 0 & 1 & 0 & 1 & 0 & 1 & 0 & 0 & 0
\end{array}\right)
$$
Take the 0-th trait (first row) as an example, which represents the abomination trait, and abomination has a structure of [3, 4, 5], so the third, forth and fifth element are 1 and others are 0. For convenience, the 0-th column(first element) of all traits are 0, because 0 champion can not activate anything.

### trait_number_matrix

The trait_number_matrix is a (26 * 5) matrix with each of its row represents a trait. The i-th element of the 5 elements in each row represents the exact number of champions needed to activate the i-th level of the current trait. The trait_number_matrix looks like this:
$$
\left(\begin{array}{cc}
0 & 3 & 4 & 5 & 0\\
0 & 2 & 4 & 6 & 0\\
& & .\\
& & .\\
& & .\\
0 & 2 & 4 & 6 & 0
\end{array}\right)
$$
Take the 0-th trait(first row) as an example, which represents the abomination trait, and abomination has 3 levels and can be activated at [3, 4, 5], so the second element (level 1) being  3 means that it takes exact 3 champions with abomination trait to activate a level 1 abomination trait for the comp. For convenience, the 0-th column(first element) of all traits are 0, because a level 0 trait has no meaning.

## Grading Strategy

For starters, the simplest strategy might be just use the sum of the comp's trait vector as a score, so that comps with more activated traits get higher scores. Or we can take the comp's cost into consideration, which is not hard to compute. The only limit is imagination.

You should write your grading method in `./namespace/graph/grader.py`. The method should return a single number as the score for the comp. You can find two methods `simple_strategy` and `poker_strategy` in that file, they are for the same grading purpose, use them as examples.

 The arguments passed to the method depends on your strategy. Once you finish your grading method, you will need to write the method to call inside each process. Remember, your grading strategy only grade a single comp for one call and we need to grade all possible comps. So we will need to write a method to call your grading method repeatedly for all comps. Also, since I'm using multi-processing to accelerate the computation, we will need another method to handle the multi-processing task distribution. Don't worry, you only need to do a little alter to the origin code.

Suppose you have already written your grading strategy inside `./namespace/graph/grader.py`:

```python
def my_strategy(*args, **kwargs):
	...
	return score
```

Then you will write another method also inside `./namespace/graph/grader.py`, this method will be passed as a callback function to the multi-processing method:

```python
def my_grader(combination_generator, include, trait_number_matrix, champion_matrix, trait_matrix, batch_index, total_batch):
    scores = dict()
    for c in combination_generator:
        comp_id = list(c) + include
        trait, _ = get_comp_matrix(comp_id, champion_matrix, trait_matrix)
        bit_code = comp_id_to_bit_code(comp_id)
        # you only need to change this following line
        score = my_strategy(*args, **kwargs)
        # -------------------------------------------
        try:
            scores[score].append(bit_code)
        except:
            scores[score] = [bit_code]
    print(f'batch {batch_index} / {total_batch} graded')
    return scores
```

You can copy the whole function, and only change the `socre = ...` line to get the score by your strategy. But don't forget to also change the function's signature according to your grading method if you decide to pass some extra arguments to your grading method.

After this, you will need to go the `./namespace/graph/grade.py` file to write a method to handle multi-processing.

```python
...
from namespace.graph.grader import my_grader
...

def my_grade(trait_number_matrix, base, champion_matrix, trait_matrix, level, reduced_size, max_workers):
    all_comp_id = list()
    reduce_combination([i for i in range(champion_matrix.shape[0])], level, [], reduced_size, all_comp_id)
    scores = dict()
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        batch_index = 1
        fs = dict()
        for item in all_comp_id:
            # you only need to change the following part
            fs[executor.submit(
                my_grader,
                item[0],
                item[1],
                trait_number_matrix,
                champion_matrix,
                trait_matrix,
                batch_index,
                len(all_comp_id)
            )] = None
            # -------------------------------------------
            batch_index += 1
        count = 1
        for f in concurrent.futures.as_completed(fs):
            cur_scores = f.result()
            merge_dict(scores, cur_scores)
            if get_scores_size(scores) >= 64 * 1024 ** 2:
                with open(CONSTANT['PATH']['GRADE'] + f'scores_{count}.pickle', 'wb') as file:
                    pickle.dump(scores, file)
                scores = dict()
                count += 1
            del fs[f]
        if len(scores.keys()) > 0:
            with open(CONSTANT['PATH']['GRADE'] + f'scores_{count}.pickle', 'wb') as file:
                pickle.dump(scores, file)
```

Again, you can copy the whole function and only change the `f[executor.submit(...)]=None` part. The first argument of `executor.submit()` is the callback function which we just write above. The following arguments are just in the order of the callback function's arguments, which you will alter according to your case. Still, don't forget to also change this function's signature accordingly like earlier.

Finally, you can just call this function inside `./graph_constructor.py`:

```python
...
from namespace.graph.grade import my_grade
...

if __name__ == '__main__':
	...
    for level in levels:
        init_path()
        # only change this following line
        my_grade(trait_number_matrix, champion_matrix, trait_matrix, level, reduced_size, max_workers)
        # -------------------------------
        extract(level, champion_matrix, trait_matrix, max_workers)
    	connect(max_diff, champion_matrix.shape[0])

```

Don't forget the importing step and now you are ready to run and test your strategy!

## Parameters

There are some parameters your can tune in the `./graph_constructor.py`, they are `levels, max_diff, max_workers, reduced_size`.

This is where I should explain why it is called the "graph constructor". In real game play, forming a strong comp needs transitional comps. In my mind, this process should be like a tree structure. Each champion is like a node, players travel through branches to find that final leaf node where all the champions along the path finally form a powerful comp. For a single strong comp, the transition process to it may looks like a tree, but for a whole bunch of strong comps, then the transition process will then be like a graph. Each comp may has intertwine relationships with each other, players won't know which final comp they will end up with. It will then become a optimal decision making problem based on game states and the graph we get.

Parameter `levels` is a list, [5, 6, 7, 8, 9] indicates that we will iterate through all possible comps for level 5, 6, 7, 8, 9 which means all possible comps with 5 champions, 6 champions... etc. As mention in the beginning, a full run through level 5 to level9 takes 48 hours on a 6 core Intel CPU. Adjusting `levels` will significantly affecting the running time.

Parameter `max_diff` is a list, its length should be `len(levels) - 1`, for a `levels=[5,6,7,8,9]`, let's say we use `max_diff=[2,2,2,3]`. When we finish all the grading, we are left with a huge amount of data, To find a transition graph among them, we have many approaches, here I'll explained my. I first connect level 5 comps with level 6 comps with a **maximum champion difference** of `max_diff[0]` (maximum 2 different champions for each pair of level 5 and level6 comp), then I connect level 6 comps with level 7 comps with a **maximum champion difference** of `max_diff[1]`, then I connect level 7 comps with level 8 comps with a **maximum champion difference** of `max_diff[2]` and so on. That is why the length of `max_diff` should be `len(levels) - 1`. 

Parameter `max_workers` is just to specify how many CPU cores you want to use for multi-processing, `None` means using all the CPU cores.

Parameter `reduced_size` means how many comps should be assigned for a single process. You can tune it depends on your computer's memories.

Other parameters that are not mentioned here are just for grading strategies.

## Results

Up till now, we never talked about how to extract comps after we gave all the comps scores. There are also many approaches to this, we can choose the top n comps for each level or we can keep picking by the score from the high to low until we have all champions being included in our choices. Here I use the later extracting strategy for a more general result.

The result is returned as a `networkx` directed graph object where each node is a comp represented by `bit_code`  and has a property of the comp's level. In Cytoscape it looks like this:

![alt text](https://github.com/justjazz903/TFTCompEnumerator/blob/main/img/graph.png "graph")

I provide some code in the `TestNotebook.ipynb` to divide the whole graph to individual transition tree and change the node from `bit_code` to readable strings.

![alt text](https://github.com/justjazz903/TFTCompEnumerator/blob/main/img/transition.png "graph")

`networkx` and Cytoscape both provides lots of graph analysis tools. You can analyze your result accordingly.

I write a `print_comp()` method in `./namespace/graph/comp_printer.py` to help print comp information directly from `bit_code`. Use it in Jupyter Notebook like this:

```python
from namespace.graph.json_processor import get_data_matrix
from namespace.graph.comp_printer import print_comp

champion_matrix, trait_matrix, _ = get_data_matrix()
bit_code = 53326318188032
champ_names, trait_names, cost = print_comp(bit_code, champion_matrix, trait_matrix)
print(champ_names)
print(trait_names)
print(cost)
# output
# ['garen', 'gragas', 'hecarim', 'heimerdinger', 'ivern', 'kled', 'sejuani', 'teemo', 'thresh']
# ['brawler: 2', 'caretaker: 1', 'cavalier: 3', 'cruel: 1', 'dawnbringer: 2', 'forgotten: 2', 'hellion: 2', # 'invoker: 2', 'knight: 2', 'renewer: 2', 'victorious: 1']
# 3.0
```

## Afterword

Ever since the TFT game was created, I've been trying to use coding to find interesting comps. However there are 1,652,411,475 possible combinations for a 8 champions comp (choose 8 from 57), let alone level 9 comps. The computation are too expensive and my coding skills are too weak. Now with multi-processing ,some mathematical theory and numpy's amazing matrix broadcasting, I am able to pull this off. Imagine to enumerate through level 5 till level9, that is:
$$
4,187,106 + 36,288,252 + 264,385,836 + 1,652,411,475 + 8,996,462,475 = 10,953,735,144
$$
Almost 11 billion comps get graded in 48 hours on a regular laptop and no GPU acceleration!

The results I got from my grading strategy looks interesting but are not very practical. Most of them are just like the example, our example has 11 traits activated while it is not very strong in real game play.

My dream is to build an AI player to play TFT like the Alpha Go project and I started this project that way. I did not started with reinforcement learning because I did not want to get too involved with the math and theories. So I started with simple enumeration and grading. Now 6 months later, here I am reading the reinforcement learning textbook and find it's fascinating. Those math and theories are truly magical and make my dream looking more and more realistic. Now I think about it, the graph is actually just a part of the Markov Decision Process.

I even write a computer vision module for this project with `pyautogui` and `opencv`, along the way I ran into `imagehash` and `fastai` which are also very amazing. But I did not get to finished it because I got exhausted by the image recognizing process, comparing different algorithms, machine learning approaches and mathematical approaches. Not to mention building a training image set and labeling it manually for my neural network. Although deep down I know that using `cv2.matchTemplate()` might be just enough. Guess I'm somewhat compulsive.

I'm learning reinforcement learning for now so no more coding for a while (although I still use coding to do some of examples in the book). I'm open for discussion with people who share this same little interest. 

Contact me at justjazz903@gmail.com

Thank you for reading!

