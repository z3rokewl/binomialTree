import math


trinomial = False

class BNode:
    def __init__(self):
        self.parent = None
        self.children = []
        self.price = 0

    def initialize(self, parent, price):
        self.parent = parent
        self.price = price

    def add_child(self, child):
        self.children.append(child)

class BiTree:
    def __init__(self, price):
        self.price = price
        self.head = self.first_node(price)
        self.sigma = 0.005303
        price_move_list = calc_price_move(self.sigma)
        self.gen_children([self.head], price_move_list, 0)

    def printer_helper(self, list_of_nodes):
        if list_of_nodes == []:
            return
        new_list = []
        for child in list_of_nodes:
            print child.price, 
            if child.children != []:
                new_list.extend(child.children)
        print
        self.printer_helper(new_list)

    def printer(self):
        print self.head.price
        self.printer_helper(self.head.children)

    def apply_to_all_nodes_price(self, fn):
        list_of_children = []
        list_of_children.append(self.head)
        while len(list_of_children) > 0:
            list_of_children[0].price = fn(list_of_children[0].price)
            list_of_children.extend(list_of_children[0].children)
            list_of_children = list_of_children[1:]

    def gen_children(self, bnode_list, price_move_list, count):
        first = 0
        next_list = []
        for new_head in bnode_list:
            if first == 0:
                self.add_children(price_move_list, new_head)
                first += 1
            else:
                self.add_children(price_move_list[1:], new_head)
            next_list.extend(new_head.children)
        count += 1
        # if count < 16:
        if count < 10:
            self.gen_children(next_list, price_move_list, count)

    def first_node(self, price):
        parent_node = BNode()
        parent_node.initialize(None, price)
        return parent_node

    def add_children(self, price_move_list, parent):
        if trinomial == True:
            self.add_children_trinomial(price_move_list, parent)
            return 
        else:
            for price_move in price_move_list:
                child = BNode()
                child_price = round(parent.price * price_move, 5)
                child.initialize(parent, child_price)
                parent.add_child(child) 

    def add_children_trinomial(self, price_move_list, parent):
        count = 0
        for price_move in price_move_list:
            child = BNode()
            child_price = round(parent.price * price_move, 5)
            child.initialize(parent, child_price)
            parent.add_child(child) 
            if count == 0:
                child = BNode()
                child_price = parent.price
                child.initialize(parent, child_price)
                parent.add_child(child)
                count += 1



# This function is meant to calculate u and d based on sigma. 
# The formula should be: u = move_up = e^(sigma*sqrt(T/n)) where T is the 
# total time (lets say in days) and n is the number of steps. 
# If we were only taking 2 steps in the tree over a 1 day period, u = move_up
# = e^(sigma*sqrt(1/2))
# but the quants are using the approximation below. 

def calc_price_move(sigma):
    move_up = (1 + sigma)
    move_down = (1 - sigma)
    return [move_down, move_up]

def main():
    tree = BiTree(100)
    head_list = [tree.head]
    tree.printer()
    def dumb(price, k=20):
        return  price - k
    tree.apply_to_all_nodes_price(dumb)
    tree.printer()

if __name__ == "__main__":
    main()
