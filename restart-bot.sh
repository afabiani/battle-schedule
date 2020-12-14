sudo systemctl stop supervisor
sudo pkill -9 -f botpoll
echo " - killed"
sudo ps aux | grep botpoll
touch battle_schedule/wsgi.py
sudo systemctl restart supervisor
echo " - restarted"
