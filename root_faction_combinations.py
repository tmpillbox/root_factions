import itertools
import prompt_toolkit

faction_stats = {
    'Marquise de Cat': {
        'key': 'MdC',
        'short': 'cats',
        'max': 1,
        'reach': [ 10 ]
    },
    'Underground Duchy': {
        'key': 'UD',
        'short': 'moles',
        'max': 1,
        'reach': [ 8 ]
    },
    'Eyrie Dynasties': {
        'key': 'ED',
        'short': 'birds',
        'max': 1,
        'reach': [ 7 ]
    },
    'Vagabond': {
        'key': 'V',
        'short': 'vagabond',
        'max': 2,
        'reach': [ 5, 2 ]
    },
    'Riverfolk Company': {
        'key': 'RC',
        'short': 'otters',
        'max': 1,
        'reach': [ 5 ]
    },
    'Woodland Alliance': {
        'key': 'WA',
        'short': 'mice',
        'max': 1,
        'reach': [ 3 ]
    },
    'Corvid Conspiracy': {
        'key': 'CC',
        'short': 'crows',
        'max': 1,
        'reach': [ 3 ]
    },
    'Lizard Cult': {
        'key': 'LC',
        'short': 'lizards',
        'max': 1,
        'reach': [ 2 ]
    }
}

player_reach_sums = {
    2: 17,
    3: 18,
    4: 21,
    5: 25,
    6: 28
}

short_names = {
    'cats': 'Marquise de Cat',

}

valid_configurations = { n: [] for n in player_reach_sums.keys() }

class Faction:
    factions = dict()
    short_names = dict()

    def __init__(self, name, key, short_name, max, reach):
        self._name = name
        self.short_name = short_name
        self.key = key
        self.max = max
        self._reach = reach
        self.factions[name] = self
        self.short_names[short_name] = self

    def reach(self, index):
        return self._reach[index]
    def rep(self, index=1):
        if self.max > 1:
            return "{}[{}]".format(self.key, str(index))
        return self.key
    
    def name(self, index):
        if self.max > 1:
            return "{} {}".format(self._name, str(index + 1))
        return self._name

class FactionEntry:
    def __init__(self, faction, index):
        self.faction = faction
        self.index = index
    def __str__(self):
        return self.faction.rep(self.index)

    @property
    def reach(self):
        return self.faction.reach(self.index)

    @property
    def name(self):
        return self.faction.name(self.index)

class FactionCombination:
    def __init__(self, num_players, faction_list=None):
        self.factions = list()
        self.players = num_players
        self.faction_list = faction_list
        if (faction_list is not None):
            for f in faction_list:
                self._add_faction(f)

    def add_faction(self, faction):
        self.faction_list.append(faction)
        return self._add_faction(faction)

    def _add_faction(self, faction):
        if len(self) >= self.players:
            return

        faction_cnt = self.count_faction(faction)
        if (faction_cnt < faction.max):
            self.factions.append(FactionEntry(faction, faction_cnt))

    def count_faction(self, faction):
        return len([ f for f in self.factions if f.faction == faction])    

    @property
    def reach(self):
        return sum([ f.reach for f in self.factions ])

    def __str__(self):
        return "[{}]".format(", ".join(sorted([ str(f) for f in self.factions ])))

    def __len__(self):
        return len(self.factions)

    def __hash__(self):
        return hash(str(self))

    @property
    def pretty_print(self):
        return "{} [{}]\n{}\n\n".format(str(self), str(self.reach), "\n".join([ " - {} [{}]".format(f.name, f.reach) for f in self.factions ]))

    @property
    def export(self):
        return "{}, {}, {}".format(str(self.players), str(self.reach), ", ".join(sorted([ f.name for f in self.factions ])))
    

class FactionCombinations:
    @staticmethod
    def expand_faction_list(faction_list):
        return [ sl_f for sublist in [ [ faction ] * faction.max for faction in faction_list ] for sl_f in sublist ]

    def __init__(self, num_players, target_reach, available_factions):
        self.num_players = num_players
        self.target_reach = target_reach
        self._factions = self.expand_faction_list(available_factions)
        self._found_hashes = list()
        self._found = list()
        self._invalid = list()
        self._recommended = list()
        self._acceptable = list()

    def _find_all(self):
        for fl in itertools.permutations(self._factions, self.num_players):
            fc = FactionCombination(self.num_players, fl)
            fc_hash = hash(fc)
            if fc_hash in self._found_hashes:
                continue
            self._found_hashes.append(fc_hash)

            self._found.append(fc)
            if len(fc) != self.num_players:
                self._invalid.append(fc)
            elif (fc.reach < self.target_reach):
                self._acceptable.append(fc)
            else:
                self._recommended.append(fc)

    @property
    def recommended(self):
        if len(self._found) == 0:
            self._find_all()
        return self._recommended

    @property
    def found(self):
        if len(self._found) == 0:
            self._find_all()
        return self._found

    @property
    def acceptable(self):
        if len(self._found) == 0:
            self._find_all()
        return self._acceptable

    @property
    def invalid(self):
        if len(self._found) == 0:
            self._find_all()
        return self._invalid


_ = [ Faction(k, v['key'], v['short'], v['max'], v['reach'])  for k,v in faction_stats.items() ]

#combinations_per_players = { k:FactionCombinations(k, v, factions.values()) for k,v in player_reach_sums.items() }
#recommended = { k:v.recommended  for k,v in combinations_per_players.items() }
#invalid = { k:v.invalid  for k,v in combinations_per_players.items() }
#found = { k:v.found for k,v in combinations_per_players.items() }
#acceptable = { k:v.acceptable for k,v in combinations_per_players.items() }

if __name__ == '__main__':
    pass

