def choice_validation(x):
    """Turns a string into a user interface. Answers are restricted to the choices.
    
    Arguments:
        x {string} -- Content for user interface
    
    Returns:
       ans {integer} -- User's answer to available choices
    """
    #User interface
    print('\n')
    y = x.split('\n')
    xx = ''
    for z in y:
        xx += z + '\n\n'
    y = xx.split(' ')
    print(xx)
    z = []
    for t in y:
        if ')' in t:
            loc = t.index(')')
            loc -= 1
            z.append(int(t[loc]))
    #Answer restriction
    while True:
        try:
            ans = int(input('Enter the number associated with your decision: '))
            low = min(z)
            high = max(z)
            if ans < low or ans > high:
                print('Invalid answer! Try again.\n')
                print(xx)
                continue
            else:
                break
        except:
            print('You must choose a number. Try again.\n')
            print(xx)
            pass
    return ans

def display_basics(treatments,averages,standard_devs):
    """Prints a table of the treatment groups with their averages and standard deviations

    Arguments:
        treatments {[list]} -- Treatment groups
        averages {[list]} -- Averages per treatment group
        standard_devs {[list]} -- Standard deviations per treatment group
    """
    #Create a table with the data using panda
    table = {'Treatment Group':treatments,'Average':averages,'Standard Deviation':standard_devs}
    table = pd.DataFrame(table)
    print(table)
    return

def print_disclaimer():
    """Prints a disclaimer message to inform the user of the limitations of this program
    """
    print('''\n\nIt is important that your data is formatted correctly on your .csv file. 
    Please follow the following instructions:
    1) Don't leave blank spaces above or to the left of your data. Your data should be located in the top left corner of your spreadsheet
    2) You must choose one of two ways to group the data.
    \ta) One numbers column. The remaining columns are factors. eg)
    \t\tColumn 1 (Raw Data) = 5,6,7,8,9,6 
    \t\tColumn 2 (Flow) = L, M, H, L, M, H
    \t\tColumn 3 (Temperature) = 30C, 30C, 30C, 60C, 60C, 60C
    \tb) All number columns with treatment group names as their headers. eg)
    \t\tColumn 1 (L Flow, 30C Temperature) = 5
    \t\tColumn 2 (M Flow, 30C Temperature) = 6
    \t\tColumn 3 (H Flow, 30C Temperature) = 7
    \t\tColumn 4 (L Flow, 60C Temperature) = 8
    \t\tColumn 5 (M Flow, 60C Temperature) = 9 
    \t\tColumn 6 (H Flow, 60C Temperature) = 6
    Note: This does mean if you do 2a, you cannot have 2 numeric columns. If one numeric column is one of your factor(s), indicate this by writing out the number. 
    ''')
    return

import pandas as pd