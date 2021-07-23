cd /D %USERPROFILE%\AppData\Roaming\krita\
xcopy /S %~dp0\kritaExportLayerAnim "pykrita\kritaExportLayerAnim"
xcopy %~dp0\kritaExportLayerAnim.desktop "pykrita\kritaExportLayerAnim.desktop"
mkdir "actions"
xcopy %~dp0\kritaExportLayerAnim.action "actions\kritaExportLayerAnim.action"