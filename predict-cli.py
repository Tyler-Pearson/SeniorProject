from predictor import *
from keras.models import load_model
import os.path



PLAYERS = shelve.open('player_store')['store'].players



def new_model():
   print("Note: 0 = rookie season, project = 0 for best season")
   prep = input("Number of prep seasons: ")
   proj = input("Projecting season: ")
   print("Getting new model")
   return get_predictor(prep = prep, proj = proj)

def get_possible_players(name):
   return sorted(filter(lambda x: len(x.seasons) > get_prep_season(), filter(lambda x: name in x.name.lower(), PLAYERS)), key=lambda x: len(x.seasons), reverse=True)


def print_prediction(model, player, other):
   print(player.name + " " + other)
   print("        age    g      mp     fga    fgp    3pa    3pp    2pa    2pp    fta    ftp    orb    drb    ast    stl    blk    tov    pf     ppg")
   print("prev:   {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f}").format(*denorm(player.seasons[get_prep_season()].to_list()))
   prep = player.seasons[PREP_SEASON].to_list()
   prediction = model.predict(array([array(prep)]))[0]
   print("proj:   {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f}").format(*denorm(prediction))
   if (len(player.seasons) > PROJ_SEASON):
      if (get_proj_season() == 0):
         actual = player.max_season.to_list()
         print("actual: {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f}").format(*denorm(actual))
         print("-------------------------")
         print("Prediction Accuracy (MSE)")
         print("-------------------------")
         print("model prediction: " + str(round(mse_calc(norm(prediction), norm(actual)), 4)))
         print("no change:        " + str(round(mse_calc(prep, norm(actual)), 4)))
         print("pseudo random:    " + str(round(mse_calc([p + random.uniform(-0.05, 0.05) for p in player.seasons[PREP_SEASON].to_list()], norm(actual)), 4)))
         print("random:           " + str(round(mse_calc(random.uniform(low=0.0, high=1.0, size=(19,)), norm(actual)), 4)))
      else:
         actual = player.seasons[get_proj_season()].to_list()
         print("actual: {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f} {:6.3f}").format(*denorm(actual))
         print("-------------------------")
         print("Prediction Accuracy (MSE)")
         print("-------------------------")
         print("model prediction: " + str(round(mse_calc(norm(prediction), norm(actual)), 4)))
         print("no change:        " + str(round(mse_calc(prep, norm(actual)), 4)))
         print("pseudo random:    " + str(round(mse_calc([p + random.uniform(-0.1, 0.1) for p in player.seasons[PREP_SEASON].to_list()], norm(actual)), 4)))
         print("random:           " + str(round(mse_calc(random.uniform(low=0.0, high=1.0, size=(19,)), norm(actual)), 4)))


def predict(model, names_train):
   name = raw_input("Player name: ").lower() # must change to input for conversion to python3
   possible_players = get_possible_players(name)
   if (len(possible_players) == 0):
      print("Player unavailable")
   elif (len(possible_players) == 1):
      print_prediction(model, possible_players[0], (" from train set" if possible_players[0].name in names_train else " from test set"))
   else:
      print("Did you mean:")
      i = 0
      for p in possible_players:
         print("   [" + str(i) + "] - " + p.name)
         i += 1
      print("   [" + str(i) + "] - None of these")
      player_ind = int(input("Which do you want?: "))
      if (player_ind >= 0 and player_ind < len(possible_players)):
         print_prediction(model, possible_players[player_ind], (" from train set" if possible_players[player_ind].name in names_train else " from test set"))
      else:
         print("Sorry!")


def get_option():
   print("\nOptions:")
   print("   (n) Get new model")
   print("   (p) Get player prediction")
   print("   (s) Save model")
   print("   (x) Exit")
   return raw_input("What do you want to do?: ").lower() # Must change to input for conversion to python3


def main():
   print("\nlet's predict!\nInitializing model\n")
   if (os.path.isfile("saved_model.h5") and os.path.isfile("saved_names")):
      print("Retrieving existing model")
      model = load_model("saved_model.h5")
      ps = shelve.open('saved_names')
      names_train = ps['names']
      ps.close()
   else:
      (m, n) = new_model()
      model = m
      names_train = n
   option = 'a'

   while (option != 'x'):
      option = get_option()
      if (option != 'n' and option != 'p' and option != 'x' and option != 's'):
         print("Invalid option")
      elif (option == 'n'):
         (m, n) = new_model()
         model = m
         names_train = n
         print("Model replaced!")
      elif (option == 'p'):
         print("Getting prediction")
         predict(model, names_train)
      elif (option == 's'):
         ps = shelve.open('saved_names')
         ps['names'] = names_train
         ps.close()
         model.save("saved_model.h5")
         print("Model Saved")
      else:
         print("Thanks!\n")


if __name__ == "__main__":
   main()
