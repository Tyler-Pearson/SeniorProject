import shelve
from stats import *
import random
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation



#
# Global Variables
#

# Prep_Season - for input we consider season 0 through Prep_Season
# keep less than PROJ_SEASON unless PROJ_SEASON == 0
PREP_SEASON = 0
# Proj_Season - season number we are projecting (0 = rookie season)
# set to 0 for max season (no point in projecting rookie season itself)
PROJ_SEASON = 1
# Ratio of train data to test data
# ie 0.8 => 80% train, 20% test
TRAIN_RATIO = 0.8


print("\nhi")
print("let's make some predictions!\n")


# Return players list from shelved player_store
def get_player_sets():
   # pull players from shelved data
   ps = shelve.open('player_store')
   players = ps['store'].players
   ps.close()
   
   # filter players by seasons played
   if (PROJ_SEASON > 0):
      players = [player for player in players if (len(player.seasons) > PROJ_SEASON)]
   else:
      players = [player for player in players if (len(player.seasons) >= PREP_SEASON)]

   # split into training and testing sets
   random.shuffle(players)
   split_ind = int(len(players) * TRAIN_RATIO)
   train_set = players[:split_ind]
   test_set = players[split_ind:]
   
   # logging
   # print(train_set[0].name, train_set[0].seasons[0].to_list())
   # print(test_set[0].name, test_set[0].seasons[0].to_list())
   
   # get testing and training input and output sets
   x_train = list(map(lambda x: x.getAverageOf(PREP_SEASON+1).to_list(), train_set))
   x_test = list(map(lambda x: x.getAverageOf(PREP_SEASON+1).to_list(), test_set))
   if (PROJ_SEASON == 0):
      y_train = list(map(lambda x: x.max_season.to_list(), train_set))
      y_test = list(map(lambda x: x.max_season.to_list(), test_set))
   else:
      y_train = list(map(lambda x: x.seasons[PROJ_SEASON].to_list(), train_set))
      y_test = list(map(lambda x: x.seasons[PROJ_SEASON].to_list(), test_set))

   return (x_train, y_train, x_test, y_test)


# Verify shelving/unshelving occured properly
# Check ages of players as rookies
def check_ages(players):
   # print total number of players
   print(str(len(players)) + " total players\n")

   print("Checking ages:\n")
   # initialize array of 40 empty lists (1 for each age)
   ages = [[] for i in range(40)]
   # iterate through all players, add them to their rookie age list
   for player in players:
      ages[player.seasons[0].age].append((player.name, len(player.seasons)))

   # print number of players who were rookies at different ages
   for i in range(40):
      if not ages[i]:
         continue # skip if rookie age list is empty
      print(str(i) + " - " + str(len(ages[i]))) # Age - Number of players
      if (len(ages[i]) >= 5):
         print(ages[i][:5]) # list of tuples [(Name, Seasons played), ...]
      else:
         print(ages[i])
      print()
         
         
# Set up Neural Network model
def get_model():
   model = Sequential()
   model.add(Dense(19, use_bias=True, activation=tf.nn.relu))
   model.add(Dense(19, use_bias=True, activation=tf.nn.relu))
   model.add(Dense(19))
   model.compile(optimizer = 'adam',
      loss = 'sparse_categorical_crossentropy',
      metrics=['accuracy'])
   return model


#
# Main
#
def main():
   # get players from shelved player_store
   (x_train, y_train, x_test, y_test) = get_player_sets()
   model = get_model()
   # p = players[2401]
   # s = p.max_season
   # print(p.name, s.age, s.ftp, s.threepa, s.ppg)
   # print(x_train[0], y_train[0])
   # print(x_test[0], y_test[0])


if __name__ == "__main__":
   main()

