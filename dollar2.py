#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Backtrack:
    """
    Backtrack dynamic algorithm for Shubik's 2-player dollar auction.
    """
    def __init__(self, b1=50, b2=50, s=20):
        self.b1 = b1
        self.b2 = b2
        self.s = s
        self.a = None

    def backtrack(self):
        # a - Matrix containing information who wins
        # a[i][j] == (which_player_wins, (inext, jnext))
        self.a = [
            [(0, None) for _ in range(self.b2 + 1)]
            for _ in range(self.b1 + 1)
        ]
        self.initial_values()
        self.dynamic_fill()
        return self.a

    def initial_values(self):
        for j in range(0, self.b2):
            self.a[self.b1][j] = (1, None)
        for i in range(0, self.b1):
            self.a[i][self.b2] = (2, None)

    def dynamic_fill(self):
        # Fill the matrix dynamically
        # Each iteration of loop over variable k fills L-shaped fragment
        for k in range(1, min(self.b1, self.b2) + 1):
            for i in range(self.b1 + 1 - k):
                self.step(i, self.b2 - k)
            for j in range(self.b2 + 1 - k):
                self.step(self.b1 - k, j)

        # Special case: when bids are both 0,
        # check if player 1 has winning strategy
        self.step1(0, 0)

    def step(self, i, j):
        # Determine whose move it is
        if i < j:
            self.step1(i, j)
        elif i > j:
            self.step2(i, j)

    def step1(self, i, j):
        # As player 1, we must give at least 1 unit more
        # than player 2 or we pass.
        inext = j + 1
        # If it would be bigger than our bankroll, we pass. Backtrack ends.
        if inext > self.b1:
            self.a[i][j] = (2, None)
            return
        # We must analyse only the options that are profitable for us
        while inext <= self.b1 and inext < i + self.s:
            which_wins, _ = self.a[inext][j]
            if which_wins == 1:
                self.a[i][j] = (1, (inext, j))
                return
            inext += 1
        # When we didn't find suitable action, we pass. Backtrack follows.
        self.a[i][j] = (2, (j + 1, j))

    def step2(self, i, j):
        # As player 2, we must give at least 1 unit more
        # than player 1 or we pass.
        jnext = i + 1
        # If it would be bigger than our bankroll, we pass. Backtrack ends.
        if jnext > self.b2:
            self.a[i][j] = (1, None)
            return
        # We must analyse only the options that are profitable for us
        while jnext <= self.b2 and jnext < j + self.s:
            which_wins, _ = self.a[i][jnext]
            if which_wins == 2:
                self.a[i][j] = (2, (i, jnext))
                return
            jnext += 1
        # When we didn't find suitable action, we pass. Backtrack follows.
        self.a[i][j] = (1, (i, i + 1))

    def print(self):
        print('█ - player 1 wins\n░ - player 2 wins\n▒ - unreachable\n')
        self.print_matrix()
        print('Backtrack:')
        i, j = 0, 0
        while self.a[i][j][1] is not None:
            _, (inext, jnext) = self.a[i][j]
            print('({},{})'.format(inext, jnext))
            i, j = inext, jnext

    def print_matrix(self):
        for x in range(0, self.b1 + 1):
            s = ''
            for y in range(0, self.b2 + 1):
                v, _ = self.a[x][y]
                if v == 0:
                    s += '▒'
                elif v == 1:
                    s += '█'
                else:
                    s += '░'
            print(s)
        print()

if __name__ == '__main__':
    backtrack = Backtrack()
    a = backtrack.backtrack()
    backtrack.print()
