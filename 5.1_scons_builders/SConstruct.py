bld = Builder(
    action='echo OUTPUT: $TARGETS, $SOURCES',
    src_suffix='.c',
    suffix='.help'
)
env = Environment(BUILDERS={'Foo': bld})
node = env.Foo(target='linker_files', source='hello.c')

# Node name has is now called hello.help
# I want to change the "hello" part of the file
# If that is possible
print(node)
