@echo off
call "C:\Program Files\QGIS 3.14\bin\o4w_env.bat"
call "C:\Program Files\QGIS 3.14\bin\qt5_env.bat"
call "C:\Program Files\QGIS 3.14\bin\py3_env.bat"

@echo on
pylupdate5 GisTools.pro
