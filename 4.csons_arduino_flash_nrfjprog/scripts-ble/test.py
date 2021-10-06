Import("env", "projenv")

# access to global construction environment
print(env)

# access to project construction environment
print(projenv)

# Dump construction environments (for debug purpose)
print(env.Dump())
print(projenv.Dump())

# append extra flags to global build environment
# which later will be used to build:
# - frameworks
# - dependent libraries
env.Append(CPPDEFINES=[
  "MACRO_1_NAME",
  ("MACRO_2_NAME", "MACRO_2_VALUE")
])

# append extra flags to only project build environment
projenv.Append(CPPDEFINES=[
  "PROJECT_EXTRA_MACRO_1_NAME",
  ("ROJECT_EXTRA_MACRO_2_NAME", "ROJECT_EXTRA_MACRO_2_VALUE")
])

