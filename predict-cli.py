from predictor import *



PLAYERS = shelve.open('player_store')['store'].players



def new_model():
   print("Note: 0 = rookie season, project = 0 for best season")
   prep = input("Number of prep seasons: ")
   proj = input("Projecting season: ")
   print("Getting new model")
   return get_predictor(prep = prep, proj = proj)

def get_possible_players(name):
   return sorted(filter(lambda x: len(x.seasons) > get_prep_season(), filter(lambda x: name in x.name.lower(), PLAYERS)), key=lambda x: len(x.seasons), reverse=True)


def print_prediction(model, player):
   print(player.name)
   print("        age    g      mp     fga    fgp    3pa    3pp    2pa    2pp    fta    ftp    orb    drb    ast    stl    blk    tov    pf     ppg")
   print("prev:   {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f}").format(*denorm(player.seasons[get_prep_season()].to_list()))
   prediction = model.predict(array([array(player.seasons[PREP_SEASON].to_list())]))[0]
   print("proj:   {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f}").format(*denorm(prediction))
   if (len(player.seasons) > PROJ_SEASON):
      if (get_proj_season() == 0):
         print("actual: {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f}").format(*denorm(player.max_season.to_list()))
      else:
         print("actual: {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f}").format(*denorm(player.seasons[get_proj_season()].to_list()))


def predict(model):
   name = raw_input("Player name: ").lower() # must change to input for conversion to python3
   possible_players = get_possible_players(name)
   if (len(possible_players) == 0):
      print("Player unavailable")
   elif (len(possible_players) == 1):
      print_prediction(model, possible_players[0])
   else:
      print("Did you mean:")
      i = 0
      for p in possible_players:
         print("   [" + str(i) + "] - " + p.name)
         i += 1
      print("   [" + str(i) + "] - None of these")
      player_ind = int(input("Which do you want?: "))
      if (player_ind >= 0 and player_ind < len(possible_players)):
         print_prediction(model, possible_players[player_ind])
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
   model = new_model()
   option = 'a'
   while (option != 'x'):
      option = get_option()
      if (option != 'm' and option != 'p' and option != 'x'):
         print("Invalid option")
      elif (option == 'm'):
         model = new_model()
         print("Model replaced!")
      elif (option == 'p'):
         print("Getting prediction")
         predict(model)
      else:
         print("Thanks!\n")


if __name__ == "__main__":
   main()
