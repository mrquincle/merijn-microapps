from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
board = env.BoardConfig()

env.SConscript("arduino/nrf5.py")
