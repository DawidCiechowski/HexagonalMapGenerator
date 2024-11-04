class HexCell:
    def __init__(self, q, r, s):
        self.q, self.r, self.s = q, r, s
        self.blocked = False
        self.unit = None

    def __eq__(self, other):
        if not isinstance(other, HexCell):
            return False
        return (self.q, self.r, self.s) == (other.q, other.r, other.s)


    def __hash__(self):
        return hash((self.q, self.r, self.s))
