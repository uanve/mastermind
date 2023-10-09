from itertools import product
import random


class Mastermind:
    def __init__(self, k, solution):
        self.K = k
        self.N = len(solution)
        self.options = self.generate_options()
        self.trial = None
        self.new_options = dict()
        self.solution = solution
        self.iterations = None

    def generate_options(self):
        return list(product(list(range(1, self.K + 1)), repeat=self.N))

    def is_option_allocated(self, option):
        return option in [trial for key_values in self.new_options.values() for trial in key_values]

    # add candidate if score is b, w
    def check_B_W(self, verbosity=False):
        counts = []
        for w in range(self.N + 1):
            for b in range(self.N + 1):
                if b + w <= self.N:
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
                                c += 1
                                if verbosity: print(option)
                                new_options.append(option)

                    self.new_options[(b, w)] = new_options
                    if verbosity: print(f"({b},{w}): {c}")
                    counts.append(c)
        return counts

    # returns worst case. For this trial, the number of candidates remaining
    def infere_score(self, trial):
        self.trial = trial
        self.new_options = dict()
        return max(self.check_B_W())
        # return max(self.check_0_0() + self.check_B_W())

    def infere_all_scores(self):
        best_option = None
        best_option_n_possibilities = 999
        for option in self.options:
            if self.infere_score(option) < best_option_n_possibilities:
                best_option_n_possibilities = self.infere_score(option)
                best_option = option
        # print(f"best option: {best_option} with {best_option_n_possibilities} possibilities")
        self.infere_score(best_option)
        return best_option

    def update_options(self, score):

        # print(self.new_options[score])
        self.options = self.new_options[score]
        return len(self.options)

    def get_score(self, trial):
        black, match_idx = self.calculate_black_score(trial, self.solution)
        white = self.calculate_white_score(trial, self.solution, match_idx)
        return (black, white)

    def main(self, interactive=False):

        it = 0
        while True:
            it += 1

            next_option = self.infere_all_scores()

            print(f"trying {next_option}")

            self.infere_score(next_option)

            if interactive:
                score = input("what's the current score? black,white = ")
                new_score = tuple(int(_score) for _score in score.split(","))
            else:
                new_score = self.get_score(next_option)

            if new_score == (self.N, 0):
                print(f"Solution found after {it} iterations!: {next_option}")
                self.iterations = it
                break

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

        white_pegs = 0
        solution_counts = {}  # Store the count of colors in the solution

        # Count the occurrences of each color in the solution
        for color in arr1:
            solution_counts[color] = solution_counts.get(color, 0) + 1

        # Iterate through the guess and count the white pegs
        for i in range(len(arr2)):
            if arr2[i] in solution_counts and solution_counts[arr2[i]] > 0:
                white_pegs += 1
                solution_counts[arr2[i]] -= 1

        return white_pegs

    @staticmethod
    def filter_idx(arr, filtered_idx):
        return [arr[i] for i in range(len(arr)) if i not in filtered_idx]


def solve_many_games():
    n_colors = 6
    for i in range(10):

        solution = tuple(random.randint(1, n_colors) for i in range(4))

        interactive = False

        for s in solution:
            assert 0 < s <= n_colors, f"solution has to be between {1} and {n_colors}, solution provided: {solution}"

        m = Mastermind(n_colors, solution)
        m.main(interactive=interactive)

        print(m.iterations)


def solve_one_game(n_colors, solution=None, interactive=False):
    if solution is None and interactive is False:
        raise Exception("No solution provided! No solution only available in interactive mode")

    m = Mastermind(n_colors, solution)
    m.main(interactive=interactive)


if __name__ == "__main__":
    n_colors = 6
    interactive = False
    solution = (5, 2, 3)

    solve_one_game(n_colors, solution=solution, interactive=interactive)
    # solve_many_games()
