import sys
import click

def _echo(message, color="reset"):
    click.secho(message, fg=color)

@click.group()
@click.version_option("1.0.0")
def fastdeploy_cli():
    """FastDeploy CLI"""
    print("CLI")

@fastdeploy_cli.command(
    help="Generate and save the entire module from a python file",
    short_help="Save module from path",
)
@click.option(
    '--path',
    type=click.STRING,
    default=".",
    help='The path to .py file'
            'Example: "--path D:\PythonProjects\HelloWorld.py"'
            'Example: "--path HelloWorld.py"',
)
def build(path):
    if path[-2:] != "py":
        raise Exception("the file is not a python file")

    import os
    import importlib
    import inspect
    from fastdeploy.myfunctions import LambdaService
    
    complete_path = os.path.join(os.getcwd(), path)
    head, module_name = os.path.split(complete_path)
    sys.path.append(head)
    module_name = module_name[:-3]
    try:
        module = importlib.import_module(module_name)
    except Exception as e:
        raise Exception(f"Couldn't import module:", e)
    
    count = 0
    classObj = None
    
    for name, obj in inspect.getmembers(module):
        try:
            if inspect.isclass(obj) and issubclass(obj, LambdaService):
                classObj = obj
        except:
            pass
    try:
        #move all source files into build folder
        root_dir = os.getcwd()
        temp_dir = root_dir + r'\build'
        build_dir = temp_dir
        import shutil
        listOfFiles = os.listdir(root_dir)    
        # print(listOfFiles)
        
        try:
            os.mkdir(temp_dir)
        except Exception as e:
            os.rmdir(temp_dir)
        for files in listOfFiles:
            try:
                shutil.copy(files,temp_dir)
            except Exception as e:
                print(e)
        
        LambdaService.create_fastapi_file(classObj,module_name)
            
        #create requirements.txt
        try:
            from pip._internal.operations import freeze
        except ImportError:  # pip < 10.0
            from pip.operations import freeze
        x = freeze.freeze()

        with open("build\\requirements.txt", "w") as file1:
            # Writing data to a file
            for p in x:
                    file1.write(p)
                    file1.write('\n')
            file1.write("fastapi\nuvicorn\nclick")
                    
        #create vercel.json
        vercel_json = """{
    "builds": [
        {"src": "/api.py", "use": "@vercel/python"}
    ],
    "routes": [
        {"src": "/(.*)", "dest": "/api.py"}
    ]
}
"""
        with open("build\\vercel.json", "w") as file1:
            file1.write(vercel_json)
        
    except Exception as e:
        print(e)
        _echo(f"Couldn't save files")
    _echo("Saved all the necessary modules.")
    return fastdeploy_cli
@fastdeploy_cli.command(
    help="Deploy your build folder onto vercel",
)
def deploy():
    import os
    if not os.path.exists('build'):
        print('Please build your project before you deploy')
        return
    os.system('vercel build')