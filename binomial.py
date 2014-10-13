import math

TOTAL_TIME = 10
NUM_STEPS = 10

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
    def __init__(self, price, sigma):
        self.price = price
        self.head = self.first_node(price)
        self.sigma = sigma
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

    def get_impotent_children(self, nodes):
        impotence_list = []
        for node in nodes:
            if node.children == []:
                impotence_list.append(node)
            else:
                impotence_list.extend(self.get_impotent_children(node.children))
        return impotence_list



    def apply_to_youngest_children(self, fn):
        list_of_children = []


    def apply_to_all_nodes_price(self, fn):
        list_of_children = []
        list_of_children.append(self.head)
        while len(list_of_children) > 0:
            list_of_children[0].price = fn(list_of_children[0].price)
            list_of_children.extend(list_of_children[0].children)
            list_of_children = list_of_children[1:]


    # TODO: this function needs some cleenup
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
        if count < 10:
            self.gen_children(next_list, price_move_list, count)

    def first_node(self, price):
        parent_node = BNode()
        parent_node.initialize(None, price)
        return parent_node

    def add_children(self, price_move_list, parent):
        for price_move in price_move_list:
            child = BNode()
            child_price = round(parent.price * price_move, 5)
            child.initialize(parent, child_price)
            parent.add_child(child) 

# p = interest_rate - move_down / (move_up - move_down)
# if we are including dividend yield, we use interest_rate = 
# (interest_rate / div_yield)
def binomial_method(list_of_values, p, interest_rate):
    new_list = []
    for i in range(len(list_of_values) - 1):
        new_value = (p * list_of_values[i+1] + (1.0 - p) * list_of_values[i]) / interest_rate
        new_list.append(new_value)
    return new_list


def calc_price_move(sigma):
    move_up = math.exp(sigma * math.sqrt(TOTAL_TIME / NUM_STEPS))
    move_down = 1.0 / move_up
    return [move_down, move_up]

def main():
    sigma = 0.005303
    initial_price = 100.0
    strike = 20.0
    interest_rate = 1.01
    tree = BiTree(initial_price, sigma)
    head_list = [tree.head]
    tree.printer()
    get_intrinsic_value = lambda price: price - strike

    impotence_list = tree.get_impotent_children([tree.head])
    impotence_list = map(lambda x: x.price, impotence_list)
    impotence_list = map(get_intrinsic_value, impotence_list)
    


    temp = calc_price_move(sigma)
    p = (interest_rate - temp[0]) / (temp[1] - temp[0])
    new_list = binomial_method(impotence_list, p, interest_rate)
    while len(new_list) > 1:
        new_list = binomial_method(new_list, p, interest_rate)
    print new_list[0]


if __name__ == "__main__":
    main()
