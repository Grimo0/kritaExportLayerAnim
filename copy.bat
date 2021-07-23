cd /D %USERPROFILE%\AppData\Roaming\krita\
xcopy /S %~dp0\exportLayerAnim "pykrita\exportLayerAnim"
xcopy %~dp0\exportLayerAnim.desktop "pykrita\exportLayerAnim.desktop"
mkdir "actions"
xcopy %~dp0\exportLayerAnim.action "actions\exportLayerAnim.action"