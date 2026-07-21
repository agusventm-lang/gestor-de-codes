
import os
import stat
import shutil
import subprocess

import ejecutorDCodes

from github import Github

TOKEN = 'coloque token aqui'

g = Github(TOKEN)

repo_name = 'agusventm-lang/pricipal-repositori'

repo = g.get_repo(repo_name)

RUTA_CARPETA = fr'{os.getcwd()}\repo_clone'



def _eliminar_item(item):
    if os.path.isdir(item) and not os.path.islink(item):
        def onerror(func, path, exc_info):
            if isinstance(exc_info[1], PermissionError):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            else:
                raise exc_info[1]

        shutil.rmtree(item, onerror=onerror)
    else:
        if os.path.exists(item) or os.path.islink(item):
            if os.path.exists(item):
                os.chmod(item, stat.S_IWRITE)
            os.remove(item)

#limpiar carpeta accede a _eliminar_item

def limpiar_carpeta():
    os.makedirs(RUTA_CARPETA, exist_ok=True)

    if os.path.exists(RUTA_CARPETA):
        for nombre in os.listdir(RUTA_CARPETA):
            item = os.path.join(RUTA_CARPETA, nombre)
            _eliminar_item(item)

#on_detect accede a limpiar carpeta





def on_detect():
    limpiar_carpeta()
    
    subprocess.run(["git", "clone", repo.clone_url, RUTA_CARPETA], check=True)

    ejecutorDCodes.main()
    

