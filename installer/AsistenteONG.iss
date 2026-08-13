; Inno Setup script for Asistente ONG
; Build the EXE first with build_exe.bat or the GitHub Actions artifact.

#define MyAppName "Asistente ONG"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Asistente ONG"
#define MyAppExeName "AsistenteONG.exe"

[Setup]
AppId={{A8B9B9B4-7A0D-4B61-9E72-ONG2026A001}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Asistente ONG
DefaultGroupName=Asistente ONG
OutputDir=..\dist-installer
OutputBaseFilename=AsistenteONG-Setup-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "..\dist\AsistenteONG.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\docs\GUIA_USUARIO_FINAL.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\docs\PILOTO_USUARIOS.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\docs\DISTRIBUCION_NACIONAL.md"; DestDir: "{app}\docs"; Flags: ignoreversion

[Icons]
Name: "{group}\Asistente ONG"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Asistente ONG"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir Asistente ONG"; Flags: nowait postinstall skipifsilent
