# poetry-plugin-latest

poetry plugin to add a command to check if all dependencies are up-to-date

```cmd
$ poetry latest --help

Description:
  Check if all top-level dependencies are up-to-date

Usage:
  latest [options] [--] [<package>]

Arguments:
  package                    The package to inspect

Options:
      --without=WITHOUT      The dependency groups to ignore. (multiple values allowed)
      --with=WITH            The optional dependency groups to include. (multiple values allowed)
      --only=ONLY            The only dependency groups to include. (multiple values allowed)
  -l, --latest               Show the latest version. (option is always True)
  -o, --outdated             Show the latest version but only for packages that are outdated. (option is always True)
  -T, --top-level            Show only top-level dependencies. (option is always True)
  -h, --help                 Display help for the given command. When no command is given display help for the list command.
  -q, --quiet                Do not output any message.
  -V, --version              Display this application version.
      --ansi                 Force ANSI output.
      --no-ansi              Disable ANSI output.
  -n, --no-interaction       Do not ask any interactive question.
      --no-plugins           Disables plugins.
      --no-cache             Disables Poetry source caches.
  -C, --directory=DIRECTORY  The working directory for the Poetry command (defaults to the current working directory).
  -v|vv|vvv, --verbose       Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug.

Help:
  The show command displays detailed information about a package, or
  lists all packages available.
```
