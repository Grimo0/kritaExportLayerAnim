mklink /D "%USERPROFILE%\AppData\Roaming\krita\pykrita\kritaExportLayerAnim" %~dp0\kritaExportLayerAnim
mklink "%USERPROFILE%\AppData\Roaming\krita\pykrita\kritaExportLayerAnim.desktop" %~dp0\kritaExportLayerAnim.desktop
mkdir "%USERPROFILE%\AppData\Roaming\krita\actions"
mklink "%USERPROFILE%\AppData\Roaming\krita\actions\kritaExportLayerAnim.action" %~dp0\kritaExportLayerAnim.action
pause