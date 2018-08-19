
# All fields in .xlsx files except Player name string
class Season:

   def __init__(self, age, g, mp, fga, fgp, threepa, threepp, twopa,
                twopp, fta, ftp, orb, drb, ast, stl, blk, tov, pf, ppg):
      self.age = age
      self.g = g
      self.mp = mp
      self.fga = fga
      self.fgp = fgp
      self.threepa = threepa
      self.threepp = threepp
      self.twopa = twopa
      self.twopp = twopp
      self.fta = fta
      self.ftp = ftp
      self.orb = orb
      self.drb = drb
      self.ast = ast
      self.stl = stl
      self.blk = blk
      self.tov = tov
      self.pf = pf
      self.ppg = ppg
   

# Player name plus array of their seasons (must maintain order)
class Player:

   def __init__(self, name, rookie_season):
      self.name = name
      self.seasons = [rookie_season]
      if '*' in name:
         self.hof = True
      else:
         self.hof = False

   # Compares Player against String - to avoid needing to create
   # a new Player object while adding a season to PlayerStore
   def __eq__(self, other):
      return (self.name == other)
      
   # Set self.max_season to a Season object of the best stat in
   # each statistical category of the player's seasons
   def setMaxSeason(self):
      self.max_season = Season(
         max(season.age for season in self.seasons),
         max(season.g for season in self.seasons),
         max(season.mp for season in self.seasons),
         max(season.fga for season in self.seasons),
         max(season.fgp for season in self.seasons),
         max(season.threepa for season in self.seasons),
         max(season.threepp for season in self.seasons),
         max(season.twopa for season in self.seasons),
         max(season.twopp for season in self.seasons),
         max(season.fta for season in self.seasons),
         max(season.ftp for season in self.seasons),
         max(season.orb for season in self.seasons),
         max(season.drb for season in self.seasons),
         max(season.ast for season in self.seasons),
         max(season.stl for season in self.seasons),
         max(season.blk for season in self.seasons),
         max(season.tov for season in self.seasons),
         max(season.pf for season in self.seasons),
         max(season.ppg for season in self.seasons)
         )


# Array of Players - to be shelved
class PlayerStore:

   def __init__(self):
      self.players = []

   # Add Season - takes a player name plus season,
   # if player in players array, append season to player's seasons array
   # if not, create player and append to players array
   def addSeason(self, name, season):
      if (name in self.players):
         ind = self.players.index(name)
         self.players[ind].seasons.append(season)
         #print("Adding season to end of " + name)
      else:
         self.players.append(Player(name, season))
         #print("Adding player " + name + " to PlayerStore")
         
   # Call at end of parsing to set the max season for every player in
   # the self.players list
   def setMaxes(self):
      for player in self.players:
         player.setMaxSeason()
