#Attempt to import important packages 
try: #Confirm that the user has installed pandas
    import pandas as pd
except: #Occurs if the user has not installed pandas
    print('\nERROR! You must use pip to install pandas in your command prompt to use this program. \nTo do this, open your command prompt. Type in \'pip install pandas\' and wait for the installation to be completed.')
try: #Confirm that the user has installed os
    import os
except: #Occurs if the user has not installed os
    print('\nERROR! You must use pip to install os in your command prompt to use this program. \nTo do this, open your command prompt. Type in \'pip install os\' and wait for the installation to be completed.')
try: 
    import requests #Confirm that the user has installed requests 
except: #Occurs if the user has not installed requests
    print('\nERROR! You must use pip to install requests in your command prompt to use this program. \nTo do this, open your command prompt. Type in \'pip install requests\' and wait for the installation to be completed.')
try:
    from bs4 import BeautifulSoup #Confirm that the user has installed bs4
except: #Occurs if the user has not installed bs4
    print('\nERROR! You must use pip to install bs4 in your command prompt to use this program (You need BeautifulSoup). \nTo do this, open your command prompt. Type in \'pip install bs4\' and wait for the installation to be completed.')
import math
import re

#Import functions
from Display import choice_validation
from Display import display_basics
from Display import print_disclaimer
from T_Table import t_stat_from_table
from T_Table import t_stat_lc
from T_Table import t_table_creation
from F_Table import F_Table
from F_Table import f_stat_from_table
from F_Table import f_table_creation
from Data_Extraction import get_directory
from Data_Extraction import Separator
from Data_Extraction import manipulate_data

