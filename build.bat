pyinstaller -y -c armcom.py
copy /y .\*.dll .\dist\armcom
copy /y .\*.lib .\dist\armcom
copy /y .\*.png .\dist\armcom
copy /y .\steam_appid.txt .\dist\armcom
mkdir .\dist\armcom\data
copy /y .\data\*.* .\dist\armcom\data
mkdir .\dist\armcom\sounds
copy /y .\sounds\*.* .\dist\armcom\sounds
mkdir .\dist\armcom\src
copy /y .\*.py .\dist\armcom\src
copy /y .\gpl.txt .\dist\armcom\src
copy /y .\icon.ico .\dist\armcom\src
