import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


XL_EXT = '.xlsx'
YEAR_START = 1979
YEAR_END = 2017


def list_comp(l1, l2):
   if not (len(l1) == len(l2)):
      return False
   for i in range(len(l1)):
      if not (l1[i] == l2[i]):
         return False
   return True

def verify_cols():
   print("\nExpected Column Headings:")
   filename_end = str(YEAR_END) + XL_EXT
   df_correct = pd.read_excel(filename_end)
   col_correct = df_correct.columns
   print("   " + filename_end + ":", col_correct)

   print("Cross-verifying all years:")
   for i in range(YEAR_START, YEAR_END):
      filename_cur = str(i) + XL_EXT
      df_cur = pd.read_excel(filename_cur)
      col_cur = df_cur.columns
      if (list_comp(col_cur, col_correct)):
         print("   " + filename_cur + " verified.")
      else:
         print(filename_cur + "incorrect:")
         print("   ", col_cur)


def main():
   print("\nhi. let's parse")
   verify_cols()
   print("\n")


if __name__ == "__main__":
   main()
