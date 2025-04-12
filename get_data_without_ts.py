# get request on https://cricclubs.com/cricketorjp/viewScorecard.do?matchId=5299 (get this as input param)

# for loop on each table row -
#     check if this row contains strong field and strong field contains 4/6/W
#         if yes, append (ball number, event) to a list. event is 4/6/W
# in the end, write the list to a csv file.

# improvements todo - 
# add some calculation in csv to get approx time stamps, or
# run this in real time to get time stamps - try to run python script in android
# find quick way to go to a time stamp and cut video in davinci resolve
# do calculation for 50/100 runs in the python script and save that ball
# quick way to add text in davinci resovle
# keep first and last ball of both innings?

import argparse
import requests
from bs4 import BeautifulSoup

description = """

This script takes a cricclubs match ID and outputs on which balls 4/6/Wicket happened.
Open your match's scorecard in browser and get the match id from the URL.

Example URL - https://cricclubs.com/cricketorjp/ballbyball.do?matchId=5299&clubId=21278
Therefore match id = 5299

Then run command as - python <filename.py> 5299

"""

def get_ball_difference(curr_ball, prev_ball):
    # print(curr_ball, prev_ball)
    curr_ball_int = int(curr_ball.split(".")[0])*6 + int(curr_ball.split(".")[1])
    prev_ball_int = int(prev_ball.split(".")[0])*6 + int(prev_ball.split(".")[1])
    ball_diff_int = curr_ball_int - prev_ball_int
    return f"{str(int((ball_diff_int - ball_diff_int % 6)/6))}.{str(ball_diff_int % 6)}"

def get_time_difference(ball_diff):
    one_ball_time = 0.66
    ball_diff_int = int(ball_diff.split(".")[0])*6 + int(ball_diff.split(".")[1])
    time_diff = ball_diff_int * one_ball_time - 1.5
    if time_diff < 0:
        time_diff = 0
    return str(int(round(time_diff, 0)))


parser = argparse.ArgumentParser(description, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("match_id", help="Match ID")

args = parser.parse_args()
match_url = args.match_id
if "https" not in match_url:
    match_url = f"https://cricclubs.com/cricketorjp/ballbyball.do?matchId={match_url}"

response = requests.get(match_url)

# print(response.status_code)  # HTTP status code (e.g. 200)
# print(response.text[0:8])         # Response body as text
# print(response.json())       # If response is JSON

soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all('table', class_='table')

for i, tbl in enumerate(tables):
    print(f"Inning {i+1}")
    print("Ball Number, Description, Event, Over Difference, Time Difference")
    prev_event_ball = "0.0"
    rows = tbl.find_all('tr')
    for row in rows:
        cols = row.find_all(['td', 'th'])
        cols_text = [col.text.strip() for col in cols]
        if len(cols_text) > 2 and ("FOUR" in cols_text[2] or "SIX" in cols_text[2] or "OUT" in cols_text[2]) and cols_text[0]:
            # print(cols_text)
            ball_diff = get_ball_difference(cols_text[0], prev_event_ball)
            time_diff = get_time_difference(ball_diff)
            prev_event_ball = cols_text[0]
            if "FOUR" in cols_text[2]:
                print(f"{cols_text[0]}, {cols_text[2].split(",")[0]}, Four, {ball_diff}, {time_diff}")
            if "SIX" in cols_text[2]:
                print(f"{cols_text[0]}, {cols_text[2].split(",")[0]}, Six, {ball_diff}, {time_diff}")
            if "OUT" in cols_text[2]:
                print(f"{cols_text[0]}, {cols_text[2].split("!")[0][:-3].split(",")[0]}, Out, {ball_diff}, {time_diff}")

