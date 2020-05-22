def f_table_creation():
    """Creates a F-table using data from the web

    Returns:
        f_table {dictionary} -- f-table for the alpha value requested by the user 
    """
    url2 = "http://www.socr.ucla.edu/Applets.dir/F_Table.html" #F-table from the web
    r2 = requests.get(url2) #Pull the html data
    soup = BeautifulSoup(r2.content,'html.parser').prettify() #Parse the html data into a string
    #Remove html specific coding from the string
    pattern = r"<(.+)>\s" #Patter for html spefic coding
    new_soup = re.sub(pattern, '', soup) #Remove html specific coding 
    new_soup = re.findall(r"[^s]", new_soup) #Turn the string into a list with individual characters
    #Reconstruct values in for a new list by combining the characters back into their intended values
    new_entry = ''
    table = []
    for character in new_soup: #Iterate through the list 
        if character == '\t': #pass whitespace
            pass
        elif character == " ": #pass whitespace
            pass
        elif character == '\n': #If its a new line, add the new value
            table.append(new_entry)
            new_entry = ''
        else: #Add the individual numbers to the create the t-statistic
            new_entry += character
    f_table_data = F_Table(table)
    f_alpha_value = str(f_table_data.alpha)
    f_table = f_table_data.table_extraction()
    return f_table,f_alpha_value

