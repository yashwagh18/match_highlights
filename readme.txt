Steps to create match highlights - Once you get used to it, a you can create highlights of a 40 overs match in less than an hour! 

This is only for Japan Cricket matches scored on CricClubs app.

--------

First, create a spreadsheet of 4/6/W balls using these steps.

Case 1 - You don't have timestamps of 4/6/W balls.

1. Go to CricClubs app, open your match's scorecard, tap share icon on top right -> share externally, copy the url, get match id from the url.
2. Run "python3 get_data_without_ts.py <match_id>" and get 4/6/W balls as output.
    - Copy the output to Google Sheets. 
    - Click on Data -> Split text into columns, for easier reading.


Case 2 - You have timestamps (from running get_data_with_ts.py script).

1. Before match start - When playing 11 are added in CricClubs and toss is done, follow case 1 -> step 1 to get the match id.
2. Run command "python3 get_data_with_ts.py <match_id>". At the same time, start video recording.
    - This command can be run in phone as well in Termux app. 
    - This creates an output file containing the 4/6/W balls and their timestamps.
3. After match end - stop video recording.
    - Open the output file, copy its contents to Google Sheets. 
    - Click on Data -> Split text into columns, for easier reading.

----

Once you have the spreadsheet ready, follow these steps. (Familiarity with Davinci Resolve software is needed here)

1. Open hd1080602.drp file. Give a unique project name.
2. Go to Edit tab. Replace broken media, if any.
    - For this, right click on the media in the top left panel -> Replace selected clip -> Select from file browser.
3. Change the intro text according to your match (AQCC vs MIB, JCL Division 2 etc).
4. Replace the score card image at the end with your match's score card.
    - To get this image, go to CricClubs app -> Open your match -> Summary -> Share icon on top right of the image.
5. Go to Cut tab. Add all video files from the camera in top left panel. Then add them in correct order in A1/V1 channel in the bottom panel.
6. Start from the end of the spreadsheet and go backwards. Find the last 4/6/W ball, cut that part, delete the part after that. Go to previous 4/6/W ball, repeat same.
    - If you don't have timestamps - find the 4/6/W ball using ball number and other details.
    - If you have timestamps - copy the timestamp, put it in the editor, scroll few seconds back. Easy!
7. Need to add few extra seconds in beginning and end to accommodate intro, outro.
8. Go to Quick export at top right -> YouTube and publish the video. Done!

--------

Useful shortcuts - "Ctrl \" to cut the video. "Backspace" to delete a clip.
