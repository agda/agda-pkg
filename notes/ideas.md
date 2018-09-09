Clean: It's working...

Init:
Esta faltando
- crear una carpeta para los repositorios: package-sources
- para cada paquete encontrado en package-index:
  leer el archivo .agda-lib y insertar en la base de datos:
  una entrada en libreria para:
    nombre+version, git-url, sha

Download: revisar en la base de datos si existe el nombre de la libreria, si
sí: descargar el repositorio en la carpeta actual, primero en un directorio
temporal or, la carpeta especificada outputdir, ajustar la version (tag) del
commit. El nombre podria especificar la version del paquete con "@"

Install:
  - donwload to outputdir=package-sources
  - check dependencies, check include
  - write defaults
  - write libraries

Uninstall:
  - check the name in the database
  - if so, confirm, the uninstallation,
    - remove the package from:
      - package-source
      - defaults
      - libraries
      - database installed packages

Info:
  - check if the package is installed, if so,
  - read from the database the Info
  - pretty print the info

Search:
  - full-text search

Upgrade:
  - It's working...


No necesariamente se instala, pero podria ser una [y/n] question al final.
