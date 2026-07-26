; Script generated for TwinBrowser Inno Setup Installer
#define MyAppName "TwinBrowser"
#define MyAppVersion "3.0"
#define MyAppPublisher "TwinBrowser"
#define MyAppExeName "TwinBrowser.exe"

[Setup]
AppId={{D739818C-5D21-4E67-A2C3-936611BA623E}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
; Default Install Path (User can choose any drive like D:\, E:\, etc. during setup)
DefaultDirName=C:\TwinBrowser
DisableDirPage=no
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=installer_dist
OutputBaseFilename=TwinBrowser_Setup
SetupIconFile=twin.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\TwinBrowser.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
