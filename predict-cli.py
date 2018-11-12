from predictor import *



PLAYERS = shelve.open('player_store')['store'].players



def get_possible_players(name):
   return sorted(filter(lambda x: name in x.name.lower(), PLAYERS), key=lambda x: len(x.seasons), reverse=True)


def predict(model):
   name = raw_input("Player name: ").lower() # must change to input for conversion to python3
   possible_players = get_possible_players(name)
   if (len(possible_players) == 0):
      print("Player unavailable")
   elif (len(possible_players) == 1):
      print("You're looking for " + possible_players[0].name)
   else:
      print("Did you mean:")
      i = 0
      for p in possible_players:
         print("   [" + str(i) + "] - " + p.name)
         i += 1
      print("   [" + str(i) + "] - None of these")
      player_ind = int(input("Which do you want?: "))
      if (player_ind < len(possible_players)):
         print("You're looking for " + possible_players[player_ind].name)
      else:
         print("Sorry!")


def get_option():
   print("\nOptions:")
   print("   (m) Get new model")
   print("   (p) Get player prediction")
   print("   (x) Exit")
   return raw_input("What do you want to do?: ").lower() # Must change to input for conversion to python3


def main():
   print("\nlet's predict!\nInitializing model\n")
   model = get_predictor()
   option = 'a'
   while (option != 'x'):
      option = get_option()
      if (option != 'm' and option != 'p' and option != 'x'):
         print("Invalid option")
      elif (option == 'm'):
         print("Replacing model\n")
         model = get_predictor()
      elif (option == 'p'):
         print("Getting prediction")
         predict(model)
      else:
         print("Thanks!\n")


if __name__ == "__main__":
   main()

