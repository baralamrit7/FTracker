# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 19:59:32 2022

@author: acer
"""


from data_structure import dataFrame
import os.path


def read_game_data(dataFolder, gameId,to_metric = False):
    ''' returns 3-tuple of dataFrame of events data , 
        tracking data of home team and tracking data of away team'''
    
    return (read_event_data(dataFolder,gameId),
            read_tracking_data(dataFolder,gameId, team='Home',to_metric = to_metric),
            read_tracking_data(dataFolder,gameId, team='Away',to_metric = to_metric))

    
def read_tracking_data(dataFolder, gameId , team, to_metric = False):
    '''returns dataFrame of tracking data of Home team or Away team'''
    
    #when to_metric is true
    metriced_filename_track = '/Sample_Game_{0}/to_metric/Sample_Game_{0}_RawTrackingData_{1}_Team.csv'.format(str(gameId),team)
    if to_metric == True and os.path.isfile(dataFolder  + metriced_filename_track):
        return dataFrame(dataFolder + metriced_filename_track)
    
    if team == 'Home' or team == 'Away':
        filename_track = '/Sample_Game_{0}/Sample_Game_{0}_RawTrackingData_{1}_Team.csv'.format(str(gameId),team)
    else:
        assert False, "team can be either 'Home' or 'Away'"
        
    tracking_data_dF =  dataFrame(dataFolder + filename_track)
    jerseys = get_player_jersey_from_tracking(tracking_data_dF)
    
    new_column_head = [tracking_data_dF[1].aslist[0], tracking_data_dF[1].aslist[1], tracking_data_dF[1].aslist[2]]
    for jersey in jerseys:
        new_column_head.append(str(jersey)+'_x')
        new_column_head.append(str(jersey)+'_y')
    new_column_head.append('Ball_x')
    new_column_head.append('Ball_y')
    
    tracking_data = dataFrame(tracking_data_dF,skiprows = 2)
    tracking_data.change_columnName(name = new_column_head)
    
    #When to_metric if tre
    if to_metric == True:
        _to_metric(tracking_data,field_x=105,field_y=68)
        dataFrame.save_as_csv(tracking_data,filename = dataFolder + metriced_filename_track)
        
    return tracking_data
    

def read_event_data(dataFolder , gameId):
    '''returns dataFrame of events data'''
    
    filename_events = '/Sample_Game_{0}/Sample_Game_{0}_RawEventsData.csv'.format(str(gameId))
    events_data =  dataFrame(dataFolder + filename_events)
    return events_data


def get_player_jersey_from_tracking(tracking_data_dF):
    '''returns a list of jersey numbers of players involved in the given team'''
    
    jerseys = tracking_data_dF[0].aslist
    jerseys = [int(item) for item in jerseys if item != '']
    return jerseys
    
    
def get_goal_keeper_from_tracking(tracking_data_dF):
    '''returns the jersey number of goal keeper'''
    
    
    
    
    
    
def  _to_metric(tracking_data,field_x=105,field_y=68):
    '''Changes the coordinate system used in the
    metrica sports data to usual coordinate system
    
    The defalt field_x and field_y represents 105m and 68m,
    the real length of the football pitch'''
    
    #   Y                                                  Y
    #   |                                                  | 
    #   |                                                  |
    #   |(0,0)                        (1,0)                |(-0.5,0.5)                    (0.5,0.5)
    #   ,--------------,--------------,                    ,--------------,--------------,
    #   |              |              |                    |              |              |
    #   |--,           |           ,--|                    |--,           |           ,--|
    #   |  |          <|>(0.5,0.5) |  |         ------>    |  |          <|>(0,0)     |  |
    #   |--'           |           '--|                    |--'           |           '--| 
    #   |              |              |                    |              |              |  
    #   '--------------'--------------'  ------X           '--------------'--------------'------X
    #   (0,1)                         (1,1)                (-0.5,-0.5)                         (0.5,-0.5)
    #
    #    Metrica sports coordinate                                To our metric system
    #    --------------------------                               ----------------------               
    
    
    
    
    columns = tracking_data.columns
    for col in columns:
        if col.endswith('_x'):
            for i in range(tracking_data.shape[0]):
                if tracking_data[i][col]=='NaN':
                    continue
                tracking_data[i][col]=float(tracking_data[i][col])-0.5
                tracking_data[i][col]*=field_x
                tracking_data[i][col]=round(tracking_data[i][col],5)
                
        elif col.endswith('_y'):
            for i in range(tracking_data.shape[0]):
                if tracking_data[i][col]=='NaN':
                    continue
                tracking_data[i][col]=float(tracking_data[i][col])-0.5
                tracking_data[i][col]*=-field_y
                tracking_data[i][col]=round(tracking_data[i][col],5)
                
        else:
            continue
    
    
    
    
    
    
