; --- Configuración básica ---
[Setup]
AppName=Practical Speech
AppVersion=1.0
DefaultDirName={pf}\Practical Speech
DefaultGroupName=Practical Speech
OutputDir=.
OutputBaseFilename=Practical_Speech_Installer
Compression=lzma
SolidCompression=yes

; --- Archivos que se copiarán ---
[Files]
Source: "dist\main.exe"; DestDir: "{app}"
Source: "img\*"; DestDir: "{app}\img"; Flags: recursesubdirs
Source: "vosk-model-en-us-0.22-lgraph\*"; DestDir: "{app}\vosk-model-en-us-0.22-lgraph"; Flags: recursesubdirs
Source: "voices\*"; DestDir: "{app}\voices"; Flags: recursesubdirs
Source: "teacher\*"; DestDir: "{app}\teacher"; Flags: recursesubdirs

; --- Creación de accesos directos ---
[Icons]
Name: "{commondesktop}\Practical Speech"; Filename: "{app}\main.exe"; IconFilename: "{app}\img\icono.ico"
Name: "{group}\Desinstalar Practical Speech"; Filename: "{uninstallexe}"
; Name: "{commondesktop}\Desinstalar Practical Speech"; Filename: "{uninstallexe}"  ; ← Descomenta si quieres en el escritorio

; --- Ejecutar programa después de instalar ---
[Run]
Filename: "{app}\main.exe"; Description: "Iniciar Practical Speech"; Flags: nowait postinstall skipifsilent
