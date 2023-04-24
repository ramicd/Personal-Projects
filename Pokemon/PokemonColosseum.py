import random
import csv
from Move import Move
from Pokemon import Pokemon


def calculate_damage(attacking_pokemon, defending_pokemon, move):
    """
    Calculates the damage caused to the pokemon defending
    :param attacking_pokemon: pokemon that attacks
    :param defending_pokemon: pokemon receiving the attack
    :param move: move chosen
    :return: damage
    """
    # calculate the damage
    damage = attacking_pokemon.get_damage(attacking_pokemon, defending_pokemon, move)
    # update the hp of the defending pokemon and return the damage
    defending_pokemon.hp -= damage
    return damage


class PokemonColosseum:
    """
    Pokemon Colosseum class: main class that runs the game
    """
    def load_moves(self):
        """
        Loads the moves into moves list
        :return: pokemon moves
        """
        moves = []
        with open('moves-data.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                # set None accuracy to 0
                if row[6] == 'None':
                    row[6] = '0'
                moves.append(Move(row[0], row[1], row[2], row[3], int(row[4]), int(row[5]), int(row[6])))
        return moves


    def load_pokemons(self):
        """
        Loads the pokemons into pokemons list
        :return: pokemons from csv file as a list
        """
        pokemons = []
        with open('pokemon-data.csv', 'r') as file:
            reader = csv.reader(file)
            # ignore first line
            next(reader)
            for row in reader:
                moves = row[7].replace('[', '').replace(']', '').replace("'", '').split(',')
                moves = [move.strip() for move in moves]
                # handle nonexistent moves
                moves = [move for move in moves if move in [move.name for move in self.moves]]
                # create pokemon objects with attributes from file
                pokemons.append(
                    Pokemon(row[0], row[1], int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]), moves))
        return pokemons

    def __init__(self):
        """
        initializes moves and pokemon
        """

        self.moves = self.load_moves()
        self.pokemons = self.load_pokemons()

    def get_move(self, name):
        """
        :param name: returns move object with the specific name
        :return: moves
        """
        for move in self.moves:
            if move.name == name:
                return move

    def get_pokemon_moves(self, pokemon):
        """
        :param pokemon: name of the pokemon
        :return: returns the moves of the pokemon
        """
        moves = []
        for move in pokemon.moves:
            moves.append(self.get_move(move))
        return moves

    def start_battle(self):
        """
        The following method starts the game
        :return:
        """
        print('Welcome to Pokemon Colosseum!')
        print()

        player_name = input('Enter Player Name: ')
        print()

        # randomly choose 3 pokemon for each team such that no pokemon is repeated in either team
        team_rocket_pokemons = random.sample(self.pokemons, 3)
        team_player_pokemons = random.sample(self.pokemons, 3)

        print(
            'Team Rocket enters with {}, {}, and {}.'.format(team_rocket_pokemons[0].name, team_rocket_pokemons[1].name,
                                                             team_rocket_pokemons[2].name))
        print()
        print('Team {} enters with {}, {}, and {}.'.format(player_name, team_player_pokemons[0].name,
                                                           team_player_pokemons[1].name, team_player_pokemons[2].name))
        print()

        print('Let the battle begin!')
        print()

        # randomly choose who starts the battle
        if random.randint(0, 1) == 0:
            print('Coin toss goes to ----- Team Rocket to start the attack!')
            print()
            team_rocket_turn = True
        else:
            print('Coin toss goes to ----- Team {} to start the attack!'.format(player_name))
            print()
            team_rocket_turn = False

        # create a queue for each team
        team_rocket_queue = []
        team_player_queue = []

        # add the pokemon to the queue
        team_rocket_queue.append(team_rocket_pokemons[0])
        team_rocket_queue.append(team_rocket_pokemons[1])
        team_rocket_queue.append(team_rocket_pokemons[2])

        team_player_queue.append(team_player_pokemons[0])
        team_player_queue.append(team_player_pokemons[1])
        team_player_queue.append(team_player_pokemons[2])

        # keep track of the moves used by each pokemon
        team_rocket_moves = []
        team_player_moves = []

        # start the battle
        while len(team_rocket_queue) > 0 and len(team_player_queue) > 0:
            if team_rocket_turn:
                # get the first pokemon in the queue
                pokemon = team_rocket_queue[0]

                # get the moves for the pokemon
                moves = self.get_pokemon_moves(pokemon)

                # randomly choose a move
                move = random.choice(moves)

                # check if the move was used before
                if move.name in team_rocket_moves:
                    # if the move was used before, then check if all the moves were used
                    if len(team_rocket_moves) == len(moves):
                        # if all the moves were used, then reset the moves
                        team_rocket_moves = []
                else:
                    # if the move was not used before, then add it to the list of moves used
                    team_rocket_moves.append(move.name)

                # get the defending pokemon
                defending_pokemon = team_player_queue[0]

                # calculate the damage
                damage = calculate_damage(pokemon, defending_pokemon, move)

                # print the result
                print("Team Rocket's {} cast '{}' to {}:".format(pokemon.name, move.name, defending_pokemon.name))
                print('Damage to {} is {} points.'.format(defending_pokemon.name, damage))

                # # if hp is less than 0 then make it 0
                if defending_pokemon.hp < 0:
                    defending_pokemon.hp = 0

                print('Now {} has {} HP, and {} has {} HP.'.format(pokemon.name, pokemon.hp, defending_pokemon.name,
                                                                   defending_pokemon.hp))
                print()

                # check if the defending pokemon fainted
                if defending_pokemon.hp <= 0:
                    # if the defending pokemon fainted, then remove it from the queue
                    team_player_queue.pop(0)

                    # check if there are any pokemon left in the queue
                    if len(team_player_queue) > 0:
                        # if there are pokemon left in the queue, then print the next pokemon
                        print('Next for Team {}, {} enters battle!'.format(player_name, team_player_queue[0].name))
                        print()

                # change the turn
                team_rocket_turn = False
            else:
                # get the first pokemon in the queue
                pokemon = team_player_queue[0]

                # get the moves for the pokemon
                moves = self.get_pokemon_moves(pokemon)

                # print the moves
                print('Choose the move for {}:'.format(pokemon.name))
                for i in range(len(moves)):
                    print('{}. {}'.format(i + 1, moves[i].name))
                print()

                # get the move from the user and handle error input
                while True:
                    move_number = input('Team {}\'s choice: '.format(player_name))

                    try:
                        move_number = int(move_number)
                        if move_number < 1 or move_number > len(moves):
                            raise ValueError("Invalid move number")
                        move = moves[move_number - 1]
                        break
                    except ValueError:
                        print("Not a valid Move, try again")

                # check if the move was used before
                if move.name in team_player_moves:
                    # if the move was used before, then check if all the moves were used
                    if len(team_player_moves) == len(moves):
                        # if all the moves were used, then reset the moves
                        team_player_moves = []
                else:
                    # if the move was not used before, then add it to the list of moves used
                    team_player_moves.append(move.name)

                # get the defending pokemon
                defending_pokemon = team_rocket_queue[0]

                # calculate the damage
                damage = calculate_damage(pokemon, defending_pokemon, move)

                # print the result
                print("{} cast '{}' to {}:".format(pokemon.name, move.name, defending_pokemon.name))
                print('Damage to {} is {} points.'.format(defending_pokemon.name, damage))

                # # if hp is less than 0 then make it 0
                if defending_pokemon.hp < 0:
                    defending_pokemon.hp = 0

                print('Now {} has {} HP, and {} has {} HP.'.format(pokemon.name, pokemon.hp, defending_pokemon.name,
                                                                   defending_pokemon.hp))
                print()

                # check if the defending pokemon fainted
                if defending_pokemon.hp <= 0:
                    # if the defending pokemon fainted, then remove it from the queue
                    team_rocket_queue.pop(0)

                    # check if there are any pokemon left in the queue
                    if len(team_rocket_queue) > 0:
                        # if there are pokemon left in the queue, then print the next pokemon
                        print('Next for Team Rocket, {} enters battle!'.format(team_rocket_queue[0].name))
                        print()

                # change the turn
                team_rocket_turn = True

        # check if the battle is over
        if len(team_rocket_queue) == 0:
            print('Team {} wins!'.format(player_name))
        else:
            print('Team Rocket wins!')


if __name__ == '__main__':
    """
    Main Method
    """
    # create a new game
    game = PokemonColosseum()
    # start the game
    game.start_battle()
