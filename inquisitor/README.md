┌─────────────────────────────────────────────────────┐
│             CYCLE DE VIE D'UNE ENTRÉE ARP           │
└─────────────────────────────────────────────────────┘


1. BESOIN
   PC A veut communiquer avec PC B
   └─► Consulte sa table ARP
       └─► Entrée trouvée ? OUI → Utilise la MAC
           │                  NON → Suite...
           ↓

2. ARP REQUEST (Broadcast) - sur le network
   "Qui a l'IP X.X.X.X ?"
   └─► Envoyé à ff:ff:ff:ff:ff:ff (tout le monde)

3. ARP REPLY (Unicast)
   "C'est moi ! Ma MAC est YY:YY:YY:YY:YY:YY"
   └─► Envoyé uniquement au demandeur

4. MISE À JOUR TABLE
   PC A enregistre : IP ↔ MAC

5. UTILISATION
   Communication directe pendant ~60-300 secondes

6. EXPIRATION
   Entrée devient STALE puis supprimée
   └─► Retour à l'étape 1 si besoin


Pourquoi ARP existe ?
Traduire IP → MAC car le matériel ne comprend que les MACs

Pourquoi les tables ARP expirent ?
Pour s'adapter aux changements (mobilité, nouveaux équipements)


Pourquoi ARP poisoning fonctionne ?
Aucune sécurité, les réponses ARP sont acceptées sans vérification

Quelle différence entre Request (op=1) et Reply (op=2) ?
Request = "who-has" (question), Reply = "is-at" (réponse)