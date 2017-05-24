# -*- coding:utf8 -*-

_directory_regex = '\/[a-zA-Z0-9\/.+_-]+'
_linenumbers_regex = '(?::\d+){1,2}'
_lenient_path_regex = '%s(?:%s)?[,:]?' % (_directory_regex, _linenumbers_regex)

def theme(context):
    return context, [
        ["(^FAILED:)(.*)$", "red,red", "bold,normal"],
        ["(^ERROR:)(.*)$", "red,red", "bold,normal"],
        ["(^.*)( error: )", "red,red", "normal,bold"],
        ["(^.*)( warning: )", "yellow,yellow", "normal,bold"],
        ["(^.*)( note: )", "cyan,cyan", "normal,bold"],
        ["(^.*)( undefined reference to )", "red,red", "normal,bold"],
        ["(^.*)( undefined references to )", "red,red", "normal,bold"],
        ["(^.*)( multiple definition of )", "red,red", "normal,bold"],
        ["(^CMake Warning )(.*)$", "yellow,yellow", "bold,normal"],
        ["(^CMake Error )(.*)$", "red,red", "bold,normal"],
        ["(^Call Stack )(.*)$", "yellow,yellow", "bold,normal"],

        # CMake lines
        ["^-- Generating done.*", "green", "bold"],
        ["^-- Configuring done.*", "green", "bold"],
        ["^-- Configuring incomplete.*", "red", "bold"],
        ["^-- Found.*$", "green", "normal"],
        ["^--.*$", "cyan", "normal"],
        ["^.*CMake Warning.*$", "yellow", "faint"],

        # Paths
        ["In file included from", "white", "bold"],
        ["^\s+from ", "white", "bold"],
        ["^%s (?!(?:error|warning|note|undefined reference to| undefined references to |multiple definition of): )" % _lenient_path_regex, "white", "bold"],
        ["/usr/bin/ccache", "white", "bold"],
        ["/usr/bin/[gc]\+\+", "white", "bold"],

        # C++ Snippets
        ["‘.*’", "Cpp", "monokai"],
        ["'[^']*'", "Cpp", "monokai"],
        ["`[^']*'", "Cpp", "monokai"],

        # Events
        ["Building.*$", "black", "bold"],
        ["Automatic moc.*$", "black", "bold"],
        ["Linking.*$", "green", "bold"],
        ["Generating.*$", "blue", "bold"],
        [" [Ww]arning:", "yellow", "bold"],
        [" [Ee]rror:", "red", "bold"],
        [" error in ", "red", "bold"],

        ["undefined reference", "red", "bold"],
        ["incomplete type", "red", "normal"],
        ["collect2: error: ld returned 1 exit status", "red", "bold"],

        # Icecc
        ["^.*ICECC.*$", "red", "faint"],

        # Python Tracebacks etc.
        ["^Traceback.*$", "white", "bold"],
        ['  File "(/[a-zA-Z0-9/.+-_]+)", line (\d+)', "white,blue", "bold,bold"],

        # GCC Warning flags
        ["\[-W[-a-zA-Z]+\]", "yellow", "bold"],
        # GCC Error flags
        ["\[-f[-a-zA-Z]+\]", "red", "bold"],

        # Ninja Prefix
        ["^(\[\s*[0-9]+%\])", "Scale", "bold"],
        ["\{[0-9\/?s. -]+\} ", "cyan", "faint"],

        ["ninja: build stopped:.*$", "red", "bold"],

        # GCC Visualization
        ["[~^]", "green", "normal"]
    ]
