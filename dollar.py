#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Backtrack2:
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
        self.dynamic_fill()
        return self.a

    def dynamic_fill(self):
        # Fill the matrix dynamically
        # Each iteration of loop over variable l fills L-shaped fragment
        for l in range(0, min(self.b1, self.b2) + 1):
            # Corner case for unequal budgets
            self.step(self.b1 - l, self.b2 - l)
            # Normal cases
            for i in range(self.b1 - l, -1, -1):
                self.step(i, self.b2 - l)
            for j in range(self.b2 - l, -1, -1):
                self.step(self.b1 - l, j)

        # Special case: force player 1 to make move:
        # (0, 0) -> (x, 0) where x > 0
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
        # If it would be bigger than our bankroll or it's unprofitable, we pass. Backtrack ends.
        if not (inext <= self.b1 and inext < i + self.s):
            self.a[i][j] = (2, None)
            return
        # We must analyse only the options that are profitable for us
        while inext <= self.b1 and inext < i + self.s:
            which_wins, _ = self.a[inext][j]
            if which_wins == 1:
                self.a[i][j] = (1, (inext, j))
                return
            inext += 1
        # When we didn't find suitable action, we make unsuitable move. Backtrack follows.
        self.a[i][j] = (2, (j + 1, j))

    def step2(self, i, j):
        # As player 2, we must give at least 1 unit more
        # than player 1 or we pass.
        jnext = i + 1
        # If it would be bigger than our bankroll or it's unprofitable, we pass. Backtrack ends.
        if not (jnext <= self.b2 and jnext < j + self.s):
            self.a[i][j] = (1, None)
            return
        # We must analyse only the options that are profitable for us
        while jnext <= self.b2 and jnext < j + self.s:
            which_wins, _ = self.a[i][jnext]
            if which_wins == 2:
                self.a[i][j] = (2, (i, jnext))
                return
            jnext += 1
        # When we didn't find suitable action, we make unsuitable move. Backtrack follows.
        self.a[i][j] = (1, (i, i + 1))

    def print(self):
        print('█ - player 1 wins\n░ - player 2 wins\n▒ - unreachable\n')
        self.print_matrix()
        self.print_backtrack(0, 0)

    def print_backtrack(self, i, j):
        print('Backtrack for ({},{}):'.format(i, j))
        while self.a[i][j][1] is not None:
            _, (inext, jnext) = self.a[i][j]
            print('({},{})'.format(inext, jnext))
            i, j = inext, jnext

    def print_matrix(self):
        for x in range(0, self.b1 + 1):
            s = '{}\t'.format(x)
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


