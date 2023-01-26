
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('ds/test1ds/survey_results_public_2021.csv')
schema = pd.read_csv('ds/test1ds/survey_results_schema_2021.csv')

'''
view data
'''

print( df.head() ) 
print(df.tail(5))
print (df.shape)
print(list (df.columns), "\n \n amount of columns: ", len( list(df.columns) ), '\n' )
df1 = df.iloc[:,-5:]  #df.iloc[row_start:row_end , col_start, col_end] --> to see last columns
print('\n last 5 coumns with aswers : \n',df1.head())

df = df.drop(['ResponseId','ConvertedCompYearly'], axis =1)

'''
questions to be answerd:
1) Is file with results of survey uderstandable ? 
2) to which questions we have less answers and to which we have more ?
3) who mostly/always avoid answering ?
4) who mostly/always answered  ?

'''


'''
1) Is file with results of survey uderstandable ? 
'''
def get_description(value_name, template):
    '''
    INPUT - template - pandas dataframe with the schema of the developers survey
            value_name - string - value for which you would like to know about description
    OUTPUT - 
            desc - string - the description of the value_name
    '''
    
    if value_name in template['qname'].values.tolist():
        desc = list(template[template['qname'] == value_name]['question'])[0]
    else :
        desc = np.nan #'NOT IN QUESTION LIST'  

    return desc


#check if all colums in aswer file are possible to be described:
column_names = pd.DataFrame( df.columns.values.tolist(), columns = ['col_name'] ) # data frame of column names with description
# print('\n answer column names: \n', column_names, column_names.shape)

descrips = pd.DataFrame(get_description(col,schema) for col in column_names['col_name']) #descriptions of column names 
# print("\n \n answer column desription : \n \n", descrips)

# horizontal_stack = pd.concat([survey_sub, survey_sub_last10], axis=1)
column_names_desc = pd.concat([column_names,descrips],axis=1)  # data frame of column names with description
columnNames = ['qname','question']
column_names_desc.columns=columnNames

# print('\n \ncolumn_names_desc  :\n',column_names_desc )

print('\n PERCENTAGE OF COLUMNS WITHOUT DESCRIPTION: ', column_names_desc['question'].isnull().mean())  # percentage of columns without description
print('\n list of column without description:: \n', column_names[column_names_desc.isna().any(axis=1)])

# to add column descritption if missing
column_names_desc.loc[column_names_desc['qname'] == 'LanguageHaveWorkedWith', 'question'] = 'Language you have worked with'
column_names_desc.loc[column_names_desc['qname'] == 'LanguageWantToWorkWith', 'question'] = 'Language you want to work with'
column_names_desc.loc[column_names_desc['qname'] == 'DatabaseHaveWorkedWith', 'question'] = 'Database you have worked with'
column_names_desc.loc[column_names_desc['qname'] == 'DatabaseWantToWorkWith', 'question'] = 'Database you want to work with'
column_names_desc.loc[column_names_desc['qname'] == 'PlatformHaveWorkedWith', 'question'] = 'Cloud platforms you have worked with'
column_names_desc.loc[column_names_desc['qname'] == 'PlatformWantToWorkWith', 'question'] = 'Cloud platforms you want to work with'
column_names_desc.loc[column_names_desc['qname'] == 'WebframeHaveWorkedWith', 'question'] = 'Web frameworks you have worked with'
column_names_desc.loc[column_names_desc['qname'] == 'WebframeWantToWorkWith', 'question'] = 'Web frameworks you want to work with'
column_names_desc.loc[column_names_desc['qname'] == 'MiscTechHaveWorkedWith', 'question'] = 'Frameworks and libraries you have done extensive development'
column_names_desc.loc[column_names_desc['qname'] == 'MiscTechWantToWorkWith', 'question'] = 'Frameworks and libraries you wnant to work with'
column_names_desc.loc[column_names_desc['qname'] == 'ToolsTechHaveWorkedWith', 'question'] = 'Tools you have done extensive development work'
column_names_desc.loc[column_names_desc['qname'] == 'ToolsTechWantToWorkWith', 'question'] = 'Tools you wnant to work with'
column_names_desc.loc[column_names_desc['qname'] == 'NEWCollabToolsHaveWorkedWith', 'question'] = 'Development environments which did you use regularly over the past year'
column_names_desc.loc[column_names_desc['qname'] == 'NEWCollabToolsWantToWorkWith', 'question'] = 'Development environments which you want to use next year'
column_names_desc.loc[column_names_desc['qname'] == 'ConvertedCompYearly', 'question'] = 'Converted year'

# print(column_names_desc.head())


'''
2) to which questions we have less answers and to which we have more ?
'''
# The proportion of missing values in columns
NaN_perc = pd.DataFrame(df.isnull().mean().sort_values(ascending=False))
NaN_perc.reset_index(inplace=True)
columnNames1 = ['qname','value']
NaN_perc.columns=columnNames1

descrips1 = pd.DataFrame(get_description(col,column_names_desc) for col in NaN_perc['qname']) #descriptions of column names 

NaN_perc_desc = pd.concat([NaN_perc,descrips1],axis=1)  # data frame of column names with description
columnNames2 = ['qname','perc of NaNs','question']
NaN_perc_desc.columns = columnNames2
# print('\n percentage of mising answers in each column: \n', NaN_perc_desc)

