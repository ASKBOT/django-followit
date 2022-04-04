from setuptools import setup, find_packages
import ez_setup
ez_setup.use_setuptools()

setup(
    name="django-followit",
    version='0.5.0',
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    long_description=''.join(open('README.rst', 'r').readlines()[4:]),
    long_description_content_type='text/x-rst'
)