class Backtrack3:
    """
    Backtrack dynamic algorithm for Shubik's 3-player dollar auction.
    """
    def __init__(self, b1=20, b2=20, b3=20, s=6):
        # Bankrolls
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        # 2-player games
        self.g12 = Backtrack2(b1=b1, b2=b2, s=s).backtrack()
        self.g13 = Backtrack2(b1=b1, b2=b3, s=s).backtrack()
        self.g23 = Backtrack2(b1=b2, b2=b3, s=s).backtrack()
        # Stake
        self.s = s
        # Soon-to-be matrix
        self.a = None

    def backtrack(self):
        # a - Matrix containing information who wins
        # a[i][j][k] == (which_player_wins, (inext, jnext, knext))
        self.a = [
            [
                [
                    (0, None) for _ in range(self.b3 + 1)
                ] for _ in range(self.b2 + 1)
            ] for _ in range(self.b1 + 1)
        ]
        self.initial_values()
        self.dynamic_fill()
        return self.a

    def initial_values(self):
        for j in range(0, self.b2):
            for k in range(0, self.b3):
                self.a[self.b1][j][k] = (1, None)
        for i in range(0, self.b1):
            for k in range(0, self.b3):
                self.a[i][self.b2][k] = (2, None)
        for i in range(0, self.b1):
            for j in range(0, self.b2):
                self.a[i][j][self.b3] = (3, None)

    def dynamic_fill(self):
        # Fill the matrix dynamically
        # Each iteration of loop over variable l fills L-shaped fragment
        for l in range(0, min(self.b1, self.b2, self.b3)):
            for i in range(self.b1 - l):
                for j in range(self.b2 - l):
                    if i != j:
                        self.step(i, j, self.b3 - l - 1)
            for i in range(self.b1 - l):
                for k in range(self.b3 - l):
                    if i != k:
                        self.step(i, self.b2 - l - 1, k)
            for j in range(self.b2 - l):
                for k in range(self.b3 - l):
                    if j != k:
                        self.step(self.b1 - l - 1, j, k)

        # Special case: force player 2 to make move:
        # (x, 0, 0) -> (x, y, 0) where y > x > 0
        for i in range(1, self.b1 + 1):
            self.step2(i, 0, 0)
        # Special case: force player 1 to make move:
        # (0, 0, 0) -> (x, 0, 0) where x > 0
        self.step1(0, 0, 0)

    def step(self, i, j, k):
        # Determine whose move it is
        if i < j and i < k:
            self.step1(i, j, k)
        elif j < i and j < k:
            self.step2(i, j, k)
        elif k < i and k < j:
            self.step3(i, j, k)

    def step1(self, i, j, k):
        # As player 1, we must give at least 1 unit more
        # than max bid of other players or we pass.
        inext = max(j, k) + 1
        # If it would be bigger than our bankroll, we pass. Backtrack ends.
        if inext > self.b1:
            which_wins, _ = self.g23[j][k]
            self.a[i][j][k] = (which_wins, None)
            return
        # We must analyse only the options that are profitable for us
        while inext <= self.b1 and inext < i + self.s:
            which_wins, _ = self.a[inext][j][k]
            if which_wins == 1:
                self.a[i][j][k] = (1, (inext, j, k))
                return
            inext += 1
        # When we didn't find suitable action, we make unsuitable move. Backtrack follows.
        inext = max(j, k) + 1
        which_wins, _ = self.a[inext][j][k]
        self.a[i][j][k] = (which_wins, (inext, j, k))

    def step2(self, i, j, k):
        # As player 2, we must give at least 1 unit more
        # than max bid of other players or we pass.
        jnext = max(i, k) + 1
        # If it would be bigger than our bankroll, we pass. Backtrack ends.
        if jnext > self.b2:
            which_wins, _ = self.g13[i][k]
            self.a[i][j][k] = (which_wins, None)
            return
        # We must analyse only the options that are profitable for us
        while jnext <= self.b2 and jnext < j + self.s:
            which_wins, _ = self.a[i][jnext][k]
            if which_wins == 2:
                self.a[i][j][k] = (2, (i, jnext, k))
                return
            jnext += 1
        # When we didn't find suitable action, we make unsuitable move. Backtrack follows.
        jnext = max(i, k) + 1
        which_wins, _ = self.a[i][jnext][k]
        self.a[i][j][k] = (which_wins, (i, jnext, k))

    def step3(self, i, j, k):
        # As player 3, we must give at least 1 unit more
        # than max bid of other players or we pass.
        knext = max(i, j) + 1
        # If it would be bigger than our bankroll, we pass. Backtrack ends.
        if knext > self.b2:
            which_wins, _ = self.g12[i][j]
            self.a[i][j][k] = (which_wins, None)
            return
        # We must analyse only the options that are profitable for us
        while knext <= self.b3 and knext < k + self.s:
            which_wins, _ = self.a[i][j][knext]
            if which_wins == 3:
                self.a[i][j][k] = (3, (i, j, knext))
                return
            knext += 1
        # When we didn't find suitable action, we make unsuitable move. Backtrack follows.
        knext = max(i, j) + 1
        which_wins, _ = self.a[i][j][knext]
        self.a[i][j][k] = (which_wins, (i, j, knext))

    def print(self):
        self.print_matrix()
        self.print_backtrack(0, 0, 0)

    def print_matrix(self):
        for z in range(0, self.b3 + 1):
            for x in range(0, self.b1 + 1):
                s = ''
                for y in range(0, self.b2 + 1):
                    v, _ = self.a[x][y][z]
                    if v == 0:
                        s += '▒'
                    else:
                        s += str(v)
                print(s)
            print()

    def print_backtrack(self, i, j, k):
        print('Backtrack for ({},{},{}):'.format(i, j, k))
        while self.a[i][j][k][1] is not None:
            _, (inext, jnext, knext) = self.a[i][j][k]
            print('({},{},{})'.format(inext, jnext, knext))
            i, j, k = inext, jnext, knext

if __name__ == '__main__':
    # backtrack = Backtrack2(b1=50, b2=50, s=20)
    # backtrack = Backtrack2(b1=45, b2=50, s=20)
    # backtrack = Backtrack2(b1=50, b2=45, s=20)
    backtrack = Backtrack3(b1=9, b2=9, b3=9, s=3)
    # backtrack = Backtrack3(b1=9, b2=9, b3=9, s=4)
    a = backtrack.backtrack()
    backtrack.print()
