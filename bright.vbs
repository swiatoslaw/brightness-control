Set oShell = CreateObject("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c pipenv run python bright.py"
oShell.Run strArgs, 0, false