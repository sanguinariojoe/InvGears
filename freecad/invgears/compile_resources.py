import os
import subprocess as sub


def compile_resources():
    # try to create a resource file
    # assume either pyside2-rcc or pyside-rcc are available.
    # if both are available pyside2-rcc is used.
    rc_input = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resources", "InvGears.qrc"))
    rc_output = os.path.join(os.path.dirname(__file__), "InvGears_rc.py")
    try:
        try:
            proc = sub.Popen(["pyside2-rcc", "-o", rc_output, rc_input], stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
            out, err = proc.communicate()
        except FileNotFoundError:
            proc = sub.Popen(["pyside-rcc", "-o", rc_output, rc_input], stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
            out, err = proc.communicate()
        print(out)
        print(err)
    except Exception as e:
        print("An error occured while trying to create the resource file: \n" + str(e))


if __name__ == '__main__':
    compile_resources()
