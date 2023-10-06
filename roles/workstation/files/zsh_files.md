# .zshenv

*Read every time*

This file is always sourced, so it should set environment variables which need to be updated frequently. `$PATH` (or its associated counterpart `$path`) is a good example because you probably don't want to restart your whole session to make it update. By setting it in that file, reopening a terminal emulator will start a new Zsh instance with the PATH value updated.

But be aware that this file is read even when Zsh is launched to run a single command (with the `-c` option), even by another tool like make. You should be very careful to not modify the default behavior of standard commands because it may break some tools (by setting aliases for example).

# .zprofile

*Read at login*

I personally treat that file like [.zshenv](#zshenv) but for commands and variables which should be set once or which don't need to be updated frequently:

environment variables to configure tools (flags for compilation, data folder location, etc.)
configuration which execute commands (like `SCONSFLAGS="--jobs=$(( $(nproc) - 1 ))"`) as it may take some time to execute.
If you modify this file, you can apply the configuration updates by running a login shell:
```
exec zsh --login
```

# .zshrc

*Read when interactive*

I put here everything needed only for interactive usage:
- prompt
- command completion
- command correction
- command suggestion
- command highlighting
- output coloring
- aliases
- key bindings
- commands history management
- other miscellaneous interactive tools (auto_cd, manydots-magic)...

# .zlogin

*Read at login*

This file is like [.zprofile](#zprofile), but is read after .zshrc. You can consider the shell to be fully set up at .zlogin execution time

So, I use it to launch external commands which do not modify shell behaviors (e.g. a login manager).

# .zlogout

*Read at logout, Within login shell*

Here, you can clear your terminal or any other resource which was setup at login.

How I choose where to put a setting
- if it is needed by a command run non-interactively: [.zshenv](#zshenv)
- if it should be updated on each new shell: [.zshenv](#zshenv)
- if it runs a command which may take some time to complete: [.zprofile](#zprofile)
- if it is related to interactive usage: [.zshrc](#zshrc)
- if it is a command to be run when the shell is fully setup: [.zlogin](#zlogin)
- if it releases a resource acquired at login: [.zlogout](#zlogout)

Pilfered from [this StackExchange post](https://unix.stackexchange.com/questions/71253/what-should-shouldnt-go-in-zshenv-zshrc-zlogin-zprofile-zlogout).