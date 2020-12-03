#!/usr/bin/env python
# coding: utf-8

# In[59]:


import numpy as np
from scipy import random
import networkx as nx
import pandas as pd
import random
import collections
import matplotlib.pyplot as plt
import os
import json
from time import time
from collections import Counter


#Model constructor
class HigherOrderNamingGame():
    
    def __init__(self, N, sizes, weights, rule):
        
        #Structure
        self.N = N
        self.simp_sizes = sizes
        self.simp_weights = weights
        self.nodes = range(self.N)
        
        #Time
        self.t = 0
        
        #Rule
        self.rule = rule

    def SetInitialConditions(self, beta, p, n_A, verbose=False):
        
        #Game parameters
        self.beta = beta
        self.p = p
    
        #Opinions of the nodes (vocabularies)
        self.opinions = {}
        
        #Generating committed agents
        N_p = int(self.N*self.p) #number of committed agents
        #Randomly picking N_p committed agents
        committed = random.sample(self.nodes, N_p)
        #Setting up a committed dictionary
        #self.is_committed = {n:False for n in self.nodes}
        for n in self.nodes:
            if n in committed:
                #self.is_committed[n]=True
                #Assigning opinion "A" to committed agents
                self.opinions[n]=frozenset(["A"])
        
        #Calculating the number of agents holding n_A (not committed) from the density in input
        N_A = int(self.N*n_A)
        N_B = self.N-N_A-N_p
        #Creating a list of opinions to assign
        opinions_to_assign = ['A']*N_A + ['B']*N_B
        #Shuffling them
        random.shuffle(opinions_to_assign)
        #Agents left to be matched with opinions
        noncommitted = set(self.nodes) - set(committed)
        for n, o in zip(noncommitted, opinions_to_assign):
            self.opinions[n]=set(o)
            
        if verbose: print('Setup Done.', self.N, 'nodes,', "N_A:", N_A, "N_B:", N_B, "N_p:", N_p) 
    
    def AgreeOnSimplex(self, simplex, said_word):
        
        #Updating the simplex on the agreed word 
        for n in simplex:
            try: #There are also committed minorities which have frozensets!
                self.opinions[n].clear()
                self.opinions[n].add(said_word)
            except AttributeError: #It was committed
                pass

    def ListenersLearnWord(self, listeners, said_word):
        
        #Looping through the listeners
        for listener in listeners:
            try: #Trying to learn...
                self.opinions[listener].add(said_word)
            except AttributeError: #It was committed
                pass
                
    def play_on_simplex(self, simplex):
        
        #Selecting speaker and listeners at random
        random.shuffle(simplex)
        speaker = simplex[0]
        listeners = simplex[1:]
        
        #Selecting a random word to be said
        said_word = random.choice(list(self.opinions[speaker]))
        words_of_listeners = [self.opinions[listener] for listener in listeners]
        
        #Using the rule to get the words of listeners to be used for the agreement
        if self.rule=='union': 
            words_of_listeners_by_rule = set.union(*[set(w) for w in words_of_listeners])
        elif self.rule=='intersection':    
            words_of_listeners_by_rule = set.intersection(*[set(w) for w in words_of_listeners])
        
        #Trying to agree based on the rule and the communication efficiency beta
        if (said_word in words_of_listeners_by_rule) and (random.random() <= self.beta):
            self.AgreeOnSimplex(simplex, said_word)
        else: #No agreement, but the said word is learned by the listeners
            self.ListenersLearnWord(listeners, said_word)
            
    def get_densities(self):
        single_opinion_counter = collections.Counter([list(opinions)[0] for opinions in self.opinions.values() if len(opinions)==1])
        n_Ap = single_opinion_counter["A"]/self.N
        n_B = single_opinion_counter["B"]/self.N
        n_AB = 1-n_Ap-n_B
        return n_Ap, n_B, n_AB

    def run(self, path, t_max=100, check_every=10, print_every=1):
        
        self.t_max = t_max
        
        #Opening file to save densities results
        densities_path = path + 'HONG_densities_N%i_beta%.4f_p%.4f.csv'%(self.N, self.beta, self.p)
        f = open(densities_path,'w')
        f.write('time,n_A+p,n_B,n_AB\n')
        
        while self.t <= self.t_max:
            self.t += 1
            if self.t%print_every==0: print('t=%i'%self.t)
                      
            #Drawing a group_size from the distribution of group sizes     
            group_size = np.random.choice(self.simp_sizes, p=self.simp_weights)         
            #Playing on a random simplex of size group_size obtained from the list of nodes
            simplex = random.sample(self.nodes, group_size)
            self.play_on_simplex(simplex)
                
            #Storing the values every check_every time steps:
            if self.t%check_every==0:
                n_Ap, n_B, n_AB = self.get_densities()
                line = "%i,%.3f,%.3f,%.3f\n"%(self.t, n_Ap, n_B, n_AB)
                f.write(line)
                
                #Also checking if we reached the absorbing state:
                if n_Ap==1 or n_B==1:
                    f.close()   
                    print('DONE! Reached the absorbing state.')
                    return None
                
        f.close()    
        print('DONE! Run out of time...')
        
def get_size_dists_from_simplices(simplices):
    size_counter = collections.Counter([len(simplex) for simplex in simplices])
    #normalising the counter
    norm = 1./sum(size_counter.values())
    size_counter = {k:v*norm for k, v in size_counter.items()}
    #converting to lists
    sizes = list(size_counter.keys())
    weights = list(size_counter.values())
    return sizes, weights


# ## Reading the simplices of a data set


#Reading
filename = '../Data/email-Eu/Processed_data/email-Eu_simplices.json'
simplices = json.load(open(filename,'r'))

dataset = 'email-Eu'

# Extracting the facets size distributions

# In[66]:


sizes, weights = get_size_dists_from_simplices(simplices)

# ## Simulating

# In[47]:


rule = 'union'

betas = np.linspace(0.,1.,30)
p = 0.03
n_A = 0

t_max = 1e5
check_every = 100
print_every=50000

N = 1000

n_runs = 50

for run_id in range(n_runs):
    for beta in betas:
        print(run_id, beta)

        output_path = '../Results/Simulations/HONG_2words_HomMix_datasets/%s/%s/fixed_p%.2f_varbeta_run%i/'%(dataset, rule, p, run_id)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        HONG = HigherOrderNamingGame(N, sizes, weights, rule)
        HONG.SetInitialConditions(beta=beta, p=p, n_A=n_A, verbose=True)
        HONG.run(output_path, t_max, check_every, print_every)
