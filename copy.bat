cd /D %USERPROFILE%\AppData\Roaming\krita\
xcopy /S exportCompositionAnim "pykrita\exportCompositionAnim"
xcopy exportCompositionAnim.desktop "pykrita\exportCompositionAnim.desktop"
mkdir "actions"
xcopy exportCompositionAnim.action "actions\exportCompositionAnim.action"