mklink /D "%USERPROFILE%\AppData\Roaming\krita\pykrita\exportCompositionAnim" %~dp0\exportCompositionAnim
mklink "%USERPROFILE%\AppData\Roaming\krita\pykrita\exportCompositionAnim.desktop" %~dp0\exportCompositionAnim.desktop
mkdir "%USERPROFILE%\AppData\Roaming\krita\actions"
mklink "%USERPROFILE%\AppData\Roaming\krita\actions\exportCompositionAnim.action" %~dp0\exportCompositionAnim.action
pause