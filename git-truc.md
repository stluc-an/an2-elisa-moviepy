# Donc normalement
Dans le terminal, dans le dossier du projet
- git remote add origin https://github.com/stluc-an/an2-elisa-moviepy.git
- git pull origin master

Si y'a des soucis parce qu'on n'a pas la même version pour l'instant:
- git stash
- git pull origin master
- git stash pop

Et plus tard après modifs
- git push --all origin
(mais ça on pourra le faire à partir de PyCharm)
