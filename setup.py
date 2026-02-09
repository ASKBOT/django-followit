from setuptools import setup, find_packages

setup(
    name="django-followit",
    version='0.7.0',
    description='A Django application that allows users to follow django model objects',
    packages=find_packages(),
    author='Evgeny.Fadeev',
    author_email='evgeny.fadeev@gmail.com',
    license='BSD License',
    keywords='follow, database, django',
    url='https://github.com/ASKBOT/django-followit',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    long_description=''.join(open('README.rst', 'r').readlines()[4:]),
    long_description_content_type='text/x-rst'
)
