import random
from collections import Counter

t = 10000 # number of simulations to run
n = 20 # size of network
p = 0.1 # probability of infection
d = 0 # number of days it takes to infect each computer once
i = 1 # number of initial infection

class Computer:
    def __init__(self, infected, p, infected_once):
        self.infected = infected
        self.p = p
        self.infected_once = infected_once  

def main():
    # network = create_network(n) # create a network of computers of size n
    # initial_infection(i, network) # assign initial number of computers to be infected
    # print('Expected value of %.2f computers infected in the network of %d computers in %d trials with %.2f probability of infection' %(expected_value(t, n, i), n, t, p))
    network = create_network(n)
    initial_infection(i, network)
    print(infect_all(network, d))

def create_network(network_size):
    # print('Creating network of size: %d' %(network_size))
    i = 0
    network = []
    while i < network_size:
        network.append(Computer(False, p, False))
        i += 1
    return network

def initial_infection(num_infect, network):
    # print('Initial number of infected computers: %d' %(num_infect))
    i = 0
    for computer in network:
        if i >= num_infect:
            break
        else:
            computer.infected = True
            computer.infected_once = True
            i += 1

def daily_infection(network):
    infected = 0
    not_infected = 0
    for computer in network:
        if computer.infected:
            infected += 1
        else:
            u = random.random()
            if u < computer.p:
                computer.infected = True
                computer.infected_once = True
                infected += 1
            else:
                not_infected += 1
    d = {}
    d['infected'] = infected
    d["not_infected"] = not_infected
    return d

def infect_all(network, days):
    daily_infection(network)
    days += 1
    for computer in network:
        if not computer.infected_once:
            return infect_all(network, days)
    return days

def daily_repair(network):
    i = 0 # current number of repairs
    max_repair = 5 # maximum number of repairs
    for computer in network:
        if i >= max_repair:
            break
        else:
            if computer.infected:
                computer.infected = False
                i += 1
                # print('Computer repaired...')

def expected_value(num_trials, network_size, num_infect):
    i = 0
    infected = 0.0
    not_infected = 0.0
    d = {}
    print('Running %d trials...' %(num_trials))
    while i < num_trials:
        network = create_network(network_size)
        initial_infection(num_infect, network)
        temp_dict = daily_infection(network)
        # add daily repair
        infected += temp_dict['infected']
        not_infected += temp_dict['not_infected']
        i += 1
    d['infected'] = infected
    d['not_infected'] = not_infected
    # print(d)
    return infected / num_trials

main()