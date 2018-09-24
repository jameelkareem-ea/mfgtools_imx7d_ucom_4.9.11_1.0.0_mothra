Set wshShell = CreateObject("WScript.shell")
wshShell.run "mfgtool2.exe -c ""Linux"" -l ""BootLoadersToEmmc"" -s ""board=imx7dea-ucom"" -s ""dtb=kit"" -s ""mmc=2"" -s ""rootfs=core-image-base"" "
Set wshShell = Nothing


