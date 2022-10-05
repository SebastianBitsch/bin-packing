
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

    def __repr__(self) -> str:
        return f"Rect(size: {self.w, self.h}, fit: {self.fit})"


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



class Packer():

    def __init__(self,x,y) -> None:
        # self.root = None
        self.root = Node((0,0), (x, y))


    def fit(self, rects:list[Rect]) -> None:
        # self.root = Node((0,0), (rects[0].w, rects[0].h))

        for rect in rects:
            node = self.find_node(self.root, rect.w, rect.h)
            if node:
                rect.fit = self.split_node(node, rect.w, rect.h)

        for r in rects:
            print(r)


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


import matplotlib.pyplot as plt

def plot():
    pass

if __name__ == "__main__":
    dims = [
        (500,200),
        (250,200),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50),
        (50,50)
    ]
    dims = sort(dims, sort_attr="asd")

    rects = [Rect(d) for d in dims]
    p = Packer(500,500)
    p.fit(rects)


