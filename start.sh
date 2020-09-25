source ../.env
export DATABASE_URL="mysql+pymysql://root:${PLATFORM_MYSQL_PASSWORD}@localhost:3306/${PLATFORM_MYSQL_DATABASE}"

python3 serve.py