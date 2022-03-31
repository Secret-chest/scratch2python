from configMeta import *
import i18n
_ = i18n.t

"""
Scratch2Python config

Each option has its own description. Have fun!
"""

# Enable insane values
INSANE: bool = False

# Language
# Supported languages:
# 🇬🇧 English - en
# 🇷🇴 limba română - ro
language: str = "en"

# Project load method
# Sets the behavior for loading projects.
# Possible values:
# manual: use the project file name defined in the "projectFileName" variable.
# interactive: use input().
# cmdline: use command argument.
# filechooser: graphical file chooser.
# For now, it's easier to test using manual mode, so it's the default.
projectLoadMethod: str = "manual"

# Project file name
# If the "manual" mode is chosen, set the Scratch project file to load.
projectFileName: str = "projects/Cake.sb3"

# Extract on project run
# Set whether to extract the project assets on run.
extractOnProjectRun: bool = True

# Enable terminal output
# Set whether any output messages should be allowed.
enableTerminalOutput: bool = True

# Enable debug messages
# Set whether debug messages (messages to stderr) should be allowed.
enableDebugMessages: bool = True

# Enable Scratch Addons debugger logs
# This allows projects using Scratch Addons to print messages to the console. Vanilla Scratch doesn't support it.
showSALogs: bool = True

# Max FPS
# Set maximum frame rate. Most projects won't break, but they
# might be too fast (or too slow) as they may rely on screen refresh.
# You can also use TURBO to use turbo mode.
# Vanilla is 30.
maxFPS: int = 30

# Screen width/height
# Stage size. You can change that, but most projects won't work with it.
# A scaling mode will be added later.
# Vanilla is 480x360.
screenWidth: int = 480
screenHeight: int = 360

# Allow off-screen sprites
# Again, most projects will break.
# Vanilla is false.
allowOffScreenSprites: bool = False


# "For this project" values
# Don't edit these. They will break Scratch2Python controls.
# Edit your defaults above instead. The values here inherit them.
projectMaxFPS = maxFPS
projectScreenWidth = screenWidth
projectScreenHeight = screenHeight
projectAllowOffScreenSprites = allowOffScreenSprites


# ConfigError class
# Error for invalid settings.
class ConfigError(Exception):
    pass


i18n.set("locale", language)
i18n.set("filename_format", "{locale}.{format}")
i18n.load_path.append("lang/")

if not INSANE:
    if screenWidth < 240 or screenHeight < 180:
        raise ConfigError(_("config-warning-screen-too-small", res="240x180"))
    if screenWidth > 1920 or screenHeight > 1080:
        raise ConfigError(_("config-warning-screen-too-large", res="1920x1080"))
