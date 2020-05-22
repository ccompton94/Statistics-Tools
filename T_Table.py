def t_table_creation():
    """Pulls a t_table from the web and constructs it into a dictionary

    Returns:
        t_table {dictionary} -- t-table where each key is an alpha value 
    """
    url = "http://www.socr.ucla.edu/Applets.dir/T-table.html" #t-table from the web
    r = requests.get(url) #Pull the html data
    soup = BeautifulSoup(r.content,'html.parser').prettify() #Parse the html data into a string
    #Remove html specific coding from the string
    pattern = r"<(.+)>\s" #Patter for html spefic coding
    new_soup = re.sub(pattern, "", soup) #Remove html specific coding
    new_soup = re.findall(r"[^/s]", new_soup) #Turn the string into a list with individual characters
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
    #Refine table to exclude values not related to the t_table
    table_refined = []
    index = 0
    for value in table:
        if '=' in value: #If there is an equal sign, only append the numeric components after the equal sign
            new_entry = ''
            skip = 0 #Skip values before the equal sign
            for character in value:
                if skip == 1:
                    new_entry += character #Combine the numeric components after the equal sign
                if character == '=': 
                    skip = 1 #Start adding now that equal sign has passed
            table_refined.append(new_entry) #append the new entry
        else:
            try: #If the value is not a number, don't add it e.g.) 't'
                new_entry = float(value) 
                table_refined.append(value)
            except:
                pass #pass values that are not numbers
        if value == '3.291': #There are two lines for infinity in this table.
            index += 1
        if index == 2: #After the second line of infinity, all t-table values have been added
            break #Stop the loop
    #Further refine the table to remove a dublicate infinity row
    table_refined_2 = table_refined[:7] #Remove the first line of infinity, only one is needed
    for t_stat in table_refined[14:(len(table_refined) - 7)]:
        table_refined_2.append(t_stat)
    table_refined_2.append('infinity') #Mark the begining of the infinity line
    for t_stat in table_refined[(len(table_refined) - 7):]:
        table_refined_2.append(t_stat)
    #Create lists for each alpha value's t_stat per df
    alpha_01 = []
    alpha_005 = []
    alpha_0025 = []
    alpha_001 = []
    alpha_0005 = []
    alpha_0001 = []
    alpha_00005 = []
    #Each t_stat is from a row in a table. Therefore each location in each row corresponds to a alpha value and this pattern is consistent
    #Exploit the consistent location by using remainders from dividing the index by the length of the row
    index = 8 #The first t_stat is at index 8
    for t_stat in table_refined_2[8:]:
        if index % 8 == 0:
            alpha_01.append(t_stat)
        elif index % 8 == 1:
            alpha_005.append(t_stat)
        elif index % 8 == 2:
            alpha_0025.append(t_stat)
        elif index % 8 == 3:
            alpha_001.append(t_stat)
        elif index % 8 == 4:
            alpha_0005.append(t_stat)
        elif index % 8 == 5:
            alpha_0001.append(t_stat)
        elif index % 8 == 6:
            alpha_00005.append(t_stat)
        index += 1
    #Turn the lists of alpha values into a dictionary
    t_table = {table_refined_2[0] : alpha_01, table_refined_2[1] : alpha_005, table_refined_2[2] : alpha_0025, 
    table_refined_2[3] : alpha_001, table_refined_2[4] : alpha_0005, table_refined_2[5] : alpha_0001, table_refined_2[6] : alpha_00005} 
    return t_table

def t_stat_from_table(df, t_table):
    """Determines the correct t_stat for the analysis

    Arguments:
        df {[integer]} -- degrees of freedom
        t_table {[dictionary]} -- t-table where each key is an alpha value 

    Returns:
        t_stat_table {[integer]} -- t-stat from the t-table needed for the analysis
    """
    #Let the user pick which alpha value they want to use
    users_alpha = "\nChoose the alpha value you wish to use with the t_test "
    numbered_choice = 0
    alpha_options = {}
    for key in t_table: #Compile the options into a string
        numbered_choice += 1
        users_alpha += ('\n%d) %s' % (numbered_choice, key))
        alpha_options[numbered_choice] = '%s' % key 
    alpha_list = t_table[alpha_options[choice_validation(users_alpha)]] #Corresponding list of t_stats per user's choice 
    #Determine the index of the t_stat needed from the list of t_stats based off the degrees of freedom
    if df > 120:
        table_index = 32
    elif df > 60:
        table_index = 31
    elif df > 30:
        table_index = 30
    else:
        table_index = df - 1
    t_stat_table = float(alpha_list[table_index]) #Pull the correct t_stat for the analysis from the list
    return t_stat_table

def t_stat_lc(df, t_table, alpha):
    """Determines the correct t_stat for the analysis

    Arguments:
        df {[integer]} -- degrees of freedom
        t_table {[dictionary]} -- t-table where each key is an alpha value 

    Returns:
        t_stat_table {[integer]} -- t-stat from the t-table needed for the analysis
    """
    #Divide the alpha by two for the linear contrast t-stat
    alpha = float(alpha) / 2
    if alpha == 0.0125:
        alpha = str(0.01)
    elif alpha == 0.0025:
        alpha = str(0.001)
    elif alpha < 0.0005:
        alpha = str(0.0005)
    else:
        alpha = str(alpha)
    alpha_list = t_table[alpha]
    #Determine the index of the t-stat needed from the list of t_stats based off the degrees of freedom
    if df > 120:
        table_index = 32
    elif df > 60:
        table_index = 31
    elif df > 30:
        table_index = 30
    else:
        table_index = df - 1
    t_stat_table = float(alpha_list[table_index]) #Pull the correct t_stat for the analysis from the list
    return t_stat_table

from bs4 import BeautifulSoup
import re
import requests
from Display import choice_validation