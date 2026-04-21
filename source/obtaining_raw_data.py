""" obtaining_raw_data.py         damiancclarke            yyyy-mm-dd:2026-03-20
---|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8

  This file creates the basic raw data that will be used as the backbone to the rest of the raw data and subsequently for the rest of the project

  The data comes from the table from each year from the Six Nations Rugby website where we copied the result table gtom each year.
https://www.sixnationsrugby.com/en/m6n/fixtures/202600/table

At times where the table was unclear, I used the corresponding results table from https://www.rugbypass.com/six-nations/history/ 

This code will create the basic raw data and save into the data folder. 
In order to replicate this file, the only required change is the ROOT directory, indicated on line 25.
The basic raw data can, however, simply be obtained from the GitHub repo - this code is only for the creation.

Full details related to the replication of this file can be found in the README code in the top level of this directory.

"""

#------------------------------------------------------------------------------
#--- (0) Imports the necessary librarys
#------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import os

ROOT = "/home/hcross27/BEE2041/Emperical_Project/Harrison-Cross---BEE2041-Emperical-Project-Repo/"

DAT  = ROOT+'data/'

#------------------------------------------------------------------------------
#--- (1) Creating the columns that will be used in the dataframe
#------------------------------------------------------------------------------


results_table_columns = [
    'team', 'year', 'final_position', 'grand_slam',
    'matches_won', 'matches_lost', 'matches_drawn',
    'points_scored', 'points_conceded', 'points_difference',
    'tries_scored', 'tries_conceded'
]

#------------------------------------------------------------------------------
#--- (2) Pasting the data into a nested list to be later put into the dataframe
#------------------------------------------------------------------------------

