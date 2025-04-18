from prompt_toolkit.completion import NestedCompleter

command_completer = NestedCompleter.from_nested_dict({
    "set": {
        "target": None,
        "scan": None
    },
    "show": {
        "options": None
    },
    "run": None,
    "history": None,
    "help": None,
    "exit": None,
    "quit": None
})