def stat():
    """Main function to perform statistics on the users' data:
    Averages, Standard Deviation
    Ttest
    ANNOVA, Linear Contrast
    """
    users_pick = '''\nWelcome to Stat Tools. What would you like to do today?
    \n1) Basic statistics: Averages and Standard Deviations
    \n2) ttest: Compare the means of two groups to determine if they are equal or if there is a significant difference 
    \n3) ANOVA: Compare the means of multiple groups to determine if all groups are equal or at least one is significantly than another
    \n4) Quit: End the program'''
    choice = choice_validation(users_pick)
    if choice == 4:
        return
    users_input = '''Now, I need to get you data. How would you like me to attain it?
    \n1) Manual entry
    \n2) Guide me to the data by entering the directory and full name \nNOTE: This only works with .cvs files
    \n3) This program is inside a folder with the data \nNOTE: This only works with .csv files and the data must be the ONLY .csv file in the directory'''
    choice_input = choice_validation(users_input)
    if choice_input == 1:
        while True:
            all_treatment_groups = []
            #Get the names of the treatment groups
            treatment_groups = [treatment_group for treatment_group in input('Enter the names of your treatment groups separated by a comma (Do not include a comma in the name of the treatment group): ').split(',')]
            #Make sure isers' choice and number of treatment groups align
            if len(treatment_groups) != 2 and choice == 2:
                print('A ttest is between only two treatment groups. Please try again.')
                continue
            elif len(treatment_groups) < 3 and choice == 3:
                print('ANOVA is used for more than 2 treatment groups. Please try again.')
                continue
            #Get the data points per treatment group
            for treatment in treatment_groups:
                data_entry = [int(data_point) for data_point in input('Enter your data points for \'%s\' separated by a comma: ' % treatment).split(',')]
                all_treatment_groups.append(data_entry)
            break
    elif choice_input == 2:
        print_disclaimer()
        data = get_directory()
        all_treatment_groups,treatment_groups = manipulate_data(data)
    else:
        print_disclaimer()
        directory = os.getcwd()
        for file in os.listdir(directory + '\\'):
            if file.endswith('.csv'):
                data = pd.read_csv((directory + '\\' + file),engine='python')
                all_treatment_groups,treatment_groups = manipulate_data(data)
                break
    #Start Calculating Averages
    averages =[]
    for treatment_group in all_treatment_groups[:]:
        sum_data = 0
        n = 0
        for data_point in treatment_group[:]:
            sum_data += data_point
            n += 1
            if n == len(treatment_group):
                average = sum_data / n
                averages.append(average)
    #Start Calculating Standard Deviation
    stdevs = []
    index_average = -1
    for treatment_group in all_treatment_groups[:]:
        sum_square_difference = 0
        n = -1 #n minus 1 for standard deviation of sample
        index_average += 1
        for data_point in treatment_group[:]:
            difference = data_point - averages[index_average]
            sum_square_difference += difference**2
            n += 1
            if n == (len(treatment_group) - 1):
                stdev = math.sqrt(sum_square_difference / n)
                stdevs.append(stdev)
    if choice == 1:
        display_basics(treatment_groups,averages,stdevs)
    elif choice == 2:
    #Start Calculating ttest
    #Start Calculating Sp
        sp = math.sqrt((((len(all_treatment_groups[0])-1)*((stdevs[0])**2))+((len(all_treatment_groups[1])-1)*((stdevs[1])**2)))/(len(all_treatment_groups[0])+len(all_treatment_groups[1])-2))
    #Start Calculating t value
        t_value = (averages[0] - averages[1])/math.sqrt(((sp**2)/len(all_treatment_groups[0]))+((sp**2)/len(all_treatment_groups[1])))
        t_table = t_table_creation()
        df = len(all_treatment_groups[0]) + len(all_treatment_groups[1]) - 2 #Degrees of freedom
        t_stat_table = t_stat_from_table(df,t_table)
        if abs(t_value) > t_stat_table:
            print('The treatment groups are significantly different. The absolute t_value is {} compared to a t_value of {} from the t-table\n'.format(abs(t_value),t_stat_table))
        else:
            print('The treatment groups are not significantly different. The absolute t_value is {} compared to a t_value of {} from the t-table\n'.format(abs(t_value),t_stat_table))
        users_pick_2 = 'Would you also like to see the averages and standard deviations? \n1) Yes \n2) No'
        #Option to see averages and standard deviations
        second_choice = choice_validation(users_pick_2)
        if second_choice == 1:
            display_basics(treatment_groups,averages,stdevs)
    elif choice == 3:
    #Start calculating ANOVA
        dft = len(all_treatment_groups) - 1
    #SSB
        ssb_prt1 = 0
        for treatment_group in all_treatment_groups[:]:
            sum_data = 0
            n = 0
            for data_point in treatment_group[:]:
                sum_data += data_point
                n += 1
                if n == len(treatment_group):
                    sum_data_squared = sum_data**2
                    sum_data_sqaured_divided_n = sum_data_squared / n
                    ssb_prt1 += sum_data_sqaured_divided_n
        sum_all = 0
        n_total = 0
        for treatment_group in all_treatment_groups[:]:
            for data_point in treatment_group[:]:
                sum_all += data_point
                n_total += 1
        sum_all_sqaured = sum_all**2
        dfnt = n_total - 1
        dfnt_t = n_total - len(all_treatment_groups)
        ssb_prt2 = sum_all_sqaured / n_total
        ssb = ssb_prt1 - ssb_prt2
    #TSS
        sum_squares = 0
        for treatment_group in all_treatment_groups[:]:
            for data_point in treatment_group:
                sum_squares += data_point**2
        tss = sum_squares - ssb_prt2
        ssw = tss - ssb
    #sb^2 and sw^2 (Mean Square)
        sb2 = ssb / dft
        sw2 = ssw / dfnt_t
    #f-value
        f = sb2 / sw2
        f_table,f_alpha_value = f_table_creation()
        f_stat_table = f_stat_from_table(f_table,dft,dfnt_t)
        if abs(f) > f_stat_table:
            print('The treatment groups are significantly different with absolute f-value: {} compared to a f-value of {} from the f-table'.format(abs(f),f_stat_table))
        else:
            print('The treatment groups are not significantly different with absolute f-value: {} compared to a f-value of {} from the f-table'.format(abs(f),f_stat_table))
    #Linear Contrast
        while True:
            users_pick_3 = 'Do you need a linear contrast performed? \n1) Yes 2) No'
            third_choice = choice_validation(users_pick_3)
            if third_choice == 2:
                break
            else:
                print('\nRemember, your a-values must sum to 0.\n')
                a_values = []
                index = -1
                for treatment_group in treatment_groups:
                    index += 1
                    while True:
                        try:
                            a_value = float(input('Enter your a-value for treatment group \'%s\': ' % treatment_group))
                            break
                        except:
                            print('ERROR! You must enter a numerical value')
                    a_values.append(a_value)
                    if index == (len(treatment_groups) - 1):
                        sum_a = 0
                        for a_value in a_values:
                            sum_a += a_value
                        if sum_a != 0:
                            print('Your a-values did not sum to 0. Please try again.')
                            continue
                l_hat = 0
                index = 0
                for a_value in a_values[:]:
                    l_hat += a_value * averages[index]
                    index += 1
                index = 0
                a_n = 0
                for treatment_group in all_treatment_groups[:]:
                    a_n += (a_values[index]**2) / len(treatment_group)
                    index += 1
                se = math.sqrt(a_n * sw2)
                t_stat = l_hat / se
                t_table = t_table_creation()
                t_stat_table = t_stat_lc(dfnt_t,t_table,f_alpha_value)
                if abs(t_stat) > t_stat_table:
                    print('The linear contrast is significantly different with absolute t-value: {} compared to a t_value of {} from the t-table\n'.format(abs(t_stat),t_stat_table))
                else:
                    print('The linear contrast is not significantly different with absolute t-values: {} compared to a t_value of {} from the t-table\n'.format(abs(t_stat),t_stat_table))
        #Option to see averages and standard deviations
        users_pick_2 = 'Would you also like to see the averages and standard deviations? \n1) Yes \n2) No'
        second_choice = choice_validation(users_pick_2)
        if second_choice == 1:
            display_basics(treatment_groups,averages,stdevs)
    return

stat()