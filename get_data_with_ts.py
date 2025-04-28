# https://cricclubs.com/cricketorjp/viewScorecard.do?matchId=5299 (get this as input param)

# open cricclubs app, add the teams, toss, create match. hopefully this will create match id.
# get match id from browser
# start video camera recording. run this script at the same time as recording start time.
# this script will do get request on match url every 30 sec.
# in the response, for the latest balls, if there is 4/6/W, then save the ball num, desc, event, timestamp in a file.
# make sure this script runs again if it crashes.
# make sure it works on latest balls only, if it starts after crashing. (maybe in future) 
# add timestamp like this - can be copied to davinci resolve. 01000200

# improvements todo - 
# add some calculation in csv to get approx time stamps, or
# run this in real time to get time stamps - try to run python script in android
# find quick way to go to a time stamp and cut video in davinci resolve
# do calculation for 50/100 runs in the python script and save that ball
# quick way to add text in davinci resovle
# keep first and last ball of both innings?
# case - nb 6, nb 6, w etc. multiple events on the same ball.
# case - multiple wides
# case - penalty runs - https://cricclubs.com/cricketorjp/ballbyball.do?matchId=5286&clubId=21278
# case - no ball six. will it filter?
# case - 4bye - https://cricclubs.com/cricketorjp/ballbyball.do?matchId=5285&clubId=21278
# if latest ball > curr ball by more than 0.1, raise error? work on missed balls?
# another way - do curr ball + 1, keep polling until you find that ball, work on it, then again + 1 and keep polling. might crash in case of 7 ball over etc


import argparse
import requests
from bs4 import BeautifulSoup
import time
import sys
from datetime import datetime


tm_format = "%Y%m%d_%H%M%S"
start_timestamp = datetime.now().strftime(tm_format)

FILEPATH = f"outputfile_{start_timestamp}.txt"

description = """

This script takes a cricclubs match ID and outputs on which balls 4/6/Wicket happened along with TIMESTAMPs.
After teams added in cricclubs and toss done - Open your match's scorecard in browser and get the match id from the URL.

Example URL - https://cricclubs.com/cricketorjp/ballbyball.do?matchId=5299&clubId=21278
Therefore match id = 5299

Then start video camera recording, and run command as - python <filename.py> 5299

"""

