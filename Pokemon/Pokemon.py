import random


class Pokemon:
    """
    Pokemon Class: Defines the attributes of a pokemon to create a pokemon object
    """

    def __init__(self, name, type, hp, attack, defense, height, weight, moves):
        self.name = name
        self.type = type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.height = height
        self.weight = weight
        self.moves = moves

    def type_efficiency(self, attacker, defender):
        """

        :param attacker: pokemon that attacks
        :param defender: pokemon that is being attack
        :return: the type efficiency of the attacker against the opponent based on the type of the pokemon.
        handles other types not specified
        """
        type_matchup = {
            'Normal': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1},
            'Fire': {'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Electric': 1, 'Grass': 2},
            'Water': {'Normal': 1, 'Fire': 2, 'Water': 0.5, 'Electric': 1, 'Grass': 0.5},
            'Electric': {'Normal': 1, 'Fire': 1, 'Water': 2, 'Electric': 0.5, 'Grass': 0.5},
            'Grass': {'Normal': 1, 'Fire': 0.5, 'Water': 2, 'Electric': 1, 'Grass': 0.5},
            'Other': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1}
        }

        # if attacker.type or defender.type is not in Normal, Fire, Water, Electric, Grass then it is Other
        if attacker.type not in type_matchup or defender.type not in type_matchup:
            return type_matchup['Other'][defender.type]
        # else we directly return the type efficiency
        else:
            return type_matchup[attacker.type][defender.type]

    def get_damage(self, attacker, opponent, move):
        """
        Returns damage done by pokemon attacking to the pokemon receiving the attack based on the
        provided formula
        :param attacker: pokemon that attacks
        :param opponent: pokemon that receives teh attack
        :param move: Move selected by the player or comp
        :return: damage caused to the pokemon defending
        """
        damage = move.power * (self.attack / opponent.defense)

        # multiply damage by 1.5 when pokemon and move are of the same type
        if move.type == self.type:
            damage *= 1.5
        # multiply by a random number between 0.5 and 1
        damage *= random.uniform(0.5, 1)
        # multiply by the type efficiency
        damage *= self.type_efficiency(attacker, opponent)
        return int(damage)
