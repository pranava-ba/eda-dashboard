; Inno Setup script for EDA Dashboard v3 (PyQt6 + WebEngine, one-folder build)
;
; Prerequisite: run  python build_qt.py  first, so dist\EDA_Dashboard\ exists.
; Then open this file in Inno Setup (https://jrsoftware.org/isdl.php) and Compile.
; Output: installer_output\EDA_Dashboard_v3_Setup.exe

[Setup]
AppName=EDA Dashboard
AppVersion=2.0.9
AppPublisher=Pranava Baascaran
DefaultDirName={autopf}\EDA_Dashboard
DefaultGroupName=EDA Dashboard
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputDir=installer_output
OutputBaseFilename=EDA_Dashboard_v3_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
MinVersion=10.0
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
; Ship the entire one-folder PyInstaller output.
Source: "dist\EDA_Dashboard\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\EDA Dashboard"; Filename: "{app}\EDA_Dashboard.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\EDA Dashboard"; Filename: "{app}\EDA_Dashboard.exe"; WorkingDir: "{app}"; Tasks: desktopicon
Name: "{group}\Uninstall EDA Dashboard"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\EDA_Dashboard.exe"; Description: "{cm:LaunchProgram,EDA Dashboard}"; Flags: nowait postinstall skipifsilent
