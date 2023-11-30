import time
import random
import numpy as np

num_simulations = 10000 # number of simulations to run
n_size = int(input("Enter the number of computers in the network: "))# size of network
p_virus = float(input("Enter the probability of infected computers infecting other computers. Has to be between 0 and 1: ")) # probability of infection
r_max = int(input("Enter the maximum number of computers you want to repair each day: ")) # max quantity of repairs
v_init = int(input("Enter the initial number of computers that has infection: ")) # virus initial infection

class Computer:
    infected = False
    infected_once = False
    # p = 0.1 # probability of being infected

    def __init__(self, p_virus):
        self.p = p_virus
    
    def infect(self):
        self.infected = True
        self.infected_once = True

    def repair(self):
        self.infected = False
        

def create_network(network_size):
    network = []
    for i in range(network_size):
        network.append(Computer(p_virus))
    return network

def initial_infection(network, quantity):
    # check if quantity is less than network size
    for i in range(quantity):
        network[i].infect()
    return network

def daily_infection(network):
    num_infected = 0
    # count number of infected computers
    for computer in network:
        if computer.infected:
            num_infected += 1
    
    # for each infected computer, spread virus throughout network
    for _ in range(num_infected):
        for computer in network:
            u = random.random()
            if u < computer.p:
                computer.infect()
    return network

def number_infected(network):
    i = 0
    for computer in network:
        if computer.infected:
            i += 1
    # print(i)
    return i

def number_infected_once(network):
    i = 0
    for computer in network:
        if computer.infected_once:
            i += 1
    # print(i)
    return i

def daily_repair(network):  
    i = 0 # current number of repairs
    for computer in network:
        if computer.infected and i < r_max:
            computer.repair()
            i += 1
    # print('Repaired a total of %d computers' %(i))
    return network

# Part C 2.98
def expected_number_infected():
    total_number_infected_computers = 0
    for _ in range(num_simulations):
        network = create_network(n_size) # create new network of size n
        network = initial_infection(network, v_init) # initial infection
        network = daily_infection(network) # daily infection simulation
        total_number_infected_computers += number_infected(network) # sum number of infected computers per trial
    print("The Expected Number of infected computers is: ", end = " ")
    print('%.4f' %(total_number_infected_computers / num_simulations)) # expected number of infected computers

# Part B 0.0012
def probability_infected_once():
    total_number_infected_once = 0
    for _ in range(num_simulations):
        network = create_network(n_size) # create new network of size n
        network = initial_infection(network, v_init) # initial infection
        num_current_infected = 0
        while num_current_infected < n_size:
            network = daily_infection(network) # daily infection simulation
            num_current_infected = number_infected(network)
            if num_current_infected == n_size or num_current_infected == 0:
                break
            network = daily_repair(network) # daily repair
            # current_infected = number_infected(network)
        if number_infected_once(network) == n_size:
            total_number_infected_once += 1
        
    # print(total_number_infected_once)
    print("The probability of every computers getting infected at least once is: ", end = " ")
    print('%.4f' %(total_number_infected_once / num_simulations))

# Part A 73 days*
def remove_virus():
    # elapsed_days = 0
    start_time = time.time()
    time_taken = []
    for _ in range(num_simulations):
        elapsed_days = 0
        network = create_network(n_size)
        network = initial_infection(network, v_init)
        num_current_infected = number_infected(network)
        while num_current_infected > 0:
            network = daily_infection(network)
            # print('Infected: %d' %(number_infected(network)))
            network = daily_repair(network)
            # print('Infected after repair: %d' %(number_infected(network)))
            num_current_infected = number_infected(network)
            elapsed_days += 1
        time_taken.append(elapsed_days)
    end_time = time.time()
    execution_time = end_time - start_time
    mean = np.mean(time_taken)
    print('Mean of: %.4f with execution time: %f seconds' %(mean, execution_time))
    return mean

def main():
    # Terminate the program immediately since one of the number is less than or equal to 0
    if n_size <= 0 or v_init <= 0 or r_max <= 0 or p_virus < 0:
        print("One of the number is invalid. For the amount of computers, number of initial computers infected and maximum of repaired computers per day, make sure it has to be larger than 0. For the infected probability, it needs to be at least equal to 0.")
        return 0
    if v_init > n_size:
        print("The number of initial infected computer is higher than the size of the network itself.")
        return 0
    if p_virus > 1:
        print("Probability can not be higher than 1.")
        return 0
    print()
    expected_number_infected()
    print()
    probability_infected_once()
    print()
# time_taken = []

# for _ in range(num_simulations):
#     time_to_remove = remove_virus()
#     time_taken.append(time_to_remove)

# print(np.mean(time_taken))

    start_time = time.time()

    average = []

    for _ in range(1):
        mean = remove_virus()
        average.append(mean)

    end_time = time.time()
    execution_time = end_time - start_time
    print('Total exectution time for entire simulation: %.4f minutes' %(execution_time / 60))
    print('Final expected days to fix all computers in the network: %.4f' %(np.mean(average)))
main()