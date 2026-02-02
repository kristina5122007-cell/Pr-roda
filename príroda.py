#príroda
from flask import Flask, render_template, jsonify, request
import requests

príroda = Flask(__name__)

MIESTA = {
    'tatry': {
        'nazov': 'Vysoké Tatry',
        'lat': 49.16, 'lon': 20.08,
        'vyska': '2 655 m n. m.',
        'rozloha': '738 km²',
        'fauna': 'Kamzík, svišť, medveď. Najčastejšie uvidíš kamzíka pri plesách.',
        'flora': 'Limba, Plesnivec. TRHAŤ: Nič! (Národný park).',
        'jedovate': 'Prilbica modrá (smrteľne jedovatá!).',
        'trasy_psy': 'ZÁKAZ vstupu so psami do vysokohorského terénu (nová vyhláška).',
        'trasy_bez': 'Rysy, Kriváň, Lomnický štít.',
        'body_zaujmu': 'Hrebienok, Popradské pleso, Skalnaté pleso.'
    },
    'raj': {
        'nazov': 'Slovenský raj',
        'lat': 48.91, 'lon': 20.38,
        'vyska': '1 153 m n. m.',
        'rozloha': '197 km²',
        'fauna': 'Vydra, bocian čierny. Často uvidíš dravé vtáky.',
        'flora': 'Vzácne orchidey. TRHAŤ: Bazový kvet (mimo 5. stupňa).',
        'jedovate': 'Vranie oko štvorlisté.',
        'trasy_psy': 'Prielom Hornádu (náročné pre labky), lúky na Glac.',
        'trasy_bez': 'Suchá Belá, Piecky (rebríky sú pre psy nebezpečné).',
        'body_zaujmu': 'Tomášovský výhľad, Dobšinská ľadová jaskyňa.'
    },
    'fatr': {
        'nazov': 'Malá Fatra',
        'lat': 49.18, 'lon': 19.09,
        'vyska': '1 709 m n. m.',
        'rozloha': '226 km²',
        'fauna': 'Vlk, rysa uvidíš málokedy, skôr srnčiu zver.',
        'flora': 'Horec, prvosienka. TRHAŤ: Medvedí cesnak (pozor na zóny!).',
        'jedovate': 'Ľuľkovec zlomocný.',
        'trasy_psy': 'Štefanová -> Podžiar (pohodová cesta).',
        'trasy_bez': 'Diery (rebríky), Malý Rozsutec.',
        'body_zaujmu': 'Veľký Rozsutec, Vrátna dolina.'
    }, # Tu musela byť čiarka
    'poloniny': {
        'nazov': 'Národný park Poloniny',
        'lat': 49.03, 'lon': 22.40,
        'vyska': '1 208 m n. m.',
        'rozloha': '298 km²',
        'fauna': 'Zubor hrivnatý (jediné miesto v SR), vlk dravý, medveď.',
        'flora': 'Pôvodné bukové pralesy (UNESCO). TRHAŤ: Huby (mimo rezervácií).',
        'jedovate': 'Vranie oko štvorlisté, prilbica.',
        'trasy_psy': 'Povolené na vyznačených chodníkoch s vôdzkou a náhubkom.',
        'trasy_bez': 'Prísne rezervácie (Stužica) – držte sa striktne chodníka.',
        'body_zaujmu': 'Kremenec (trojmedzie), Drevené kostolíky v okolí.'
    }
}
@príroda.route('/')
def domov():
    return render_template('príroda.html')

@príroda.route('/get_info')
def get_info():
    kod = request.args.get('miesto')
    lokalita = MIESTA.get(kod)
    if not lokalita: return jsonify({'error': 'Nenájdené'}), 404
    
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lokalita['lat']}&longitude={lokalita['lon']}&current_weather=true"
        data = requests.get(url).json()
        teplota = data['current_weather']['temperature']
        vietor = data['current_weather']['windspeed']
        
        # Logika pre bezpečnosť
        tip = "Podmienky sú ideálne na túru."
        if vietor > 30: tip = "⚠️ Pozor! Na hrebeňoch je silný vietor. Zvážte túru v lese."
        if teplota < 0: tip = "❄️ Pozor! Chodníky môžu byť namrznuté. Vezmite si mačky."
        if teplota > 30: tip = "☀️ Horúčava! Nezabudnite na dostatok vody a pokrývku hlavy."
        
        vysledok = {**lokalita, 'temp': teplota, 'wind': vietor, 'tip': tip}
    except:
        vysledok = {**lokalita, 'temp': "N/A", 'wind': "N/A", 'tip': "Dáta o počasí nedostupné."}
        
    return jsonify(vysledok)

if __name__ == '__main__':
    príroda.run(debug=True)