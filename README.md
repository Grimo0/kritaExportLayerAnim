# kritaExportCompositionAnim

A python plugin for [Krita](https://krita.org/).

It exports all root layers in distinct files.
Add `NE` to a layer to prevent it from being exported.
Add `EC` to a group layer to export it's child instead.

## Installation

- Download, clone or fork this project
- Close Krita
- Execute *copy.bat* (or *mklink.bat* if you cloned/forked this project) as an admin.
- Launch Krita 
- In Settings/Configure Krita/Python Plugin Manager, make sure that Export Composition Anim is activated
- Optionnaly. Change the shortcut (`Ctrl+Alt+Shift+E` by default).

## TODO
- [x] Add bash to create symlink in krita pykrita and actions folder (the later might not exist)
- [x] Add jpg option
- [x] Add option to export childs of a group instead of the group
- [ ] Add jpg parameters 
- [ ] Add option to export layers of the compositions