def get_tables_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        save_to_file(f"error in get request {response.status_code} {response.text}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find_all('table', class_='table')

def save_to_file(some_text):
    print(some_text)
    with open(FILEPATH, 'a') as f:
        f.write(some_text + "\n")

def get_latest_ball(table, reversed_rows=False):
    rows = table.find_all('tr')
    return_value_ball = return_value_event = return_value_description = ""
    if reversed_rows:
        rows = reversed(rows)
    for row in rows:
        cols = row.find_all(['td', 'th'])
        cols_text = [col.text.strip() for col in cols]
        if len(cols_text) > 2 and cols_text[0]:
            return_value_ball = cols_text[0]
            return_value_event = return_value_description = ""
            if "NO BALL" in cols_text[2] or "WIDE" in cols_text[2]:
                return_value_event = "Extra"
            if "FOUR" in cols_text[2]:
                return_value_event = "Four"
                return_value_description = cols_text[2].split(",")[0]
            if "SIX" in cols_text[2]:
                return_value_event = "Six"
                return_value_description = cols_text[2].split(",")[0]
            if "OUT" in cols_text[2]:
                return_value_event = "Out"
                return_value_description = cols_text[2].split("!")[0][:-3].split(",")[0]
            break
    return return_value_ball, return_value_event, return_value_description

def is_same_ball(curr_ball, curr_ball_event, latest_ball, latest_ball_event):
    latest_ball_int = int(latest_ball.split(".")[0])*6 + int(latest_ball.split(".")[1])
    curr_ball_int = int(curr_ball.split(".")[0])*6 + int(curr_ball.split(".")[1])
    if latest_ball_int > curr_ball_int:
        return False
    elif latest_ball_int == curr_ball_int:
        if curr_ball_event != latest_ball_event:
            return False
    else:
        save_to_file(f"latest ball {latest_ball} is less than current ball {curr_ball}")
    return True

def get_timestamp(start_timestamp, tm_format):
    dt1 = datetime.strptime(start_timestamp, tm_format)
    new_tm = datetime.now().strftime(tm_format)
    dt2 = datetime.strptime(new_tm, tm_format)
    delta = dt2 - dt1
    total_seconds = int(delta.total_seconds()) + 3600 - 30

    # Break down into hours, minutes, seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format the output
    return f"{hours:02}{minutes:02}{seconds:02}00"

def get_curr_table(tables, second_innings_started, curr_ball, curr_ball_event):
    if len(tables) == 2:
        # match is finished..
        print("match finished")
        # save last ball if not done
        latest_ball, latest_ball_event, latest_ball_description = get_latest_ball(tables[1], reversed_rows=True)
        if latest_ball:
            if not second_innings_started:
                save_to_file("Inning 2")
                save_to_file("Ball Number, Description, Event, Timestamp")
            print("2nd inn")
            save_to_file(f"{latest_ball}, {latest_ball_description}, {latest_ball_event}, {get_timestamp(start_timestamp, tm_format)}")
        else:
            latest_ball, latest_ball_event, latest_ball_description = get_latest_ball(tables[0], reversed_rows=True)
            if latest_ball:
                save_to_file(f"{latest_ball}, {latest_ball_description}, {latest_ball_event}, {get_timestamp(start_timestamp, tm_format)}")
        return None, None, None, None
        # latest_ball, latest_ball_event, latest_ball_description = get_latest_ball(tables[1])
        # if latest_ball:
        #     if not second_innings_started:
        #         save_to_file("Inning 2")
        #         save_to_file("Ball Number, Description, Event, Timestamp")
        #         curr_ball = "0.0"
        #         curr_ball_event = ""
        #     return tables[1], True, curr_ball, curr_ball_event
        # else:
        #     return tables[0], False, curr_ball, curr_ball_event
    elif len(tables) == 4:
        # match is going on
        latest_ball, latest_ball_event, latest_ball_description = get_latest_ball(tables[3])
        print("mt going on")
        if latest_ball:
            if not second_innings_started:
                save_to_file("Inning 2")
                save_to_file("Ball Number, Description, Event, Timestamp")
                curr_ball = "0.0"
                curr_ball_event = ""
            print("2nd inn")
            return tables[3], True, curr_ball, curr_ball_event
        else:
            print("1st inn")
            return tables[2], False, curr_ball, curr_ball_event

def get_team_names(url):
    response = requests.get(url)
    if response.status_code != 200:
        save_to_file(f"error in get request {response.status_code} {response.text}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find('meta', attrs={"name": "keywords"}).get("content").split(",")[1:3]

# main flow
parser = argparse.ArgumentParser(description, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("match_id", help="Match ID")

args = parser.parse_args()
match_url = args.match_id
if "https" not in match_url:
    match_url = f"https://cricclubs.com/cricketorjp/ballbyball.do?matchId={match_url}"

save_to_file("Script start time: " + datetime.now().strftime("%Y/%m/%d %H:%M"))
save_to_file(" vs ".join(get_team_names(match_url)))
save_to_file("Inning 1")
save_to_file("Ball Number, Description, Event, Timestamp")

curr_ball = "0.0"
curr_ball_event = ""

second_innings_started = False

while(True):
    try: 
        # need to know how the html will look before 1st innings, during 1st innings, at completion of 1st innings, during 2nd innings
        # assuming - no tables in the beginning, then 1 table as 1st inning data comes in, then 2 tables when 2nd inning starts
        # if 1 table - get the table. get the last ball. compare with saved lastball var. 
        #   if greater, check if it is 4/6/W. if yes, write in file
        # lastball var = this ball
        # maybe use hash to compare?
        # if 2 tables, get the 2nd table. get the last ball (mostly should not be present at 30 sec polls)
        # lastball var = above. if above returned none, lastball = 0
        # then similar process to above
        # check lastball and wide/noball
        tables = get_tables_from_url(match_url)
        if tables:
            curr_table, second_innings_started, curr_ball, curr_ball_event = get_curr_table(tables, second_innings_started, curr_ball, curr_ball_event) # tables[-1]
            # if len(tables) == 2 and not second_innings_started:
            #     second_innings_started = True
            #     save_to_file("Inning 2")
            #     save_to_file("Ball Number, Description, Event, Timestamp")
            #     curr_ball = "0.0"
            #     curr_ball_event = ""
            if curr_table:
                latest_ball, latest_ball_event, latest_ball_description = get_latest_ball(curr_table)
                print("latest ball ", latest_ball, latest_ball_event, latest_ball_description)
                if latest_ball and not is_same_ball(curr_ball, curr_ball_event, latest_ball, latest_ball_event):
                    curr_ball = latest_ball
                    curr_ball_event = latest_ball_event
                    if latest_ball_event in ["Four", "Six", "Out"]:
                        save_to_file(f"{latest_ball}, {latest_ball_description}, {latest_ball_event}, {get_timestamp(start_timestamp, tm_format)}")
            else:
                break
        time.sleep(20)
    except Exception as err:
        save_to_file(f"error:{err}")
        time.sleep(20)

