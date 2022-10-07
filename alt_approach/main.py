import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sort_types = {"width":0, "height":1, "max":2, "area":3, "w":0, "h":0, "a":3}    


def sort(rects:list[tuple], sort_attr:str='width') -> list[tuple]:
    """ Function for sorting a list of rects using a given sorting method """

    # Add attributes to the rects to use for sorting parameters; r = (w,h,max(w,h),w*h)
    attr = [r + (max(r), r[0]*r[1]) for r in rects]
    
    # Get the index of the inputted sorting type, if invalid width is used (0=width)
    sort_attr_index:int = sort_types.get(sort_attr, 0)

    # Sort attributes and return only the original rect dims
    attr.sort(key=lambda x: x[sort_attr_index], reverse=True)
    return [x[:2] for x in attr]



class Rect():
    def __init__(self, size:tuple) -> None:
        assert len(size) == 2
        self.w, self.h = size
        self.fit = None
        self.inbounds = True

    def __repr__(self) -> str:
        return f"Rect(size: {self.w, self.h}, fit: {self.fit}, in bounds: {self.inbounds})"


def plot(size: tuple, rects:list[Rect]) -> None:
    _, ax = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
    background = Rectangle((0,0), 20, 20, fc='grey',ec='black',alpha=0.2)
    ax.add_patch(background)
    ax.set_xlim([0,size[0]])
    ax.set_ylim([0,size[1]])

    for r in rects:
        # Only plot if the rect has been fit
        if not r.fit:
            return
        draw_rect(ax, r)

    plt.show()

def draw_rect(ax, rect: Rect) -> None:
    box = Rectangle(rect.fit.origin, rect.w, rect.h, fc='lightblue',ec='black',alpha=1.0)
    ax.add_patch(box)


class Node():

    def __init__(self, origin:tuple, size:tuple) -> None:
        assert len(size) == 2

        self.used = False
        
        self.down = None
        self.right = None

        self.origin = origin
        
        self.x, self.y = origin
        self.w, self.h = size

    def __repr__(self) -> str:
        return f"Node(size: {self.w, self.h}, origin: {self.origin})"



# class SimplePacker():

#     def __init__(self,x,y) -> None:
#         # self.root = None
#         self.root = Node((0,0), (x, y))

#     def set_size(self, w:int,h:int) -> None:
#         self.root = Node((0,0), (w,h))

#     def fit(self, rects:list[Rect]) -> None:

#         for rect in rects:
#             node = self.find_node(self.root, rect.w, rect.h)
#             if node:
#                 rect.fit = self.split_node(node, rect.w, rect.h)
  
#         plot((rects[0].fit.w, rects[0].fit.h), rects)


#     def find_node(self, node:Node, w:int, h:int) -> Node:
#         if node.used:
#             return self.find_node(node.right, w, h) or self.find_node(node.down, w, h)
#         elif w <= node.w and h <= node.h:
#             return node
#         else:
#             return None


#     def split_node(self, node:Node, w:int, h:int) -> Node:
#         node.used = True
#         node.down = Node(origin=(node.x, node.y + h), size=(node.w, node.h - h))
#         node.right = Node(origin=(node.x + w, node.y), size=(node.w - w, h))
#         return node


class AdvancedPacker():

    def __init__(self,x,y) -> None:
        self.root = Node((0,0), (x, y))
        self.bounds = (x,y)
    

    def increment_size(self, amount:int = 1) -> None:
        """ Increment the size of the bounds by +1 in both directions"""
        self.root = Node((0,0), (self.root.w + amount, self.root.h + amount))
        self.bounds = (self.bounds[0] + amount, self.bounds[1] + amount)


    def n_inbound(self) -> int:
        """ Get the number of rects that are inbound"""
        return sum([r.inbounds for r in self.rects])


    def filled_pct(self) -> float:
        """ Get the percentage of the total area that is filled"""
        filled_area = sum([r.w*r.h for r in self.rects if r.inbounds])
        total_area = self.bounds[0]*self.bounds[1]
        return filled_area / float(total_area)


    def fit(self, rects:list[Rect]) -> None:

        for rect in rects:
            node = self.find_node(self.root, rect.w, rect.h)
            if node:
                rect.fit = self.split_node(node, rect.w, rect.h)
            else:
                rect.fit = self.grow_node(rect.w, rect.h)

            # Set inbound variable for each rect
            rect.inbounds = False if self.root.x+self.bounds[0] <= rect.fit.x or self.root.y+self.bounds[1] <= rect.fit.y else True

        self.rects = rects
        return self.rects


    def grow_node(self, w:int, h:int):
        can_grow_down = w <= self.root.w
        can_grow_right = w <= self.root.h

        should_grow_right = can_grow_right and (self.root.w + w <= self.root.h)
        should_grow_down = can_grow_down   and (self.root.h + h <= self.root.w)
        
        if should_grow_right:
            return self.grow_right(w,h)
        elif should_grow_down:
            return self.grow_down(w,h)
        elif can_grow_right:
            return self.grow_right(w,h)
        elif can_grow_down:
            return self.grow_down(w,h)
        else:
            return None


    def grow_down(self, w:int, h:int):
        new_root = Node((0,0), (self.root.w, self.root.h + h))
        new_root.used = True
        new_root.down = Node((0, self.root.h), (self.root.w, h))
        new_root.right = self.root

        self.root = new_root

        node = self.find_node(self.root, w, h)
        if node:
            return self.split_node(node, w, h)
        else:
            return None

    def grow_right(self, w:int, h:int):
        new_root = Node((0,0), (self.root.w + w, self.root.h))
        new_root.used = True
        new_root.down = self.root
        new_root.right = Node((self.root.w, 0), (w, self.root.h))

        self.root = new_root

        node = self.find_node(self.root, w, h)
        if node:
            return self.split_node(node, w, h)
        else:
            return None

    def find_node(self, node:Node, w:int, h:int) -> Node:
        if node.used:
            return self.find_node(node.right, w, h) or self.find_node(node.down, w, h)
        elif w <= node.w and h <= node.h:
            return node
        else:
            return None


    def split_node(self, node:Node, w:int, h:int) -> Node:
        node.used = True
        node.down = Node(origin=(node.x, node.y + h), size=(node.w, node.h - h))
        node.right = Node(origin=(node.x + w, node.y), size=(node.w - w, h))
        return node




if __name__ == "__main__":
    dims = [
        (4,14),
        (5,2),
        (2,2),
        (9,7),
        (5,5),
        (2,5),
        (7,7),
        (3,5),
        (6,5),
        (3,2),
        (6,2),
        (4,6),
        (6,3),
        (10,3),
        (6,3),
        (6,3),
        (10,3)
    ]
    # dims = [
    #     (2,12),
    #     (7,12),
    #     (8,6),
    #     (3,6),
    #     (3,5),
    #     (5,5),
    #     (3,12),
    #     (3,7),
    #     (5,7),
    #     (2,6),
    #     (3,2),
    #     (4,2),
    #     (3,4),
    #     (4,4),
    #     (9,2),
    #     (11,2)
    # ]
    # dims = [
    #     (500,200),
    #     (250,200),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (50,50),
    #     (150,50),
    #     (150,50),
    #     (200,200)
    # ]
    dims = sort(dims, sort_attr="max")

    rects = [Rect(d) for d in dims]
    # p = SimplePacker(20, 20)

    size = (20, 20)
    p = AdvancedPacker(*size)
    rects = p.fit(rects)
    for r in rects:
        print(r)
    plot((50, 50), rects)

