def get_directory():
    """Requests the user to copy and paste the directory where the data is saved and type the name of the file.
    
    Returns:
       data {dictionary} -- Data pulled from the user's file.
    """
    while True: #Create a loop to give the user multiple attempts to enter the directory correctly
        try: #If the user does not enter the direcotry or file name correctly, they will be asked to do it again
            #Split the directory by the forward slash so that an additional forward slash can be added. Python uses the forward slash as an escape, so two is needed here
            print('\n\nHelp me find your data.')
            directory = [a for a in input('\nFrom your file explorer, copy and paste the directory for the location of the data file: ').split('\\')]
            new_directory = ''
            for x in directory:
                new_directory += (x + '\\')
            filename = input('\nEnter the name of the file, e.g. Practice.csv: ')
            last_digits = filename[(len(filename) - 4):]
            if last_digits != '.csv': #Make sure the filename ends in the proper file type
                full_directory = new_directory + filename + '.csv'
            else:
                full_directory = new_directory + filename
        except: #Occurs if the directory or filename is incorrect
            print('\nERROR! Please check your directory and file name.')
            pass #Restart the loop if the user did not answer the question correctly
        try:
            data = pd.read_csv((full_directory),engine='python') #Confirm the directory and file name works
            break
        except:
            print('\nERROR! Data could not be retrieved. Make sure the file and filename match the data file you are trying to use.')
    return data

class Separator():
    def __init__(self,data,divisor,treatment,treatment_name):
        self.data = data
        self.index_divisor = divisor
        self.treatment = treatment 
        self.treatment_name = treatment_name
    #Define a function to separate the data into new treatment groups based off the given factor
    def separate(self):
        """Divides the treatment groups by the new factor

        Returns:
           new_data_list {[list]} -- List of treatment groups 
           new_treatment {[list]} -- Treatment group names 
        """
        segregation = []
        for treatment_group in self.data: #Iterate through treatment groups
            for data_point in treatment_group: #iterate through data points in the treatment groups
                index = -1
                for info in data_point: #Iterate through the information provided for each data point
                    index += 1
                    if index == self.index_divisor: #If the info is a factor, add it to the list 
                        segregation.append(info)
        segregation_set = [{dividee for dividee in segregation}] #Turn the list into an embedded unique set inside a list
        #Extract the set and turn it back into a list to create a list with only unique entries
        factor = [] 
        for set_in_list in segregation_set:
            for identifier in set_in_list:
                factor.append(identifier)
        #Track the treatment group names
        new_treatment = []
        for factor_level in factor:
            for old_treatment in self.treatment:
                new_treatment.append(old_treatment + ' & ' + factor_level + ' ' + self.treatment_name)
        #Separate the data list into the new treatment groups
        new_data_list = []
        for factor_level in factor:
            for treatment_group in self.data:
                new_treatment_group = []
                for data_point in treatment_group:
                    if data_point[self.index_divisor] == factor_level:
                        new_treatment_group.append(data_point)
                new_data_list.append(new_treatment_group)
        return new_data_list,new_treatment
    #Define a function to extract the data points from the embedded lists
    def final_iterations(self):
        """Creates the final lists of data and treatment groups by removing unneeded information

        Returns:
           data_point_list {[list]} -- List of data per treatment group 
           new_treatment_groups {[list]} -- Treatment group names
        """
        data_point_list = []
        for treatment_group in self.data:
            treatment = []
            for data_point in treatment_group:
                treatment.append(data_point[self.index_divisor])
            data_point_list.append(treatment)
        new_treatment_groups = []
        for treatment_group in self.treatment:
            if treatment_group[1] == '&':
                new_treatment = treatment_group[3:]
            else:
                new_treatment = treatment_group
            new_treatment_groups.append(new_treatment)
        return data_point_list,new_treatment_groups

def manipulate_data(data):
    """Separates data into separate treatment groups for analysis

    Arguments:
        data {[dictionary]} -- Data imported by user

    Returns:
        all_treatment_groups {[list]} -- Data imported by user
        treatment_groups {[list]} -- Data imported by user all_treatment_groups,treatment_groups
    """
    num_label_tracker = []
    all_treatment_groups = []
    for column in data:
        test_for_numbers = data[column]
        index = 0
        #Determine how the user has stored the data. 
        #Either the data is in separate columns per treatment or the data is in one column with other columns as identifiers
        for cell in test_for_numbers:
            index += 1
            try:
                cell = int(cell)
            except ValueError:
                num_label_tracker.append(1) #Data is in one column with identifiers in other columns
                break
            if index == (len(test_for_numbers) - 1):
                num_label_tracker.append(0) #This column is only data
    if 1 not in num_label_tracker: #Data is in separate columns with treatment groups as labels above the entries
        treatment_groups = []
        for column in data:
            all_treatment_groups.append(data[column])
            treatment_groups.append(column)
    else:
        index_data = num_label_tracker.index(0)
        index = -1
        for column in data:
            index += 1
            if index == index_data:
                pre_all_treatment_groups = data[column]
        all_treatment_groups_initial = [] #List to store the details of the data points as embedded individual lists 
        index = -1
        for entry in range(len(pre_all_treatment_groups)): #Entry acts as an index
            data_point = []
            for column in data:
                column_values = data[column]
                data_point.append(column_values[entry]) #Append the details for the indexed data point
            all_treatment_groups_initial.append(data_point) #Store the individual data point lists 
        all_treatment_groups.append(all_treatment_groups_initial) #Embed the initial list
        index = -1
        treatment_groups = [""]
        for column in data: #Iterate through the columns in data
            index += 1
            #if the column is not the data column, sperate it by the factors 
            if index == index_data:
                pass
            else:
                all_treatment_groups_transform = Separator(all_treatment_groups,index,treatment_groups,column) #Create a new object 
                all_treatment_groups,treatment_groups = all_treatment_groups_transform.separate() #Re-assign the lsit 
        final_data_points = Separator(all_treatment_groups, index_data, treatment_groups, 'Substitution')
        all_treatment_groups,treatment_groups = final_data_points.final_iterations()
    return all_treatment_groups,treatment_groups

import os