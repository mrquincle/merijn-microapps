from os.path import join, sep

from SCons.Script import DefaultEnvironment, SConscript

from platformio.builder.tools import platformio as platformio_tool

env = DefaultEnvironment()
env.Replace(
    PLATFORMFW_DIR=env.PioPlatform().get_package_dir("framework-cs-arduino")
)
