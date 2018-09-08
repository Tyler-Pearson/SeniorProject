import shelve
from stats import *
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation


print("hi")
print("let's make some predictions!\n")


# Return players list from shelved player_store
def get_players(seasons_played):
   ps = shelve.open('player_store')
   players = ps['store'].players
   ps.close()
   return [player for player in players if (len(player.seasons) > seasons_played)]


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
         
def get_model():
   model = Sequential()
   model.add(Dense(19, activation=tf.nn.relu))
   model.add(Dense(19, activation=tf.nn.relu))
   model.add(Dense(19))
   return model


# Main
def main():
   players = get_players(1) # get players from shelved player_store
   # model = get_model()
   # p = players[2401]
   # s = p.max_season
   # print(p.name, s.age, s.ftp, s.threepa, s.ppg)
   check_ages(players) # verify player list usability


if __name__ == "__main__":
   main()

