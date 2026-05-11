import os
import requests
import statistics
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

# --- TES PARAMÈTRES DE GESTION ---
BANKROLL_INITIALE = 50.0  # Ton capital total dédié aux paris sportifs (ex: 1000€)
FRACTION_KELLY = 0.25       # 0.25 = Quart de Kelly (Recommandé par les pros)
# ---------------------------------

url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions=eu&markets=h2h&apiKey={api_key}"

print(f"🛡️ Radar activé | Capital : {BANKROLL_INITIALE}€ | Stratégie : 1/4 Kelly\n")
reponse = requests.get(url)

if reponse.status_code == 200:
    donnees = reponse.json()
    value_bets_trouves = []
    
    for match in donnees:
        bookmakers = match.get('bookmakers', [])
        
        if len(bookmakers) > 0:
            equipe_domicile = match['home_team']
            equipe_exterieur = match['away_team']
            cotes_disponibles = []
            
            for bookie in bookmakers:
                nom_bookie = bookie['title']
                for market in bookie['markets']:
                    if market['key'] == 'h2h':
                        for outcome in market['outcomes']:
                            if outcome['name'] == equipe_domicile:
                                cote = outcome['price']
                                if cote <= 10.0: 
                                    cotes_disponibles.append((nom_bookie, cote))
            
            if len(cotes_disponibles) >= 3: 
                cotes_disponibles.sort(key=lambda x: x[1], reverse=True)
                meilleur_bookie, meilleure_cote = cotes_disponibles[0]
                
                valeurs_cotes = [c[1] for c in cotes_disponibles]
                oracle_cote = statistics.median(valeurs_cotes)
                probabilite_reelle = 1 / oracle_cote
                
                ev = (probabilite_reelle * meilleure_cote) - 1
                
                if 0 < ev < 0.20:
                    # --- NOUVEAU : CALCUL DU CRITÈRE DE KELLY ---
                    b = meilleure_cote - 1
                    q = 1 - probabilite_reelle
                    
                    kelly_plein = (probabilite_reelle * b - q) / b
                    kelly_ajuste = kelly_plein * FRACTION_KELLY
                    
                    # On calcule la mise en euros
                    mise_recommandee = BANKROLL_INITIALE * kelly_ajuste
                    
                    value_bets_trouves.append({
                        'match': f"{equipe_domicile} vs {equipe_exterieur}",
                        'equipe': equipe_domicile,
                        'cote': meilleure_cote,
                        'bookmaker': meilleur_bookie,
                        'ev_pourcentage': ev * 100,
                        'mise': mise_recommandee,
                        'pourcentage_br': kelly_ajuste * 100
                    })

    if len(value_bets_trouves) > 0:
        value_bets_trouves.sort(key=lambda x: x['ev_pourcentage'], reverse=True)
        
        print("🏆 LE TOP 3 DES OPPORTUNITÉS SÉCURISÉES :")
        print("-" * 50)
        for i, pari in enumerate(value_bets_trouves[:3]):
            print(f"#{i+1} Match : {pari['match']}")
            print(f"    👉 Pari : Victoire de {pari['equipe']}")
            print(f"    🔥 Cote : {pari['cote']} (chez {pari['bookmaker']})")
            print(f"    📈 Avantage Mathématique (EV) : +{pari['ev_pourcentage']:.2f} %")
            print(f"    💰 MISE CONSEILLÉE : {pari['mise']:.2f}€ ({pari['pourcentage_br']:.2f}% de la Bankroll)")
            print("-" * 50)
    else:
        print("❌ Aucun Value Bet 100% fiable trouvé sur le marché pour l'instant.")
            
else:
    print(f"Erreur de connexion : {reponse.status_code}")
