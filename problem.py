import sys


def execution(filename):
    
    with open(filename, 'r') as f:
        res = []
        result = f.readline().strip().split(" ")
        default_val = ["0", "0", "0"]

        while result != default_val:
            
            machine = Machines(*result) #creates the machine object that I'm working with
            
            # add list of machine info
            for i in range(machine.N):
                machine_info = f.readline().strip().split(' ')
                machine.machines.append(Machine(*machine_info))

                
            res.append(machine)
            result = f.readline().strip().split(' ')

    return res


class Node(object):
    """Make each buy and sell option into a node"""
    # Example Tree of Nodes
    #                           Initial
    #                        buy /   \ stay
    # day 1              outcome1     outcome2
    #                buy / \ stay    buy / \ stay
    # day 3       outcome3 outcome4 outcome5 outcome6
    #
    # Machines.max_profit() will find best of last day outcomes after day D

    def __init__(self):
        self.buy = None
        self.stay = None

        self.curr_machine = None
        self.curr_dollars = 0

        self.node_day = None


class Machine(object):
    """Each machine has 4 attributes"""

    def __init__(self, di, pi, ri, gi):
        self.di = int(di)  # day for sale
        self.pi = int(pi)  # price
        self.ri = int(ri)  # resale value
        self.gi = int(gi)  # generated daily profit


class Machines(object):

    def __init__(self, N, C, D):
        self.N = int(N)  # number of machines
        self.C = int(C)  # company dollars
        self.D = int(D)  # days of restructure
        self.machines = []

    def max_profit(self):
        """Determine the max profit of buying/selling machines"""

        for m_index in range(self.N):
            curr = m_index
            while curr > 0 and \
                    self.machines[curr - 1].di > \
                    self.machines[curr].di:

                self.machines[curr - 1], self.machines[curr] = \
                    self.machines[curr], self.machines[curr - 1]
                curr -= 1

        # initialize a tree with buy and stay options
        outcome_tree = Node()
        outcome_tree.curr_machine = None  # just to be  explicit
        outcome_tree.curr_dollars = self.C
        outcome_tree.node_day = 0

        # for each day, add value to profits whether buy or sell as a tree
        curr_row = [outcome_tree, ]

        # only need to check paths on day machines are avail.
        for machine in self.machines:
            next_row = []

            for outcome_tree in curr_row:

                outcome_tree.buy = Node()
                outcome_tree.stay = Node()
                outcome_tree.buy.node_day = machine.di
                outcome_tree.stay.node_day = machine.di

                # buy branch #
                # do you already own a machine to sell?
                sell_for = 0
                profit = 0
                if outcome_tree.curr_machine:
                    sell_for = outcome_tree.curr_machine.ri
                    # calc profit since last day calculated:
                    profit = outcome_tree.curr_machine.gi * \
                                    (machine.di - outcome_tree.node_day - 1)

                # buy if you have enough
                if machine.pi <= (outcome_tree.curr_dollars + profit + sell_for):
                    # profit from owning last machine
                    outcome_tree.buy.curr_dollars = \
                                outcome_tree.curr_dollars + \
                                profit + \
                                sell_for + \
                                - machine.pi

                    outcome_tree.buy.curr_machine = machine

                    next_row.append(outcome_tree.buy)

                # stay branch #
                outcome_tree.stay.curr_machine = outcome_tree.curr_machine

                try:
                    outcome_tree.stay.curr_dollars = \
                            outcome_tree.curr_dollars + \
                            outcome_tree.curr_machine.gi * \
                            (machine.di - outcome_tree.node_day)
                except AttributeError:
                    outcome_tree.stay.curr_dollars = outcome_tree.curr_dollars
                next_row.append(outcome_tree.stay)

            curr_row = next_row

        # find most profitable outcome
        max_outcome = 0
        for outcome in curr_row:
          
            try:
                final = outcome.curr_dollars + \
                        outcome.curr_machine.gi * \
                        (self.D - outcome.node_day) + \
                        outcome.curr_machine.ri
            # Error will be raised if there is no machine owned 
            except AttributeError:
                final = outcome.curr_dollars
            if final > max_outcome:
                max_outcome = final

        return max_outcome


if __name__ == '__main__':
    
    result = execution("input.txt")
    
    for val, res in enumerate(result,1):
        print ("Case %i: %i" % (val, res.max_profit()))
