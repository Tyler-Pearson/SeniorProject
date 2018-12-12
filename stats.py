
def mse_calc(proj, actual):
   ms = 0
   for i in range(len(proj)):
      ms += (actual[i] - proj[i]) ** 2
   return ms / len(proj)

def mse_all(projs, actuals):
   return round(sum([mse_calc(projs[i], actuals[i]) for i in range(len(projs))]) / len(projs), 4)

def norm(l):
   l[0] /= 50.0
   l[1] /= 82.0
   l[2] /= 48.0
   l[3] /= 50.0
   l[5] /= 50.0
   l[7] /= 50.0
   l[9] /= 50.0
   l[11] /= 50.0
   l[12] /= 50.0
   l[13] /= 50.0
   l[14] /= 50.0
   l[15] /= 50.0
   l[16] /= 50.0
   l[17] /= 6.0
   l[18] /= 50.0
   return [round(x, 3) for x in l]

def denorm(l):
   l[0] *= 50.0
   l[1] *= 82.0
   l[2] *= 48.0
   l[3] *= 50.0
   l[5] *= 50.0
   l[7] *= 50.0
   l[9] *= 50.0
   l[11] *= 50.0
   l[12] *= 50.0
   l[13] *= 50.0
   l[14] *= 50.0
   l[15] *= 50.0
   l[16] *= 50.0
   l[17] *= 6.0
   l[18] *= 50.0
   return [round(x, 3) for x in l]

# All fields in .xlsx files except Player name string
class Season:

   def __init__(self, age, g, mp, fga, fgp, threepa, threepp, twopa,
                twopp, fta, ftp, orb, drb, ast, stl, blk, tov, pf, ppg):
      self.age = round(age/50.0, 3)
      self.g = round(g/82.0, 3)
      self.mp = round(mp/48.0, 3)
      self.fga = round(fga/50.0, 3)
      self.fgp = round(fgp, 3)
      self.threepa = round(threepa/50.0, 3)
      self.threepp = round(threepp, 3)
      self.twopa = round(twopa/50.0, 3)
      self.twopp = round(twopp, 3)
      self.fta = round(fta/50.0, 3)
      self.ftp = round(ftp, 3)
      self.orb = round(orb/50.0, 3)
      self.drb = round(drb/50.0, 3)
      self.ast = round(ast/50.0, 3)
      self.stl = round(stl/50.0, 3)
      self.blk = round(blk/50.0, 3)
      self.tov = round(tov/50.0, 3)
      self.pf = round(pf/6.0, 3)
      self.ppg = round(ppg/50.0, 3)

   def denorm(self):
      self.age = age*50.0
      self.g = g*82.0
      self.mp = mp*48.0
      self.fga = fga*50.0
      self.threepa = threepa*50.0
      self.twopa = twopa*50.0
      self.fta = fta*50.0
      self.orb = orb*50.0
      self.drb = drb*50.0
      self.ast = ast*50.0
      self.stl = stl*50.0
      self.blk = blk*50.0
      self.tov = tov*50.0
      self.pf = pf*6.0
      self.ppg = ppg*50.0

   def to_denorm_list(self):
      l = [self.age*50.0, self.g*82.0, self.mp*48.0, self.fga*50.0, self.fgp,
                self.threepa*50.0, self.threepp, self.twopa*50.0, self.twopp,
                self.fta*50.0, self.ftp, self.orb*50.0, self.drb*50.0,
                self.ast*50.0, self.stl*50.0, self.blk*50.0, self.tov*50.0,
                self.pf*6.0, self.ppg*50.0]
      return [round(el, 3) for el in l]

   def to_list(self):
      return [self.age, self.g, self.mp, self.fga, self.fgp, self.threepa,
                self.threepp, self.twopa, self.twopp, self.fta, self.ftp,
                self.orb, self.drb, self.ast, self.stl, self.blk, self.tov,
                self.pf, self.ppg]


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
         max(season.age*50.0 for season in self.seasons),
         max(season.g*82.0 for season in self.seasons),
         max(season.mp*48.0 for season in self.seasons),
         max(season.fga*50.0 for season in self.seasons),
         max(season.fgp for season in self.seasons),
         max(season.threepa*50.0 for season in self.seasons),
         max(season.threepp for season in self.seasons),
         max(season.twopa*50.0 for season in self.seasons),
         max(season.twopp for season in self.seasons),
         max(season.fta*50.0 for season in self.seasons),
         max(season.ftp for season in self.seasons),
         max(season.orb*50.0 for season in self.seasons),
         max(season.drb*50.0 for season in self.seasons),
         max(season.ast*50.0 for season in self.seasons),
         max(season.stl*50.0 for season in self.seasons),
         max(season.blk*50.0 for season in self.seasons),
         min(season.tov*50.0 for season in self.seasons),
         min(season.pf*6.0 for season in self.seasons),
         max(season.ppg*50.0 for season in self.seasons)
         )

   # Get season of averages of first n seasons
   def getAverageOf(self, n):
      if (n > len(self.seasons)):
         raise ValueError('Not enough seasons ' + self.name + ' ' +
            str(len(self.seasons)) + ' - ' + str(n))
      n_seasons = self.seasons[:n]
      return Season(
         sum([season.age*50.0 for season in n_seasons]) / n,
         sum([season.g*82.0 for season in n_seasons]) / n,
         sum([season.mp*48.0 for season in n_seasons]) / n,
         sum([season.fga*50.0 for season in n_seasons]) / n,
         sum([season.fgp for season in n_seasons]) / n,
         sum([season.threepa*50.0 for season in n_seasons]) / n,
         sum([season.threepp for season in n_seasons]) / n,
         sum([season.twopa*50.0 for season in n_seasons]) / n,
         sum([season.twopp for season in n_seasons]) / n,
         sum([season.fta*50.0 for season in n_seasons]) / n,
         sum([season.ftp for season in n_seasons]) / n,
         sum([season.orb*50.0 for season in n_seasons]) / n,
         sum([season.drb*50.0 for season in n_seasons]) / n,
         sum([season.ast*50.0 for season in n_seasons]) / n,
         sum([season.stl*50.0 for season in n_seasons]) / n,
         sum([season.blk*50.0 for season in n_seasons]) / n,
         sum([season.tov*50.0 for season in n_seasons]) / n,
         sum([season.pf*6.0 for season in n_seasons]) / n,
         sum([season.ppg*50.0 for season in n_seasons]) / n
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
