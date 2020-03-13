from settings import api


class Command:
    """
        A class that contains all the possible commands.
        Note: every function documentation is used for help() command
    """

    def __init__(self, commandline, message):
        self.__message = message
        self.__paramstr = commandline.get("args", "")  # Set the args to an empty string if they were not passed
        self.__name = commandline["command"]

        from inspect import getmembers, ismethod
        self.__cmdlist = dict(filter(lambda member: member[0][0] != "_" and ismethod(member[1]), getmembers(self)))
        self.result = self._wrap(self._execute())

    def _execute(self):
        """
            Returns the function result if the function exists
        """
        if self.__name in self.__cmdlist:
            return self.__cmdlist[self.__name]()
        else:
            return "Unknown command."

    def _wrap(self, outcome):
        """
            Makes a message object out of text if necessary and checks output validity
        """
        if isinstance(outcome, str):
            # Wrap a string
            return {"message": outcome}
        elif isinstance(outcome, dict) and (outcome.get("message") or outcome.get("attachment")):
            # Just return already wrapped content
            return outcome
        else:
            # Error if no way to wrap
            return {"message": f"{self.__name}: Command result cannot be shown."}

    def help(self):
        """
            Usage: /help [commands]
            Shows all the available commands or help on specified ones
        """
        from inspect import getdoc
        if self.__paramstr:
            cmd_list = {name: getattr(self, name) for name in self.__paramstr.split(" ")}
            return '\n\n'.join([getdoc(cmd_list[name]) for name in cmd_list])
        else:
            return '\n'.join([f"/{name}: {''.join(getdoc(self.__cmdlist[name]).splitlines(True)[1:]) or 'No description'}" for name in self.__cmdlist])

    def pm(self):
        """
            Usage: /pm <peer> <message content>
            Send a message to the specified peer
        """
        parts = self.__paramstr.split(" ")
        peer_id = 0
        if parts[0][0] == "c":
            parts[0] = parts[0][1:]
            peer_id = 2000000000
        try:
            peer_id += int(parts[0])
            from random import randint
            api.messages.send(random_id=randint(0, 2 ** 64), peer_id=peer_id, message=" ".join(parts[1:]))
            return "Message sent"
        except ValueError:
            return "pm: wrong peer id!"
        except Exception as e:
            return str(e)

    def exec(self):
        """
            Usage: /exec <code>
            Execute given code and return the result
        """
        try:
            return str(eval(self.__paramstr))
        except Exception as e:
            return str(e)
