@echo off

if not exist %cd%\bin goto exit
if not exist %cd%\pkg goto exit
if not exist %cd%\src goto exit

set GOPATH=%cd%
go %*

:exit
echo check 'bin', 'pkg', 'src' directories exist.