import os
import shutil
import subprocess
from pathlib import Path
import string
import random


def findfile(startdir, pattern):
    for root, dirs, files in os.walk(startdir):
        for name in files:
            if name.find(pattern) >= 0:
                return root + os.sep + name


def venv_controll(code, stinput):
    VENV_NAME = 'venviroment'
    REQUIREMENTS = 'requirements.txt'

    process1 = subprocess.run(['where.exe', 'python3'], capture_output=True, shell=True, text=True)

    if process1.returncode != 0:
        raise OSError('Sorry python3 is not installed')

    python_bin = process1.stdout.strip()

    print(f'Python found in: {python_bin}')

    try:
        create_venv = subprocess.run(["python3", '-m', 'venv', VENV_NAME + '/'], check=True, shell=True)

        if create_venv.returncode == 0:
            print(f'Your venv {VENV_NAME} has been created')

            pip_bin = f'{VENV_NAME}/Scripts/pip3'

            if Path(REQUIREMENTS).exists():
                print(f'Requirements file "{REQUIREMENTS}" found')
                print('Installing requirements')
                subprocess.run([pip_bin, 'install', '-r', REQUIREMENTS])

                print('Process completed! Now activate your environment with "source .venv/bin/activate"')

            else:
                print("No requirements specified ...")
    except Exception:
        print(f'Your venv {VENV_NAME} was already created')

    s = 7
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=s))

    print(name)

    # try:
    #     subprocess.run(['virtualenv-clone', VENV_NAME, name])
    # except EnvironmentError:
    #     print("nis")

    cwd = os.getcwd()
    print(cwd)
    subprocess.run(['Xcopy', '/E', '/I', VENV_NAME, name])
    subprocess.run(['Xcopy', code, name], check=True)
    os.remove(code)
    cal_dir = "/" + name
    os.chdir(cwd + cal_dir)
    removal = os.environ['PATH']
    os.environ['PATH'] = os.path.dirname(findfile(cwd + cal_dir, 'activate')) + os.pathsep + os.environ['PATH']
    print(os.environ['PATH'])
    p = subprocess.Popen([cwd + cal_dir + '/Scripts/python.exe', code],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input=bytes(stinput, 'utf-8'))
    # print(cwd + cal_dir + '/Scripts/python.exe')
    # os.system('python print.py')
    os.environ['PATH'] = removal
    os.chdir(cwd)
    shutil.rmtree(name)
    return stdout, stderr
