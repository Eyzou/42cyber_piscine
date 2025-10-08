🚀 Construction et démarrage

1. Construire l'image
make all
2.  Obtenir l'adresse .onion
make logs
3. Tester SSH via Tor
torsocks ssh -i /home/ehamm/.ssh/id_ed25519 -p 4242 ehamm@[ADRESSE.onion]
4. Tester HTTP via Tor
torsocks curl http://[ADRESSE.onion] 
5. Tester HTTP en local
curl localhost:80

Others
hostname
ps aux | grep -E 'tor|ssh|nginx' (process en cours)
ss -tlnp
