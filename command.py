#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import sys
import os
import shutil
from os.path import lexists


class Command(object):
    def execute(self):
        pass
    def undo(self):
      pass


class CopyFileCommand(Command):
    # TODO handle src parameter as path
    def __init__(self, src ):
        self.src = src
        self.dest = "Copy_"+src
        self.name = "Copy " + src

    def execute(self):
        self.copy(self.src, self.dest)

    def undo(self):
        print('remove {} '.format( self.dest))
        os.remove( self.dest)

    def copy(self , src,dest ):
        print('copy {} to {}'.format(src, dest))
        shutil.copy(src, dest)


class MoveFileCommand(Command):

    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
        self.name="Move "+src
    def execute(self):
        self.rename(self.src, self.dest)

    def undo(self):
        self.rename(self.dest, self.src)

    def rename(self, src, dest):
        print('renaming {} to {}'.format(src, dest))
        os.rename(src, dest)


def main():
    command_stack = []

    # commands are just pushed into the command stack
    command_stack.append(CopyFileCommand('foo1.txt'))
    command_stack.append(CopyFileCommand('Copy_foo1.txt'))

    command_stack.append(MoveFileCommand('foo.txt', 'bar.txt'))
    command_stack.append(MoveFileCommand('bar.txt', 'baz.txt'))

    names=["foo.txt","baz.txt","foo1.txt"]
    for name in names:
        try:
          os.unlink(name)
        except:
            pass
        finally:
            pass

    # verify that none of the target files exist
    assert(not lexists("foo.txt"))
    assert(not lexists("bar.txt"))
    assert(not lexists("baz.txt"))
    try:
        with open("foo.txt", "w") as src1:  # Creating the file
            src1.close()
        with open("foo1.txt", "w") as src2:  # Creating the file
            src2.close()

        # they can be executed later on
        for cmd in command_stack:
            print "******Executing "+cmd.name
            cmd.execute()

        # and can also be undone at will
        for cmd in reversed(command_stack):
            print "" \
                  "------Undo " + cmd.name
            cmd.undo()



    except :
        #e = sys.exc_info()[0]
        #print("Error: %s" % e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "*** print_exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)
        print "*** print_exc:"
        traceback.print_exc()
        print "*** format_exc, first and last line:"
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        print "*** format_exception:"
        print repr(traceback.format_exception(exc_type, exc_value,
                                              exc_traceback))
        print "*** extract_tb:"
        print repr(traceback.extract_tb(exc_traceback))
        print "*** format_tb:"
        print repr(traceback.format_tb(exc_traceback))
        print "*** tb_lineno:", exc_traceback.tb_lineno


    finally:
        print "finaly block  "
        os.unlink("foo.txt")
        os.unlink("foo1.txt")



if __name__ == "__main__":
    main()

### OUTPUT ###
# renaming foo.txt to bar.txt
# renaming bar.txt to baz.txt
# renaming baz.txt to bar.txt
# renaming bar.txt to foo.txt
