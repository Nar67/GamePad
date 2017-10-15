from simonpad import simonpad_game
from tron import tron_game
from stepseq import stepsequencer
from asteroids import asteroids_game
from tower import tower_game

games = [
    ("Simon", simonpad_game),
    ("Asteroids", asteroids_game),
    ("Tron", tron_game),
    ("Tower", tower_game),
    ("Step Sequencer", stepsequencer),
]

def printMenu():
    print("Select a Game from:")
    for i, data  in enumerate(games):
        name = data[0]
        print(" [%s]. %s" % (i + 1, name))


def isValidInput(choice):
    try:
        value = int(choice)
        if value < 1 or value > len(games) + 1:
            print("Invalid choice. Select a valid option")
            return False
    except Exception:
        print("Invalid choice. Select a valid option")
        return False
    return True


def selectGame():
    choice = raw_input("Enter your choice [1-%s]: " % (len(games) + 1))
    if isValidInput(choice):
        name, module = games[int(choice) - 1]
        print("Selected '%s'" % name)
        module.main()


def main():
    printMenu()
    selectGame()

main()
