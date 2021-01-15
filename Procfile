% prepara el repositorio para su despliegue. 
release: sh -c 'cd decide && python manage.py makemigrations authentication && python manage.py migrate && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell'
% especifica el comando para lanzar Decide
web: sh -c 'cd decide && gunicorn decide.wsgi --log-file -'