# bin-packing

A Python implementation of the running process for a 2D greedy two-level search algorithm for the 2D rectangular packing problem. Implemented following the process outlined in Chen and Huang (2007) (see sources).  

The rectangles are placed into the container one by one and each rectangle is packed at a position by a corner-occupying action so that it touches at least two items without overlapping other already packed rectangles. At the first level of the algorithm, a simple algorithm called A0 selects and packs one rectangle according to the highest degree first rule at every iteration of packing. At the second level, A0 is itself used to evaluate the benefit of a CCOA more globally.  

The algorithm is implemented in python using matplotlib for visualization where the running time has been slowed for the sake of recording.

**Sources**  
https://www.sciencedirect.com/science/article/abs/pii/S0360835207000678?via%3Dihub
https://www.sciencedirect.com/science/article/abs/pii/S0377221799003574?via%3Dihub
https://en.wikipedia.org/wiki/Bin_packing_problem

**Demo**  
![Skærmoptagelse-2022-06-01-kl -01 40 50](https://user-images.githubusercontent.com/72623007/171301493-75ba9711-9515-48f2-bae2-872a45a6aae2.gif)

**Explaination**  
In the right pane is an overview of all the rectangles that are to be packed. The rectangles colored in blue are the boxes that have not yet been packed, and the ones colored grey have already been packed into the left pane.
The left pane is the packing area, where the goal is to fit in as many of the boxes from the right pane as possible. The algorithm is said to converge successfully if all the boxes are packed in the left pane with no gaps. The rectangles in blue are the packed rects, and the ones in grey represent all possible positions for the next move. Red crosses are the point at which the origins can be placed.
