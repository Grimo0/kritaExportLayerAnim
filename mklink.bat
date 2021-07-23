mklink /D "%USERPROFILE%\AppData\Roaming\krita\pykrita\exportLayerAnim" %~dp0\exportLayerAnim
mklink "%USERPROFILE%\AppData\Roaming\krita\pykrita\exportLayerAnim.desktop" %~dp0\exportLayerAnim.desktop
mkdir "%USERPROFILE%\AppData\Roaming\krita\actions"
mklink "%USERPROFILE%\AppData\Roaming\krita\actions\exportLayerAnim.action" %~dp0\exportLayerAnim.action
pause