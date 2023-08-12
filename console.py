#!/usr/bin/python3
"""Module for the entry point of the command interpreter."""

import cmd
from models.base_model import BaseModel
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):

    """Program entry point and manipulation class"""

    prompt = "(hbnb) "

    def default(self, line_data):
        """" handles unverified_data commands"""
        self._precmd(line_data)

    def _precmd(self, line_data):
        """Tests commands for class.syntax()"""
        verified_data = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line_data)
        # egUser.show("877548969gygy")
        if not verified_data:
            return line_data
        classname = verified_data.group(1)  # eg User
        method = verified_data.group(2)  # show
        args = verified_data.group(3)  # "877548969gygy"
        verified_data_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if verified_data_uid_and_args:
            uid = verified_data_uid_and_args.group(1)
            dict_or_attr = verified_data_uid_and_args.group(2)
        else:
            uid = args
            dict_or_attr = False

        attr_and_value = ""
        if method == "update" and dict_or_attr:
            verified_data_dict = re.search('^({.*})$', dict_or_attr)
            if verified_data_dict:
                self.update_dict(classname, uid, verified_data_dict.group(1))
                return ""
            verified_data_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', dict_or_attr)
            if verified_data_attr_and_value:
                attr_and_value = (verified_data_attr_and_value.group(
                    1) or "") + " " + (verified_data_attr_and_value.group(2) or "")
        user_command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(user_command)  # show User "877548969gygy"
        return user_command

    def update_dict(self, classname, uid, s_dict):
        """Method to update from Dictonary"""
        new_str = s_dict.replace("'", '"')
        dict_ = json.loads(new_str)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            Entry = "{}.{}".format(classname, uid)
            if Entry not in storage.all():
                print("** no instance found **")
            else:
                properties = storage.properties()[classname]
                for property, value in dict_.items():
                    if property in properties:
                        value = properties[property](value)
                    setattr(storage.all()[Entry], property, value)
                storage.all()[Entry].save()

    def do_EOF(self, line_data):
        """Handles End Of File character.
        """
        print()
        return True

    def do_quit(self, line_data):
        """Terminates the program.
        """
        return True

    def emptyline_data(self):
        """Doesn't do anything on ENTER.
        """
        pass

    def do_create(self, line_data):
        """Creates an instance.
        """
        if line_data == "" or line_data is None:
            print("** class name missing **")
        elif line_data not in storage.classes():
            print("** class doesn't exist **")
        else:
            b = storage.classes()[line_data]()
            b.save()
            print(b.id)

    def do_show(self, line_data):
        """Prints the string representation of an instance.
        """
        if line_data == "" or line_data is None:
            print("** class name missing **")
        else:
            content = line_data.split(' ')
            if content[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(content) < 2:
                print("** instance id missing **")
            else:
                Entry = "{}.{}".format(content[0], content[1])
                if Entry not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[Entry])

    def do_destroy(self, line_data):
        """Deletes an instance based on the class name and id.
        """
        if line_data == "" or line_data is None:
            print("** class name missing **")
        else:
            content = line_data.split(' ')
            if content[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(content) < 2:
                print("** instance id missing **")
            else:
                Entry = "{}.{}".format(content[0], content[1])
                if Entry not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[Entry]
                    storage.save()

    def do_all(self, line_data):
        """Prints all string representation of all instances.
        """
        if line_data != "":
            content = line_data.split(' ')
            if content[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                nl = [str(obj) for Entry, obj in storage.all().items()
                      if type(obj).__name__ == content[0]]
                print(nl)
        else:
            new_list = [str(obj) for Entry, obj in storage.all().items()]
            print(new_list)

    def do_count(self, line_data):
        """Counts the instances of a class.
        """
        content = line_data.split(' ')
        if not content[0]:
            print("** class name missing **")
        elif content[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            verified_dataes = [
                k for k in storage.all() if k.startswith(
                    content[0] + '.')]
            print(len(verified_dataes))

    def do_update(self, line_data):
        """Updates an instance by adding or updating property.
        """
        if line_data == "" or line_data is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        verified_data = re.search(rex, line_data)
        classname = verified_data.group(1)
        uid = verified_data.group(2)
        attribute = verified_data.group(3)
        value = verified_data.group(4)
        if not verified_data:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            Key = "{}.{}".format(classname, uid)
            if Key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                _typ = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        _typ = float
                    else:
                        _typ = int
                else:
                    value = value.replace('"', '')
                properties = storage.attributes()[classname]
                if attribute in properties:
                    value = properties[attribute](value)
                elif _typ:
                    try:
                        value = _typ(value)
                    except ValueError:
                        pass
                setattr(storage.all()[Key], attribute, value)
                storage.all()[Key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
