import shelve
from stats import *
import random
import tensorflow as tf
from sklearn.model_selection import StratifiedKFold
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
EPOCHS = 50
# size of batches
BATCH_SIZE = 16
# folds
FOLDS = 10


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
   #random.shuffle(players)
   #split_ind = int(len(players) * TRAIN_RATIO)
   #train_set = players[:split_ind]
   #test_set = players[split_ind:]

   # get testing and training input and output sets
   X = list(map(lambda x: x.seasons[PREP_SEASON].to_list(), players))
   #x_test = list(map(lambda x: x.seasons[PREP_SEASON].to_list(), test_set))
   if (PROJ_SEASON == 0):
      Y = list(map(lambda x: x.max_season.to_list(), players))
      #y_test = list(map(lambda x: x.max_season.to_list(), test_set))
   else:
      Y = list(map(lambda x: x.seasons[PROJ_SEASON].to_list(), players))
      #y_test = list(map(lambda x: x.seasons[PROJ_SEASON].to_list(), test_set))

   return (array(X), array(Y))


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
   x = Dense(h_layer_size, activation=tf.nn.sigmoid)(inputs)
   x = Dense(h_layer_size, activation=tf.nn.sigmoid)(x)
   x = Dense(h_layer_size, activation=tf.nn.sigmoid)(x)
   #x = Dense(out_size, activation=tf.nn.sigmoid, use_bias=True)(x)
   #x = Dense(out_size, activation='linear', use_bias=True)(x)
   #x = Dense(out_size, activation=tf.nn.sigmoid, use_bias=True)(x)
   #x = Dense(out_size, activation=tf.nn.sigmoid, use_bias=True)(x)
   #x = Dense(out_size, activation=tf.nn.sigmoid, use_bias=True)(x)
   #x = Dense(out_size, activation=tf.nn.sigmoid, use_bias=True)(x)
   outputs = Dense(out_size, activation=tf.nn.sigmoid, use_bias=True)(x)
   model = Model(inputs=inputs, outputs=outputs)
   model.compile(optimizer = 'rmsprop',
      loss = 'mse')
   return model

#
# Helpers and API
#
def get_prep_season():
   global PREP_SEASON
   return PREP_SEASON

def get_proj_season():
   global PROJ_SEASON
   return PROJ_SEASON

def print_glossary():
   print("----------------")
   print("Metrics Glossary")
   print("----------------")
   print("MSE:          mean squared error = average of normalized error")
   print("Validation:   mse accuracy of model predicting on validation set")
   print("No Change:    prediction is player's stats will not change")
   print("Regr to mean: prediction is player's stats will be halfway between their previous season")
   print("                 and the league historic average for players in their correlated season")
   print("Pseudo Rand:  prediction is player's prep season + 0% to 10% improvement")
   print("Full Rand:    prediction is random float between 0.0 and 1.0 denormalized\n")

def get_averages(p_set):
   averages = []
   for i in range(len(p_set[0])):
      sum = 0
      for j in range(len(p_set)):
         sum += p_set[j][i]
      averages.append(sum / len(p_set))
   return averages

def compare_acc(x, y, model):
   print("Comparison metrics")
   print("------------------")
   predictions = model.predict(x)
   print("Validation MSE Acc:   " + str(mse_all(predictions, y)))
   print("No Change MSE Acc:    " + str(mse_all(x, y)))
   averages = get_averages(x)
   print("Regr to mean MSE Acc: " + str(mse_all([[(averages[i] + p[i]) / 2 for i in range(len(x[0]))] for p in x], y)))
   print("Pseudo Rand MSE Acc:  " + str(mse_all([p + random.uniform(0.0, 0.1) for p in x], y)))
   print("Full Rand MSE Acc:    " + str(mse_all([random.uniform(0.0, 1.0, size=len(y[0])) for i in range(len(y))], y)))


#
# Main
#
def get_predictor(prep = 0, proj = 1):
   global PREP_SEASON, PROJ_SEASON
   PREP_SEASON = prep
   PROJ_SEASON = proj
   # get players from shelved player_store
   (X, Y) = get_player_sets()
   model = get_model(len(X[0]), len(Y[0]))
   model.summary()
   print("\n\nGetting new model...")
   print("Epochs: " + str(EPOCHS) + ", Batch Size: " + str(BATCH_SIZE) + ", Folds: " + str(FOLDS) + "\n")
   print_glossary()
   kfold = StratifiedKFold(n_splits=FOLDS, shuffle=True)
   scores = []
   for i, (train, test) in enumerate(kfold.split(X, Y.argmax(1))):
      model.fit(X[train], Y[train], epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=0)
      score = model.evaluate(X[test], Y[test], verbose=0)
      print("\nloss after fold " + str(i+1) + ": " + str(round(score, 5)))
      scores.append(score)
   print("\nave: " + str(round(sum(scores)/len(scores), 5)))
   compare_acc(X, Y, model)
   # predictions = model.predict(X)
   return model


# if __name__ == "__main__":
   # main()
