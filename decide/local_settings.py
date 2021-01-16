ALLOWED_HOSTS = ["*"]

# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]

BASEURL = 'https://guadalentin-visualizacion.herokuapp.com/'

APIS = {
    'authentication': BASEURL,
    'base': BASEURL,
    'booth': BASEURL,
    'census': BASEURL,
    'mixnet': BASEURL,
    'postproc': BASEURL,
    'store': BASEURL,
    'visualizer': BASEURL,
    'voting': BASEURL,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd3vluoj2jnujlr',
        'USER': 'tqczpqfauhtxas',
        'PASSWORD': 'ad28c32b4d7354de54de17a3d4ba141961fb7e7b65895fdfa9f2c351754fad58',
        'HOST': 'ec2-34-254-24-116.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256