class F_Table():
    #Choices for different alpha values
    alpha_values = '\nPlease choose the alpha value you wish to use with this analysis: \n1) 0.10 \n2) 0.05 \n3) 0.025 \n4) 0.01 \n5) 0.001'
    alpha_options = {1 : '0.10', 2 : '0.05', 3 : '0.025', 4 : '0.01', 5 : '0.001'}
    def __init__(self,html_data):
        self.html_data = html_data
        self.alpha = self.alpha_options[choice_validation(self.alpha_values)] #Allow user to pick an alpha value
    #Extract the F-table needed for the analysis 
    def table_extraction(self):
        """Pulls the F-table needed for the analysis depending on the alpha value choosen by the user

        Returns:
            f_table_final [dictionary] -- f-table where every key is a df1 column 
        """
        #Extract the section of data needed to create the F-table
        f_table = []
        start_extraction = 0
        pattern = r'^for.=%s' % self.alpha #Pattern for endding the extraction
        for value in self.html_data:
            if start_extraction == 1 and (value == 'F' or re.match(r'FTablefor.=0.001',value)): #End extraction after the table is complete
                break
            if start_extraction == 1:
                f_table.append(value)
            if re.match(pattern,value) or value == 'DF': #Start extraction 
                start_extraction = 1
        #Remove unneeded values from the table 
        index = -1
        f_table_refined = []
        pass_next = 0
        for value in f_table:
            index += 1
            if pass_next == 1: #Skip this value 
                pass_next = 0
            else:
                if '=' in value: #If there is an equal sign, only append the numeric components after the equal sign
                    new_entry = ''
                    skip = 0 #Skip values before the equal sign
                    for character in value:
                        if skip == 1:
                            new_entry += character #Combine the numeric components after the equal sign
                        if character == '=': 
                            skip = 1 #Start adding now that equal sign has passed
                    f_table_refined.append(new_entry) #append the new entry
                elif value == '∞':
                    f_table_refined.append('infinity')
                elif value == 'df': #df has a subscript for df1 and df2. Only need the value, skip the rest
                    pass_next = 1
                elif value == 'DF': #Last F-table on the web page has DF instead of df 
                    pass
                else:
                    try: #If the value is not a number, don't add it e.g.) 't'
                        new_entry = float(value) 
                        f_table_refined.append(value)
                    except:
                        pass #pass values that are not numbers
                if value == '1' and f_table[(index - 1)] == '1.44681197': #Disregard everything following the last value for the last F-table on the web page
                    break
        #Create lists for each df1 value's t_stat per df2 value
        df1_1 = []
        df1_2 = []
        df1_3 = []
        df1_4 = []
        df1_5 = []
        df1_6 = []
        df1_7 = []
        df1_8 = []
        df1_9 = []
        df1_10 = []
        df1_12 = []
        df1_15 = []
        df1_20 = []
        df1_24 = []
        df1_30 = []
        df1_40 = []
        df1_60 = []
        df1_120 = []
        df1_infinity = []
        #Create a series of lists to contain the columns of the table 
        index = 20 #The first t_stat is at index 20
        for t_stat in f_table_refined[20:]:
            #Each t_stat is from a row in a table. Therefore each location in each row corresponds to a alpha value and this pattern is consistent.
            #Exploit consistent location by using reminders from dividing the index by the length of the row
            if index % 20 == 0:
                df1_1.append(t_stat)
            elif index % 20 == 1:
                df1_2.append(t_stat)
            elif index % 20 == 2:
                df1_3.append(t_stat)
            elif index % 20 == 3:
                df1_4.append(t_stat)
            elif index % 20 == 4:
                df1_5.append(t_stat)
            elif index % 20 == 5:
                df1_6.append(t_stat)
            elif index % 20 == 6:
                df1_7.append(t_stat)
            elif index % 20 == 7:
                df1_8.append(t_stat)
            elif index % 20 == 8:
                df1_9.append(t_stat)
            elif index % 20 == 9:
                df1_10.append(t_stat)
            elif index % 20 == 10:
                df1_12.append(t_stat)
            elif index % 20 == 11:
                df1_15.append(t_stat)
            elif index % 20 == 12:
                df1_20.append(t_stat)
            elif index % 20 == 13:
                df1_24.append(t_stat)
            elif index % 20 == 14:
                df1_30.append(t_stat)
            elif index % 20 == 15:
                df1_40.append(t_stat)
            elif index % 20 == 16:
                df1_60.append(t_stat)
            elif index % 20 == 17:
                df1_120.append(t_stat)
            elif index % 20 == 18:
                df1_infinity.append(t_stat)
            index += 1
        #Turn the lists of df1 values into a dictionary 
        f_table_final = {f_table_refined[0] : df1_1, f_table_refined[1] : df1_2, f_table_refined[2] : df1_3, f_table_refined[3] : df1_4, f_table_refined[4] : df1_5, 
        f_table_refined[5] : df1_6, f_table_refined[6] : df1_7, f_table_refined[7] : df1_8, f_table_refined[8] : df1_9, f_table_refined[9] : df1_10, f_table_refined[10] : df1_12, 
        f_table_refined[11] : df1_15, f_table_refined[12] : df1_20, f_table_refined[13] : df1_24, f_table_refined[14] : df1_30, f_table_refined[15] : df1_40, 
        f_table_refined[16] : df1_60, f_table_refined[17] : df1_120, f_table_refined[18] : df1_infinity}
        return f_table_final

def f_stat_from_table(table,df1,df2):
    """Determines the correct f-stat for the analysis

    Arguments:
        table {[dictionary]} -- f-table where each key is a df1
        df1 {[integer]} -- degrees of freedom 1
        df2 {[type]} -- degrees of freedom 2

    Returns:
        f_stat_table {[integer]} -- f-stat from the f-table needed for the analysis
    """
    #Iterate through the dictionary and determine the appropriate df1 list to use
    index = -1
    for df in table:
        index += 1
        if index == (len(table) - 1):
            df_column = table[df] 
            break
        if int(df) == df1:
            df_column = table[df]
            break
        elif int(df) > df1:
            df_column = table[df]
            break
    #Determine the index to use on the df1 list
    if df2 > 120:
        table_index = 33
    elif df2 > 60:
        table_index = 32
    elif df2 > 40:
        table_index = 31
    elif df2 > 30:
        table_index = 30
    else:
        table_index = df2 - 1
    f_stat_table = float(df_column[table_index]) #Pull the correct f_stat for the analysis from the list
    return f_stat_table

from bs4 import BeautifulSoup
import re
import requests
from Display import choice_validation