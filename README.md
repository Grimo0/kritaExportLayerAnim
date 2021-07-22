# kritaExportCompositionAnim

A python plugin for [Krita](https://krita.org/).

It exports layers in files. All layers up to the specified depth (2 by default) not containing NE in their name will be exported.

## Installation

- Close Krita
- Execute the *copy.bat* (or the *mklink.bat* if you forked this project) as an admin.
- Launch Krita 
- In Settings/Configure Krita/Python Plugin Manager, make sure that Export Composition Anim is activated
- Optionnaly. Change the shortcut (`Ctrl+Alt+Shift+E` by default).

## TODO
- [x] Add bash to create symlink in krita pykrita and actions folder (the later might not exist)
- [x] Add jpg option
- [ ] Add jpg parameters 
- [ ] Add depth of layers to export