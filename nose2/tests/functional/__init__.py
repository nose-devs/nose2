import os
import subprocess

SUPPORT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'support'))

def support_file(*path_parts):
    return os.path.join(SUPPORT, *path_parts)



def run_nose2(*nose2_args, **popen_args):
    if 'cwd' in popen_args:
        cwd = popen_args.pop('cwd')
        if not os.path.isabs(cwd):
            popen_args['cwd'] = support_file(cwd)
    process = subprocess.Popen(
        ['python', '-m', 'nose2.__main__'] + list(nose2_args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **popen_args)
    output, err = process.communicate()
    retcode = process.poll()
    return retcode, output, err