results_table_perYear = [
    # format for each list: Team, Year, Position, Gram Slam (1 = Yes, 0 = No), matches Won, matches Lost, matches Drawn, points for, points against, point difference, tries for, tries against
    
    #results for the year...
    # 2000
    ['England', 2000, 1, 0, 4, 1, 0, 183, 70, 113, 20, 5],
    ['France', 2000, 2, 'N/A', 3, 2, 0, 140, 92, 48, 12, 8],
    ['Ireland', 2000, 3, 'N/A', 3, 2, 0, 168, 133, 35, 17, 13],
    ['Wales', 2000, 4, 'N/A', 3, 2, 0, 111, 135, -24, 8, 12],
    ['Scotland', 2000, 5, 'N/A', 1, 4, 0, 95, 145, -50, 9, 12],
    ['Italy', 2000, 6, 'N/A', 1, 4, 0, 106, 228, -122, 9, 25],


    #results for the year...
    # 2001
    ['England', 2001, 1, 0, 4, 1, 0, 229, 80, 149, 29, 6],
    ['Ireland', 2001, 2, 'N/A', 4, 1, 0, 129, 89, 40, 11, 10],
    ['Scotland', 2001, 3, 'N/A', 2, 2, 1, 92, 116, -24, 8, 10],
    ['Wales', 2001, 4, 'N/A', 2, 2, 1, 125, 166, -41, 10, 15],
    ['France', 2001, 5, 'N/A', 2, 3, 0, 115, 138, -23, 9, 12],
    ['Italy', 2001, 6, 'N/A', 0, 5, 0, 106, 207, -101, 8, 22],


    #results for the year...
    # 2002
    ['France', 2002, 1, 1, 5, 0, 0, 156, 75, 81, 15, 7],
    ['England', 2002, 2, 'N/A', 4, 1, 0, 184, 53, 131, 23, 4],
    ['Ireland', 2002, 3, 'N/A', 3, 2, 0, 145, 138, 7, 16, 15],
    ['Scotland', 2002, 4, 'N/A', 2, 3, 0, 91, 128, -37, 6, 13],
    ['Wales', 2002, 5, 'N/A', 1, 4, 0, 119, 188, -69, 11, 18],
    ['Italy', 2002, 6, 'N/A', 0, 5, 0, 70, 183, -113, 4, 18],


    #results for the year...
    # 2003
    ['England', 2003, 1, 1, 5, 0, 0, 173, 46, 127, 18, 4],
    ['Ireland', 2003, 2, 'N/A', 4, 1, 0, 119, 97, 22, 10, 9],
    ['France', 2003, 3, 'N/A', 3, 2, 0, 153, 75, 78, 17, 6],
    ['Scotland', 2003, 4, 'N/A', 2, 3, 0, 81, 161, -80, 7, 17],
    ['Italy', 2003, 5, 'N/A', 1, 4, 0, 100, 185, -85, 12, 25],
    ['Wales', 2003, 6, 'N/A', 0, 5, 0, 82, 144, -62, 10, 13],


    #results for the year...
    # 2004
    ['France', 2004, 1, 1, 5, 0, 0, 144, 60, 84, 14, 5],
    ['Ireland', 2004, 2, 'N/A', 4, 1, 0, 128, 82, 46, 17, 8],
    ['England', 2004, 3, 'N/A', 3, 2, 0, 150, 86, 64, 17, 6],
    ['Wales', 2004, 4, 'N/A', 2, 3, 0, 125, 116, 9, 14, 13],
    ['Italy', 2004, 5, 'N/A', 1, 4, 0, 42, 152, -110, 2, 20],
    ['Scotland', 2004, 6, 'N/A', 0, 5, 0, 53, 146, -93, 4, 16],


    #results for the year...
    # 2005
    ['Wales', 2005, 1, 1, 5, 0, 0, 151, 77, 74, 17, 8],
    ['France', 2005, 2, 'N/A', 4, 1, 0, 134, 82, 52, 13, 6 ],
    ['Ireland', 2005, 3, 'N/A', 3, 2, 0, 126, 101, 25, 12, 9],
    ['England', 2005, 4, 'N/A', 2, 3, 0, 121, 77, 44, 16, 6],
    ['Scotland', 2005, 5, 'N/A', 1, 4, 0, 84, 155, -71, 8, 20],
    ['Italy', 2005, 6, 'N/A', 0, 5, 0, 55, 179, -124, 5, 22],


    #results for the year...
    # 2006
    ['France', 2006, 1, 0, 4, 1, 0, 148, 85, 63, 18, 7],
    ['Ireland', 2006, 2, 'N/A', 4, 1, 0, 131, 97, 34, 12, 10],
    ['Scotland', 2006, 3, 'N/A', 3, 2, 0, 78, 81, -3, 5, 7],
    ['England', 2006, 4, 'N/A', 2, 3, 0, 120, 106, 14, 12, 8],
    ['Wales', 2006, 5, 'N/A', 1, 3, 1, 80, 135, -55, 9, 15],
    ['Italy', 2006, 6, 'N/A', 0, 4, 1, 72, 125, -53, 5, 14],


    #results for the year...    
    # 2007
    ['France', 2007, 1, 0, 4, 1, 0, 155, 86, 69, 15, 9],
    ['Ireland', 2007, 2, 'N/A', 4, 1, 0, 149, 84, 65, 17, 5],
    ['England', 2007, 3, 'N/A', 3, 2, 0, 119, 115, 4, 10, 9],
    ['Italy', 2007, 4, 'N/A', 2, 3, 0, 94, 147, -53, 9, 18],
    ['Wales', 2007, 5, 'N/A', 1, 4, 0, 86, 113, -27, 7, 9],
    ['Scotland', 2007, 6, 'N/A', 1, 4, 0, 95, 153, -58, 7, 15],


    #results for the year...
    # 2008
    ['Wales', 2008, 1, 1, 5, 0, 0, 148, 66, 82, 13, 2],
    ['England', 2008, 2, 'N/A', 3, 2, 0, 108, 83, 25, 8, 5],
    ['France', 2008, 3, 'N/A', 3, 2, 0, 103, 93, 10, 11, 7],
    ['Ireland', 2008, 4, 'N/A', 2, 3, 0, 93, 99, -6, 9, 10],
    ['Scotland', 2008, 5, 'N/A', 1, 4, 0, 69, 123, -54, 3, 13],
    ['Italy', 2008, 6, 'N/A', 1, 4, 0, 74, 131, -57, 6, 13],


    #results for the year...
    # 2009
    ['Ireland', 2009, 1, 1, 5, 0, 0, 121, 73, 48, 12, 3],
    ['England', 2009, 2, 'N/A', 3, 2, 0, 124, 70, 54, 16, 5],
    ['France', 2009, 3, 'N/A', 3, 2, 0, 124, 101, 23, 14, 11],
    ['Wales', 2009, 4, 'N/A', 3, 2, 0, 100, 81, 19, 8, 7],
    ['Scotland', 2009, 5, 'N/A', 1, 4, 0, 79, 102, -23, 4, 9],
    ['Italy', 2009, 6, 'N/A', 0, 5, 0, 49, 170, -121, 2, 21],


    #results for the year...
    # 2010
    ['France', 2010, 1, 1, 5, 0, 0, 135, 69, 66, 13, 6],
    ['Ireland', 2010, 2, 'N/A', 3, 2, 0, 106, 95, 11, 11, 6],
    ['England', 2010, 3, 'N/A', 2, 2, 1, 88, 76, 12, 6, 5],
    ['Wales', 2010, 4, 'N/A', 2, 3, 0, 113, 117, -4, 10, 11],
    ['Scotland', 2010, 5, 'N/A', 1, 3, 1, 83, 100, -17, 3, 8],
    ['Italy', 2010, 6, 'N/A', 1, 4, 0, 69, 137, -68, 5, 12],


    #results for the year...
    # 2011
    ['England', 2011, 1, 0, 4, 1, 0, 132, 81, 51, 13, 5],
    ['France', 2011, 2, 'N/A', 3, 2, 0, 117, 91, 26, 10, 8],
    ['Ireland', 2011, 3, 'N/A', 3, 2, 0, 93, 81, 12, 10, 4],
    ['Wales', 2011, 4, 'N/A', 3, 2, 0, 95, 89, 6, 6, 8],
    ['Scotland', 2011, 5, 'N/A', 1, 4, 0, 82, 109, -27, 6, 11],
    ['Italy', 2011, 6, 'N/A', 1, 4, 0, 70, 138, -68, 6, 15],


    #results for the year...
    # 2012
    ['Wales', 2012, 1, 1, 5, 0, 0, 109, 58, 51, 10, 3],
    ['England', 2012, 2, 'N/A', 4, 1, 0, 98, 71, 27, 7, 4],
    ['Ireland', 2012, 3, 'N/A', 2, 2, 1, 121, 94, 27, 13, 8],
    ['France', 2012, 4, 'N/A', 2, 2, 1, 101, 86, 15, 8, 8],
    ['Italy', 2012, 5, 'N/A', 1, 4, 0, 53, 121, -68, 4, 12],
    ['Scotland', 2012, 6, 'N/A', 0, 5, 0, 56, 108, -52, 4, 11],


    #results for the year...
    # 2013
    ['Wales', 2013, 1, 0, 4, 1, 0, 122, 66, 56, 9, 3],
    ['England', 2013, 2, 'N/A', 4, 1, 0, 94, 78, 16, 5, 6],
    ['Scotland', 2013, 3, 'N/A', 2, 3, 0, 98, 107, -9, 7, 9],
    ['Italy', 2013, 4, 'N/A', 2, 3, 0, 75, 111, -36, 5, 8],
    ['Ireland', 2013, 5, 'N/A', 1, 3, 1, 72, 81, -9, 5, 5],
    ['France', 2013, 6, 'N/A', 1, 3, 1, 73, 91, -18, 6, 6],
    
    
    #results for the year...
    #2014
    ['Ireland', 2014, 1, 0, 4, 1, 0, 132, 49, 83, 16, 4],
    ['England', 2014, 2, 'N/A', 4, 1, 0, 138, 65, 73, 14, 5],
    ['Wales', 2014, 3, 'N/A', 3, 2, 0, 122, 79, 43, 11, 6],
    ['France', 2014, 4, 'N/A', 3, 2, 0, 101, 100, 1, 9, 10],
    ['Scotland', 2014, 5, 'N/A', 1, 4, 0, 47, 138, -91, 4, 15],
    ['Italy', 2014, 6, 'N/A', 0, 5, 0, 63, 172, -109, 7, 21],


    #results for the year...
    # 2015
    ['Ireland', 2015, 1, 0, 4, 1, 0, 119, 56, 63, 8, 3],
    ['England', 2015, 2, 'N/A', 4, 1, 0, 157, 100, 57, 18, 11],
    ['Wales', 2015, 3, 'N/A', 4, 1, 0, 146, 93, 53, 13, 8],
    ['France', 2015, 4, 'N/A', 2, 3, 0, 103, 101, 2, 9, 9],
    ['Italy', 2015, 5, 'N/A', 1, 4, 0, 62, 182, -120, 8, 19],
    ['Scotland', 2015, 6, 'N/A', 0, 5, 0, 73, 128, -55, 6, 12],


    #results for the year...
    # 2016
    ['England', 2016, 1, 1, 5, 0, 0, 132, 70, 62, 13, 4],
    ['Wales', 2016, 2, 'N/A', 3, 1, 1, 150, 88, 62, 17, 7],
    ['Ireland', 2016, 3, 'N/A', 2, 2, 1, 128, 87, 41, 15, 9],
    ['Scotland', 2016, 4, 'N/A', 2, 3, 0, 122, 115, 7, 11, 13],
    ['France', 2016, 5, 'N/A', 2, 3, 0, 82, 109, -27, 7, 9],
    ['Italy', 2016, 6, 'N/A', 0, 5, 0, 79, 224, -145, 8, 29],


    #results for the year...
    # 2017
    ['England', 2017, 1, 0, 4, 1, 0, 146, 81, 65, 16, 8],
    ['Ireland', 2017, 2,'N/A', 3, 2, 0, 126, 77, 49, 14, 7],
    ['France', 2017, 3, 'N/A', 3, 2, 0, 107, 90, 17, 8, 6],
    ['Scotland', 2017, 4, 'N/A', 3, 2, 0, 122, 118, 4, 14, 12],
    ['Wales', 2017, 5, 'N/A', 2, 3, 0, 102, 86, 16, 8, 7],
    ['Italy', 2017, 6, 'N/A', 0, 5, 0, 50, 201, -151, 6, 26],


    #results for the year...
    # 2018
    ['Ireland', 2018, 1, 1, 5, 0, 0, 160, 82, 78, 20, 11],
    ['Wales', 2018, 2, 'N/A', 3, 2, 0, 119, 83, 36, 13, 11],
    ['Scotland', 2018, 3, 'N/A', 3, 2, 0, 101, 128, -27, 11, 14],
    ['France', 2018, 4, 'N/A', 2, 3, 0, 108, 94, 14, 8, 6],
    ['England', 2018, 5, 'N/A', 2, 3, 0, 102, 92, 10, 14, 9],
    ['Italy', 2018, 6, 'N/A', 0, 5, 0, 92, 203, -111, 12, 27],


    #results for the year...
    # 2019
    ['Wales', 2019, 1, 1, 5, 0, 0, 114, 65, 49, 10, 7],
    ['England', 2019, 2, 'N/A', 3, 1, 1, 184, 101, 83, 24, 13],
    ['Ireland', 2019, 3, 'N/A', 3, 2, 0, 101, 100, 1, 14, 10],
    ['France', 2019, 4, 'N/A', 2, 3, 0, 93, 118, -25, 12, 15],
    ['Scotland', 2019, 5, 'N/A', 1, 3, 1, 105, 125, -20, 14, 17],
    ['Italy', 2019, 6, 'N/A', 0, 5, 0, 79, 167, -88, 10, 22],


    #results for the year...
    # 2020
    ['England', 2020, 1, 0, 4, 1, 0, 121, 77, 44, 14, 9],
    ['France', 2020, 2, 'N/A', 4, 1, 0, 138, 117, 21, 17, 13],
    ['Ireland', 2020, 3, 'N/A', 3, 2, 0, 132, 102, 30, 17, 11],
    ['Scotland', 2020, 4, 'N/A', 3, 2, 0, 77, 59, 18, 7, 5],
    ['Wales', 2020, 5, 'N/A', 1, 4, 0, 119, 98, 21, 13, 11],
    ['Italy', 2020, 6, 'N/A', 0, 5, 0, 44, 178, -134, 6, 25],
    

    #results for the year...
    # 2021
    ['Wales', 2021, 1, 0, 4, 1, 0, 164, 103, 61, 20, 11],
    ['France', 2021, 2, 'N/A', 3, 2, 0, 140, 103, 37, 18, 10],
    ['Ireland', 2021, 3, 'N/A', 3, 2, 0, 136, 88, 48, 12, 10],
    ['Scotland', 2021, 4, 'N/A', 3, 2, 0, 138, 91, 47, 18, 10],
    ['England', 2021, 5, 'N/A', 2, 3, 0, 112, 121, -9, 12, 11],
    ['Italy', 2021, 6, 'N/A', 0, 5, 0, 55, 239, -184, 6, 34],


    #results for the year...
    # 2022
    ['France', 2022, 1, 1, 5, 0, 0, 141, 73, 68, 17, 7],
    ['Ireland', 2022, 2, 'N/A', 4, 1, 0, 168, 63, 105, 24, 4],
    ['England', 2022, 3, 'N/A', 2, 3, 0, 101, 96, 5, 8, 12],
    ['Scotland', 2022, 4, 'N/A', 2, 3, 0, 92, 121, -29, 11, 15],
    ['Wales', 2022, 5, 'N/A', 1, 4, 0, 76, 104, -28, 8, 8],
    ['Italy', 2022, 6, 'N/A', 1, 4, 0, 60, 181, -121, 5, 27],


    #results for the year...
    # 2023
    ['Ireland', 2023, 1, 1, 5, 0, 0, 151, 72, 79, 20, 6],
    ['France', 2023, 2, 'N/A', 4, 1, 0, 174, 115, 59, 21, 14],
    ['Scotland', 2023, 3, 'N/A', 3, 2, 0, 118, 98, 20, 17, 12],
    ['England', 2023, 4, 'N/A', 2, 3, 0, 100, 135, -35, 13, 18],
    ['Wales', 2023, 5, 'N/A', 1, 4, 0, 84, 147, -63, 11, 19],
    ['Italy', 2023, 6, 'N/A', 0, 5, 0, 89, 149, -60, 9, 22],


    #results for the year...
    # 2024
    ['Ireland', 2024, 1, 0, 4, 1, 0, 144, 60, 84, 19, 7],
    ['France', 2024, 2, 'N/A', 3, 1, 1, 128, 122, 6, 13, 14],
    ['England', 2024, 3, 'N/A', 3, 2, 0, 118, 123, -5, 13, 13],
    ['Scotland', 2024, 4, 'N/A', 2, 3, 0, 115, 115, 0, 12, 13],
    ['Italy', 2024, 5, 'N/A', 2, 2, 1, 92, 126, -34, 9, 16],
    ['Wales', 2024, 6, 'N/A', 0, 5, 0, 92, 143, -51, 13, 16],


    #results for the year...
    # 2025
    ['France', 2025, 1, 0, 4, 1, 0, 218, 93, 125, 30, 11],
    ['England', 2025, 2, 'N/A', 4, 1, 0, 179, 105, 74, 25, 15],
    ['Ireland', 2025, 3, 'N/A', 4, 1, 0, 135, 117, 18, 17, 14],
    ['Scotland', 2025, 4, 'N/A', 2, 3, 0, 115, 131, -16, 16, 14],
    ['Italy', 2025, 5, 'N/A', 1, 4, 0, 106, 188, -82, 10, 29],
    ['Wales', 2025, 6, 'N/A', 0, 5, 0, 76, 195, -119, 10, 25],


    #results for the year...
    # 2026
    ['France', 2026, 1, 0, 4, 1, 0, 211, 130, 81, 30, 19],
    ['Ireland', 2026, 2, 'N/A', 4, 1, 0, 146, 108, 38, 20, 14],
    ['Scotland', 2026, 3, 'N/A', 3, 2, 0, 143, 144, -1, 20, 18],
    ['Italy', 2026, 4, 'N/A', 2, 3, 0, 79, 117, -38, 9, 16],
    ['England', 2026, 5, 'N/A', 1, 4, 0, 153, 151, 2, 21, 18],
    ['Wales', 2026, 6, 'N/A', 1, 4, 0, 90, 172, -82, 11, 26],
]


#------------------------------------------------------------------------------
#--- (3) Collecting the nest lists and the columns and feeding them into the data frame
#------------------------------------------------------------------------------



collective_results_table_df = pd.DataFrame(results_table_perYear, columns=results_table_columns)


#------------------------------------------------------------------------------
#--- (4) Reordering the data by most recent downwards and then alphabetically and feeding into a new dataframe
#------------------------------------------------------------------------------

basic_raw_datad_df = collective_results_table_df.sort_values(
    by=['year', 'team'],
    ascending=[False, True]
).reset_index(drop=True)


print(basic_raw_datad_df.head(20))          # outputting the top 20 rows to test


#------------------------------------------------------------------------------
#--- (5) Saving the new dataframe into a csv to be the basic raw data
#------------------------------------------------------------------------------

basic_raw_datad_df.to_csv(DAT + "Six_Nations-basic_raw_data.csv", index=False)


