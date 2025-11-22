# Terminal-Screensaver
A set of programs to run from the terminal that display something interesting while idling in the background. The programs are all organized in a similar way. Each folder in the repository contains a main.py file, a helper_functions.py file, and the other files and folders required to run the program. To run any particular screensaver, navigate to the desired folder in the repository via the terminal and use the command `python main.py -h`

The arguments of all programs can be viewed by navigating to the location of the main.py script for that program and running `python main.py -h` in the command line.

### Game of Life
A Python program to run Conway's Game of Life on the terminal screen. It can also run 'Game of Life'-like simulations under arbitrary rulesets. To run alternate rulesets, use the command `python main.py --rule='B###/S###'`. As an example rule, B3/S23 means that cells are (B)orn if they have 3 living neighbors and (S)tay alive if they have 2 or 3 living neighbors.

### Wikipedia Random Walk
This python program performs a random walk through Wikipedia links, printing out the summary of each article it stops on. It starts by default with the article [Unusual Articles](https://en.wikipedia.org/wiki/Wikipedia:Unusual_articles), but that argument can be overridden. After the program has been ended, the list of articles toured by the random walk can be printed with `python main.py --display_prev_walk`.
