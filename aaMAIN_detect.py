from github import Github
import time

import action
import ejecutorDCodes

g = Github(action.TOKEN)

repo_name = 'agusventm-lang/pricipal-repositori'



repo = g.get_repo(repo_name)

print(f'\naccediendo a repsitorio: {repo.name}')
print('\n______________________________________________\n')

repo_change = repo.pushed_at
print(repo_change)

action.on_detect()
#asi hacemos q clone el repositorio


ejecutorDCodes.main()
#esto ejecutamos el repositorio al inicio



while True:
    repo = g.get_repo(repo_name)
    if repo_change != repo.pushed_at:#detecta cambios en el repositorio


        print('\n\n!repositorio editado y detectado\n\n')

        action.on_detect()
        ejecutorDCodes.main()
        
        repo_change = repo.pushed_at

    
    time.sleep(1)

    

