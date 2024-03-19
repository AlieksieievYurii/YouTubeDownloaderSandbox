set -x
docker run --name some-mysql --rm -e MYSQL_ROOT_PASSWORD=yurii -p 3306:3306 -v D:/Projects/YouTubeDownloader/back/auth/init.sql:/docker-entrypoint-initdb.d/init.sql mysql:latest