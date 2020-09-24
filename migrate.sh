./use_mysql.sh

if [[ -z $1 ]]; then
    echo "You should set migration name"
fi

python3 manage.py db migrate -m "$1"
