import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from stats import *


# Defines
XL_EXT = '.xlsx'
YEAR_START = 1979
YEAR_END = 2017


# Helper function for verify_cols, compares 2 lists
def list_comp(l1, l2):
   # compare lengths to avoid index out of bounds
   if not (len(l1) == len(l2)):
      return False
   # compare each element
   for i in range(len(l1)):
      if not (l1[i] == l2[i]):
         return False
   return True

# Verify the column headers of all season xlsx files against
# most recent. Assumes most recent has correct headers
def verify_cols():
   invalids = []
   print("\nExpected Column Headings:")
   filename_end = str(YEAR_END) + XL_EXT
   # read in data file of most recent year
   df_correct = pd.read_excel(filename_end)
   # read in column headers
   col_correct = df_correct.columns
   print("   " + filename_end + ":", col_correct)

   print("Cross-verifying all years:")
   # iterate through all season xlsx files
   for i in range(YEAR_START, YEAR_END):
      filename_cur = str(i) + XL_EXT
      # get file data
      df_cur = pd.read_excel(filename_cur)
      # get column headers
      col_cur = df_cur.columns
      # check if cur headers == most recent
      if (list_comp(col_cur, col_correct)):
         print("   " + filename_cur + " verified.")
      else:
         invalids.append(filename_cur)
         print(filename_cur + "incorrect:")
         print("   ", col_cur)

   if (invalids):
      print("Invalids:", invalids)
      return False
   else:
      print("All headers valid")
      return True


# main
def main():
   print("\nhi. let's parse")
   if not (verify_cols()):
      print("Fix invalid headers\n")
      return
   print("\n")


if __name__ == "__main__":
   main()
