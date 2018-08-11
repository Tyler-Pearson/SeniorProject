import shelve
from stats import *


print("hi")
print("let's make some predictions!")


# Return players list from shelved player_store
def unpack_player_stats():
   ps = shelve.open('player_store')
   players = ps['store'].players
   ps.close()
   return players


# Verify shelving/unshelving occured properly
# Check ages of players as rookies
def check_ages(players):
   # print total number of players
   print(str(len(players)) + " total players")

   print("Checking ages:")
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
      if (i > 27 and ages[i]):
         print(ages[i]) # list of tuples [(Name, Seasons played), ...]


# Main
def main():
   players = unpack_player_stats() # get players from shelved player_store
   check_ages(players) # verify player list usability


if __name__ == "__main__":
   main()

