import requests
import json
import pandas as pd
import psycopg2

def getActivityData(wid, start_dt, end_dt):
    Data_params ={
        "wid" : int(wid),
        "start" : start_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "end" : end_dt.strftime("%Y-%m-%d %H:%M:%S")
    }
    # now.strftime("%Y-%m-%d, %H:%M:%S")
    print(Data_params)
    column_list = ["dt", "date", "time", "bitdepth", "md", "blockpos", "rop", "hklda", "woba", "torqa", "rpm", "stppress", "mudflowin",]
    # return None
    WellData = (
        (
            requests.get("https://pdumitradome.id/dome_api/rtdc/get_data", data=json.dumps(Data_params))
        ).text
    )

    Data_DF = pd.json_normalize(json.loads(WellData), record_path='result')
    # print(Data_DF.head(5))
    return Data_DF[column_list]



def get_session_id():
    # Hack to get the session object from Streamlit.

    ctx = ReportThread.get_report_ctx()

    this_session = None
    
    current_server = Server.get_current()
    if hasattr(current_server, '_session_infos'):
        # Streamlit < 0.56        
        session_infos = Server.get_current()._session_infos.values()
    else:
        session_infos = Server.get_current()._session_info_by_id.values()

    for session_info in session_infos:
        s = session_info.session
        if (
            # Streamlit < 0.54.0
            (hasattr(s, '_main_dg') and s._main_dg == ctx.main_dg)
            or
            # Streamlit >= 0.54.0
            (not hasattr(s, '_main_dg') and s.enqueue == ctx.enqueue)
        ):
            this_session = s

    if this_session is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object"
            'Are you doing something fancy with threads?')

    return id(this_session)

def GetInputActivity_DB(Conn, Well, Comp):
    cursor = Conn.cursor()

    select_query = "select * from activitylog_db"
    select_query += " where (well = '%s' and comp = '%s')" % (Well, Comp)
    # select_query += "where  = %s" %Well
    Table_Column = ['input_id',
                        'dt',
                        'date',
                        'time',
                        'comp',
                        'well',
                        'activity',
                        'in_slip_treshold',
                        'remarks',
                        'pic',
                        'section'
                        ]
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    
    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()
    Conn.close()
    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=Table_Column)
    return df
def GetSummaryActivity_DB(Conn, Well, Comp):
    cursor = Conn.cursor()

    select_query = "select * from summary_activity_db"
    select_query += " where (well = '%s' and comp = '%s')" % (Well, Comp)
    # select_query += "where  = %s" %Well
    listcolumn = ['comp',
        'well',
        'time_start',
        'time_end',
        'duration_minutes',
        'hole_depth',
        'bit_depth',
        'meterage_drilling',
        'rotate_drilling_time',
        'slide_drilling_time',
        'reaming_time',
        'connection_time',
        'on_bottom_hours',
        'stand_duration',
        'label_subactivity',
        'label_activity',
        'stand_meterage_drilling',
        'stand_durationx',
        'stand_on_bottom',
        'stand_group',
        'pic',
        'section',
        'remarks']
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    
    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()
    Conn.close()
    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=Table_Column)
    return df

# @st.cache
def OpenConnection():
    param_dic = {
    "host"      : "localhost",
    "database"  : "PDU_AUTOMAPPING",
    "user"      : "postgres",
    "password"  : "Saber2496"
    }
    conn = None
    # import json


    
    # print(user_encode_data)
    # try:
        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**param_dic)
    # except (Exception, psycopg2.DatabaseError) as error:
        # print(error)
        # sys.exit(1) 
    return conn

def DeleteInputActivity_DB(Conn, Well, Comp, InputID):
    SQL_Queries = "delete from activitylog_db"
    SQL_Queries += " where ((well = '%s' and comp = '%s') and input_id = %s)" % (Well, Comp, InputID)

    
    cursor = Conn.cursor()
    try:
        cursor.execute(SQL_Queries)
        Conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        Conn.rollback()
        cursor.close()
        return 1
    cursor.close()
    Conn.close() 

    # return None

def InsertInputActivity_DB(Conn, InputDict):
    
    SQL_Queries = """
    INSERT into activitylog_db(input_id, dt, date, time, comp, well, activity, in_slip_treshold, remarks, pic, section) values(%s,'%s','%s','%s','%s','%s','%s',%s,'%s','%s','%s');
    """ % tuple(InputDict.values())
    
    cursor = Conn.cursor()
    try:
        cursor.execute(SQL_Queries)
        Conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        Conn.rollback()
        cursor.close()
        return 1
    cursor.close()
    Conn.close() 
    # return None

def InsertSummaryActivity_DB(Conn, SummaryActivity_DF, WellName, CompName):
    SummaryActivity_DF = Activity.SummaryTranslator(SummaryActivity_DF, WellName, CompName, '-', '-', '-')
    for i in SummaryActivity_DF.index:
        SQL_Queries = """INSERT into summary_activity_db(comp, well, time_start, time_end, duration_minutes, hole_depth, bit_depth, meterage_drilling, rotate_drilling_time, slide_drilling_time, reaming_time, connection_time, on_bottom_hours, stand_duration, label_subactivity, label_activity, stand_meterage_drilling, stand_durationx, stand_on_bottom, stand_group, pic, section, remarks) values('%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', '%s', '%s', %s, %s, '%s', '%s', '%s', '%s'"""
        SQL_Queries += ")" 

        # print()
        cursor = Conn.cursor()
        try:
            cursor.execute(SQL_Queries % tuple(SummaryActivity_DF.iloc[i,:].to_list()))
            Conn.commit()
        except(Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            Conn.rollback()
            cursor.close()
            return 1
        cursor.close()
    Conn.close() 
