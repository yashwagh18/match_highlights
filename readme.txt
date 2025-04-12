youtube highlights making steps -

case 1 - don't have timestamps

1. use get_data_without_ts.py and get 4/6/W balls. add it in google sheets. split text into columns.
2. open video files in davinci resolve. change project resolution and frame rate. add all files to timeline in order. 
3. go to edit page, select all, right click, create compound file. back to cut page.
4. cut the video acc to data in spreadsheet. all fields are useful to quickly find next event ball.
5. useful shortcuts - "ctrl \" to cut the video. "backspace" to delete a clip. you can set timecode at bottom right of the video display.
6. add subscribe video at the end.
7. go to edit tab, add title. "fusion title -> clean and simple" is good.
8. export video to a file. upload to youtube from chrome browser.

case 2 - have timestamps (from python script ran during the match)

use get_data_with_ts.py
need to test this once. need to test how to run in phone without crashing.

1. before match - after teams added in cricclubss and toss done, get the match id and start video recording and python script at the same time.
2. after match - stop python script. copy output file content and send to laptop via gmail/google sheets.
3. open video files in davinci resolve. change project resolution and frame rate. add all files to timeline in order. 
4. go to edit page, select all, right click, create compound file. back to cut page.
5. start from end of the timestamp list and go backwards.
6. in davinci resolve, go to each timestamp, find the event, cut the video, remove the clip after the event. do it for all timestamps from last to first.
7. add subscribe video at the end.
8. go to edit tab, add title. "fusion title -> clean and simple" is good.
9. export video to a file. upload to youtube from chrome browser.
