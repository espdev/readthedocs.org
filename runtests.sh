cd readthedocs
rm -rf rtd_tests/builds/
export PYTHONPATH=`pwd`:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=settings.test
coverage run -m py.test $*
exit=$?
cd -
exit $exit
