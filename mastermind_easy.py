#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 16:33:15 2023

@author: joan
"""
from itertools import product





class Mastermind:
    def __init__(self, k, solution):
        self.K = k
        self.N = len(solution)
        self.options = self.gemerate_options()
        self.trial = None
        self.new_options = dict()
        self.solution = solution
        
    def calc(self, trial):
        self.trial = trial
        self.check_0_0()
        self.check_0_1()
        self.check_0_2()
        self.check_1_0()
        
    def gemerate_options(self):
        
        return list(product(list(range(1, self.K+1)), repeat=self.N))
        
        
    # add candidate if it doesn't contain any of the numbers in trial
    def check_0_0(self, verbosity=False):
        c = 0
        new_options = []
        for option in self.options:
            if sum([e in option for e in self.trial]) == 0:
                new_options.append(option)
                if verbosity: print(option)
        self.new_options[(0,0)] = new_options
        if verbosity: print(f"(0,0): {c}")
        return [c]
    
    def check_B_W(self, verbosity=False):
        counts = []
        for w in range(self.N):
            for b in range(self.N):
                if b + w <= 4:
                    c = 0
                    new_options = []
                    for option in self.options:
                        if option == self.trial:
                            continue
                        black, match_idx = self.calculate_black_score(option, self.trial)        
                        if black != b:
                            continue
                        else:
                            white = self.calculate_white_score(option, self.trial, match_idx)
                            if white == w:
                                c+=1
                                if verbosity: print(option)
                                new_options.append(option)
                                
                    
                    self.new_options[(b, w)] = new_options
                    if verbosity: print(f"({b},{w}): {c}")
                    counts.append(c)
        return counts
                                
    
    def infere_score(self, trial):
        self.trial = trial
        return max(self.check_0_0() + self.check_B_W())
        # return max([
        #     self.check_0_0(),
        #     self.check_0_1(),
        #     self.check_0_2(),
        #     self.check_1_0()
        #     ])
    
    def infere_all_scores(self):
        best_option = None
        best_option_n_possibilities = 999
        for option in self.options:
            # print(option, self.infere_score(option))
            if self.infere_score(option) < best_option_n_possibilities:
                best_option_n_possibilities = self.infere_score(option)
                best_option = option
        # print(f"best option: {best_option} with {best_option_n_possibilities} possibilities")
        return best_option
                
        
    def update_options(self, score):
        
        # print(self.new_options[score])
        self.options = self.new_options[score]
        return len(self.options)
        
        
    def get_score(self, trial):
        black, match_idx = self.calculate_black_score(self.trial, self.solution)
        white = self.calculate_white_score(self.trial, self.solution, match_idx)
        return (black, white)
        
    
    def main(self):
        
        not_found = True
        it = 0
        
        while True:
            it += 1
            next_option = self.infere_all_scores()
            
            print(f"trying {next_option}")
            
            self.infere_score(next_option)
            new_score = self.get_score(next_option)
            
            if new_score == (self.N, 0):
                return f"Solution found after {it} iterations!: {next_option}" 
            
            new_n_options = self.update_options(new_score)
            
            
    
    @staticmethod
    def calculate_black_score(arr1, arr2):
        score = 0
        match_idx = []
        for i in range(len(arr1)):
            if arr1[i] == arr2[i]:
                score += 1
                match_idx.append(i)
        return score, match_idx

    
    def calculate_white_score(self, arr1, arr2, black_match_idx):
        arr1 = self.filter_idx(arr1, black_match_idx)
        arr2 = self.filter_idx(arr2, black_match_idx)
        return sum([arr1[i] in arr2 for i in range(len(arr1))])
    
    @staticmethod
    def filter_idx(arr, filtered_idx):
        return [arr[i] for i in range(len(arr)) if i not in filtered_idx]
        
    
        
m = Mastermind(6, (6,2,1))
m.main()

m.trial = (2,2,1)
m.check_B_W(True)


next_option = m.infere_all_scores()

print(f"trying {next_option}")

m.infere_score(next_option)
new_score = (2,2)

if new_score == (m.N, 0):
    print(f"Solution found {next_option}" )

new_n_options = m.update_options(new_score)

        
                
