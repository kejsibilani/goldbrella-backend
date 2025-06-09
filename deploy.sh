set -e

echo "Reloading Daemons"
sudo systemctl daemon-reload
echo "Restarting Daphne"
sudo systemctl restart daphne
echo "Deployment Done"
