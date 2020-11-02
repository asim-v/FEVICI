## Plataforma social de Feria de Ciencias con Flask y Firebase



**Estructurado de la siguiente forma:
**
HECHO:

.firebase
.git
**apps/  **#endpoints extienden app.py**
**-     -about.py      #usuarios ingresan su perfil 
-     -calendar.py   #mostrará el objeto de calendario vinculado al usuario
-     -chat.py        #el chat funciona, le haré una interfaz
-     -expo.py      #aqui se ven todos los proyectos y se pueden ver completos los que así lo hayan señalado
-     -index.py     #landing page
-     -login.py     #landing page tambien
-     -project.py   #puede editar y invitar colaboradores y subir archivos
-     -register.py    #para registrar usuarios nuevos
-     -firebase_user_auth.py        #un pequeño modulo que uso para guardar nuevas entradas  y archivos en la base de datos
-     -teams.py      #para recibir y enviar invitaciones 

**static/**
    -aún falta mover los archivos estáticos aquí, hasta ahora todos son autocontenidos en el html

**templates/**
    visualizations/ 
        -Aqui hay visualizaciones interactivas autocontenidas que se cargan aleatoriamente al acceder por primera vez al sitio y también deben ser visibles desde el centro de recursos
    -about.html 
    -calendar.html
    -chat.html
    -expo.html
    -header.html    #todas las plantillas heredan js o css de aquí, y son insertadas en el {{block body}}
    -index.html
    -login.html
    -new-note.html   #usado para pruebas de chat
    -project.html
    -test.html

**app.py**  #registra todos los blueprints de apps/ y construye la app
**init.py **  #todos los blueprints heredan dependencias y variables globales de aquí!
firebase_user_auth.py     #un modulo que hice para facilitar la conexión a firebase-admin y insertar o sacar entradas

otros(404,gitignore,firebasearc)
GitHub
asim-v/FEVICI
fevici.web.app. Contribute to asim-v/FEVICI development by creating an account on GitHub.

**POR HACER:
**
VENTANA PARA ACADEMICO Básicamente poder 
registrarte como juez o ponente y poder explorar los proyectos, ver el pdf embedido y poder señalar comentarios y retrolalimentación, poder hacer queries o buscedas ordenadas por categorías y la opción de chatear con los miembros. (solo podrá criticar los proyectos si está habilitada la revisión en el panel admin)
    -- Los jueces pueden agregar eventos , explorar y criticar los proyectos
    ----- La crítica de proyectos se hace asignando una puntuación con esta rúbrica: https://shorturl.at/opsyP
    -- Los ponentes pueden agregar eventos y explorar proyectos
    -- Los eventos son talleres platicas o conferencias que el participante puede explorar en la ventana calendario en su plataforma y decidir a cual asistir, cuando decide a cual asistir se agrega automaticamente a su calendariio de google.

BLOG : En la landing page, no necesita registro,  estaba pensando usar de un folder de Google Drive por simplicidad y poder agregar docs al folder y cada vez que alguien entre al blog, parsear esos documentos

CENTRO DE RECURSOS Básicamente los recursos interactivos que ya existen, enlistados y al seleccionarlos tener toda la página para interactuar con ellos

ACTUALIZACIONES Y ALERTAS Verificación por correo, poder invitar usuarios a un proyecto por correo, envia una URL, y cuando entren con esa url puedan registrarse directamente a ese equipo.

PANEL ADMIN Control de acceso-edición o agregar a la BD, se borra todo, se pueden agregar/eliminar objetos de colaboradores, estos objetos tienen varios atributos: 
    -Nombre
    -Premio que ofrecen (puede ser nulo y  si tienen un premio se muestra en la landing page)
    -Imagen(se mostrará en el carrusel de la laning page)
    -Sitio de referencia(A donde quieren que vincule el link de su icono en el carrusel)
