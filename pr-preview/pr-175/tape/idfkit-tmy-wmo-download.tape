Set WindowBar Colorful
Set FontSize 18
Set Width 1100
Set Height 480
Set Padding 20
Output idfkit_tmy_wmo_download.gif

Type "idfkit tmy --wmo 725300 --variant 2009-2023 --first --download ./weather/"
Enter
Sleep 10s
Type "ls ./weather/files/725300/*/"
Enter
Sleep 3s
