import pandas as pd
import glob
import os

path = r'C:\Users\bmisaghi\Desktop\CapitalBikeShare'
all_files = glob.glob(os.path.join(path,'*.csv'))

df_list = []
date_formats = ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M']
for file in all_files:
    df = pd.read_csv(file)
    
    #lowercase all the column names
    df.columns = [nam.lower() for nam in df.columns]
    df.rename(columns = {'total Duration' : 'duration',
                         'total duration (ms)' : 'duration',
                        'duration in milliseconds' : 'duration',
                        'duration (ms)' : 'Duration',
                        'bike#' : 'Bike number',
                        'bike #' : 'bike number',
                        'type': 'Subscription Type',
                        'bike key' : 'subscription type',
                        'subscriber type' : 'subscription type',
                        'member type' : 'subscription type',
                        'account type' : 'subscription type',
                        'start time' : 'start_date',
                        'start date' : 'start_date',
                        'start station' : 'start_station'
                        } 
            ,inplace = True)
    df = df[['start_date', 'start_station']]
    #format the dataframe to normalize
    df['start_station'] = df['start_station'].str.replace(r"\(.*\)","")
    df['start_station'] = df['start_station'].str.strip()
    df = df.apply(lambda x: x.astype(str).str.lower())
    df['start_date'] = pd.to_datetime(df['start_date'], infer_datetime_format = True)
    #put the dataframe in a list
    df_list.append(df)
	
#combine the list of dataframes
df = pd.concat(df_list)

#get earliest record of each station
df_first = df.sort('start_date').groupby('start_station', as_index = False).first()