print('\n MISSING VALUES IN COLUMNS: \n' ) 

print('\n COLUMNS WITH TOP MISSING VALUES: \n' ) 
print(NaN_perc_desc.head(10))

print('\n COLUMNS WITH LEAST MISSING VALUES: \n' ) 
print(NaN_perc_desc.tail(10))

plt.title('COLUMNS WITH TOP MISSING VALUES')
plt.xlabel('question')
plt.xticks(rotation=45, ha='right',fontsize = 9,wrap=True )
plt.ylabel('perc of NaN')
plt.plot(NaN_perc_desc['question'][:5],NaN_perc_desc['perc of NaNs'][:5],'ro')
current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.2f}'.format(x) for x in current_values])
plt.gca().set_yticklabels(['{:,.1%}'.format(x) for x in current_values])
plt.subplots_adjust(bottom=0.35)
plt.show()

plt.title('COLUMNS WITH LEAST MISSING VALUES')
plt.xlabel('question')
plt.xticks(rotation=45, ha='right',fontsize = 9,wrap=True )
plt.ylabel('perc of NaN')
plt.plot(NaN_perc_desc['question'][-5:],NaN_perc_desc['perc of NaNs'][-5:],'go')
current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.3f}'.format(x) for x in current_values])
plt.gca().set_yticklabels(['{:,.2%}'.format(x) for x in current_values])
plt.subplots_adjust(bottom=0.35)
plt.show()


'''
3) who mostly/always avoid answering ?
4) who mostly/always answered  ?
'''

#how many NaN and not_NaN in rows of aswer data frame:
nan_in_row = df.isnull().sum(axis=1)
not_nan_in_row = df.notna().sum(axis=1)

prof_nans = pd.concat([df['MainBranch'],nan_in_row,not_nan_in_row],axis=1) # data frame of proffesions and NaN/not_NaN in rows
columnNames3 = ['proffesion','NaNs_count','not_NaNs_count']
prof_nans.columns=columnNames3

prof_nans_df = pd.DataFrame( prof_nans.groupby('proffesion').sum()['NaNs_count'] ) # percentage of aswers missed gouped by proffesion:

for i in range (prof_nans.groupby('proffesion').sum()['NaNs_count'].shape[0]):  # calculate percetage for each row
    prof_nans_df.loc[prof_nans_df.index[i],'perc_of_NaN'] = (prof_nans.groupby('proffesion').sum()['NaNs_count'][i] / prof_nans.groupby('proffesion').sum()['not_NaNs_count'][i])

print('\n PERCENTAGE OF ANSWERS MISSED, GROUPED BY PROFFESION :\n',prof_nans_df.sort_values(by='perc_of_NaN', ascending=False))

prof_nans_df.reset_index(inplace=True)

plt.title('PERCENTAGE OF ANSWERS MISSED, GROUPED BY PROFFESION')
plt.xlabel('proffesion')
plt.xticks(rotation=45, ha='right',fontsize = 9,wrap=True ) 
plt.ylabel('perc of NaN')
plt.plot(prof_nans_df.sort_values(by='perc_of_NaN', ascending=False)['proffesion'],prof_nans_df.sort_values(by='perc_of_NaN', ascending=False)['perc_of_NaN'],'b^')
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.1%}'.format(x) for x in current_values])
plt.subplots_adjust(bottom=0.35)

plt.show()


'''
5) Does your opinion about survey influents amount of NaNs  ?
'''

surv_opinion = pd.concat([df['SurveyLength'],nan_in_row,not_nan_in_row],axis=1) # data frame of proffesions and opinions about survey
columnNames4 = ['SurveyLength','NaNs_count','not_NaNs_count']
surv_opinion.columns=columnNames4

surv_opinion_df = pd.DataFrame( surv_opinion.groupby('SurveyLength').sum()['NaNs_count'] ) # percentage of aswers missed grouped by opinions about survey

for i in range (surv_opinion.groupby('SurveyLength').sum()['NaNs_count'].shape[0]):  # calculate percetage for each row
    surv_opinion_df.loc[surv_opinion_df.index[i],'perc_of_NaN'] = (surv_opinion.groupby('SurveyLength').sum()['NaNs_count'][i] / surv_opinion.groupby('SurveyLength').sum()['not_NaNs_count'][i])

print('\n PERCENTAGE OF ANSWERS MISSED, GROUPED BY OPINION ABOUT SURVEY :\n', surv_opinion_df.sort_values(by='perc_of_NaN', ascending=False))

surv_opinion_df.reset_index(inplace=True)
print(surv_opinion_df)


plt.title('PERCENTAGE OF ANSWERS MISSED, GROUPED BY OPINION ABOUT SURVEY')
plt.xlabel('Survey Length')
plt.ylabel('perc of NaN')
plt.plot(surv_opinion_df.sort_values(by='perc_of_NaN', ascending=False)['SurveyLength'],surv_opinion_df.sort_values(by='perc_of_NaN', ascending=False)['perc_of_NaN'],'bs')
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.1%}'.format(x) for x in current_values])

plt.show()
