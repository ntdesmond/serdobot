from settings import api, group
from random import randint
import re


class MessageParser:
    def __init__(self, msg):
        self.__message = msg.get("message")
        self.__client = msg.get("client_info")
        try:
            self.__response(self.__parse())
        except Exception as e:
            self.__response({"message": "An error has occurred. I'll notify the admin."})
            api.messages.send(random_id=randint(0, 2 ** 64), peer_id=group.get("ADMIN_ID"),
                              message=f"{str(e)}\n\nPeer: {self.__message.get('peer_id')}",
                              forward_messages=self.__message.get("id"))

    def __parse(self):
        cmd_args = re.fullmatch(r"\/(?P<command>[\w\.]+)(?: (?P<args>.+))?", self.__message.get("text", ""), re.S | re.I)
        if cmd_args:
            if self.__message.get("from_id") == group.get("ADMIN_ID"):
                cmd_args = cmd_args.groupdict()
                from commands import Command
                cmd = Command(cmd_args, self.__message)
                return cmd.result
            else:
                return {"message": "No way you do this!"}
        else:
            return {"message": "serdobot v0.0"}

    def __response(self, message):
        message.update({"peer_id": self.__message.get("peer_id"), "random_id": randint(0, 2 ** 64)})
        api.messages.send(**message)
