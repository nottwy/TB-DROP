tar -zxvf pipeline.tar.gz 
usermod -d /var/lib/mysql mysql
service mysql start
mysql -uroot < /root/pipeline/tb-visualization/01.software/create.sql
nohup python3 /root/pipeline/tb-visualization/03.server/flask/run.py &> /dev/null &

