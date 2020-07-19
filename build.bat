"C:\python27\python.exe" pyinstaller -y -c C:\armcom\armcom.py
copy /y .\*.dll .\dist\armcom
copy /y .\*.png .\dist\armcom
mkdir .\dist\armcom\data
copy /y .\data\*.* .\dist\armcom\data
mkdir .\dist\armcom\src
copy /y .\armcom.py .\dist\armcom\src
copy /y .\armcom_defs.py .\dist\armcom\src
copy /y .\armcom_vehicle_defs.py .\dist\armcom\src
copy /y .\xp_loader.py .\dist\armcom\src
copy /y .\gpl.txt .\dist\armcom\src
