set -e

echo "Pulling code from GitHub"
git pull
echo "Reloading Daemons"
sudo systemctl daemon-reload
echo "Restarting Daphne"
sudo systemctl restart daphne
echo "Deployment Done"
