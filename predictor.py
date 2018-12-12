import shelve
from stats import *
import random
import tensorflow as tf
from keras.models import Model, Sequential
from keras.layers import Input, Dense, Activation
from numpy import array
from numpy import random



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
# epochs
EPOCHS = 200
# size of batches
BATCH_SIZE = 16


# print("\nhi")
# print("let's make some predictions!\n")


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
      players = [player for player in players if (len(player.seasons) > PREP_SEASON)]

   # split into training and testing sets
   random.shuffle(players)
   split_ind = int(len(players) * TRAIN_RATIO)
   train_set = players[:split_ind]
   test_set = players[split_ind:]

   # logging
   # print("LOG:")
   # print(train_set[0].name, train_set[0].seasons[0].to_list())
   # print(test_set[0].name, test_set[0].seasons[0].to_list())

   # get testing and training input and output sets
   x_train = list(map(lambda x: x.seasons[PREP_SEASON].to_list(), train_set))
   x_test = list(map(lambda x: x.seasons[PREP_SEASON].to_list(), test_set))
   if (PROJ_SEASON == 0):
      y_train = list(map(lambda x: x.max_season.to_list(), train_set))
      y_test = list(map(lambda x: x.max_season.to_list(), test_set))
   else:
      y_train = list(map(lambda x: x.seasons[PROJ_SEASON].to_list(), train_set))
      y_test = list(map(lambda x: x.seasons[PROJ_SEASON].to_list(), test_set))

   return (array([array(el) for el in x_train]),
            array([array(el) for el in y_train]),
            array([array(el) for el in x_test]),
            array([array(el) for el in y_test]))


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
def get_model(in_size, out_size):
   h_layer_size = int((in_size + out_size) / 2)
   print("generating model", in_size, h_layer_size, out_size)
   inputs = Input(shape=(in_size,))
   x = Dense(h_layer_size*25, activation='linear')(inputs)
   x = Dense(out_size, activation=tf.nn.sigmoid, use_bias=True)(x)
   x = Dense(out_size, activation='linear', use_bias=True)(x)
   #x = Dense(out_size, activation=tf.nn.sigmoid, use_bias=True)(x)
   #x = Dense(out_size, activation=tf.nn.sigmoid, use_bias=True)(x)
   #x = Dense(out_size, activation=tf.nn.sigmoid, use_bias=True)(x)
   #x = Dense(out_size, activation=tf.nn.sigmoid, use_bias=True)(x)
   outputs = Dense(out_size, activation=tf.nn.sigmoid, use_bias=True)(x)
   model = Model(inputs=inputs, outputs=outputs)
   model.compile(optimizer = 'rmsprop',
      loss = 'mse')
   return model


def get_prep_season():
   global PREP_SEASON
   return PREP_SEASON

def get_proj_season():
   global PROJ_SEASON
   return PROJ_SEASON


def compare_acc(x, y, model):
   print("Comparison metrics")
   predictions = model.predict(x)
   print("Validation MSE Acc:  " + str(mse_all(predictions, y)))
   print("No Change MSE Acc:   " + str(mse_all(x, y)))
   print("Pseudo Rand MSE Acc: " + str(mse_all([p + random.uniform(-0.05, 0.05) for p in x], y)))
   print("Full Rand MSE Acc:   " + str(mse_all([random.uniform(0.0, 1.0, size=len(y[0])) for i in range(len(y))], y)))


#
# Main
#
def get_predictor(prep = 0, proj = 1):
   global PREP_SEASON, PROJ_SEASON
   PREP_SEASON = prep
   PROJ_SEASON = proj
   # get players from shelved player_store
   (x_train, y_train, x_test, y_test) = get_player_sets()
   model = get_model(len(x_train[0]), len(y_train[0]))
   model.summary()
   history = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=0)
   compare_acc(x_test, y_test, model)
   #predictions = model.predict(x_test)
   #print("[age, g, mpg, fga, fgp, 3pa, 3pp, 2pa, 2pp, fta, ftp, orb, drb, ast, stk, blk, tov, pf, ppg]")
   #print(1)
   #print(list(x_test[0]))
   #print([round(x, 3) for x in predictions[0]])
   #print(list(y_test[0]))
   #print(2)
   #print(list(x_test[1]))
   #print([round(x, 3) for x in predictions[1]])
   #print(list(y_test[1]))
   return model
   # p = players[2401]
   # s = p.max_season
   # print(p.name, s.age, s.ftp, s.threepa, s.ppg)
   # print(x_train[0], y_train[0])
   # print(x_test[0], y_test[0])


# if __name__ == "__main__":
   # main()
