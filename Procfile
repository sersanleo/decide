% prepara el repositorio para su despliegue. 
release: sh -c 'cd decide && python manage.py makemigrations authentication && python manage.py migrate && echo "from django.contrib import *; User = auth.get_user_model(); User.objects.create_superuser('admin', 'admin@admin.com', 'M', 'N', password='admin')" | python manage.py shell'
% especifica el comando para lanzar Decide
web: sh -c 'cd decide && gunicorn decide.wsgi --log-file -'