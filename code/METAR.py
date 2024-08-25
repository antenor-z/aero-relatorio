import re
from datetime import datetime, timedelta

# Fonte: https://ajuda.decea.mil.br/base-de-conhecimento/como-decodificar-o-metar-e-o-speci/

other_items = {
    "SH": "Pancada(s) moderada.",
    "+SH": "Pancada(s) forte.",
    "-FZ": "Congelante leve.",
    "FZ": "Congelante moderado.",
    "+FZ": "Congelante forte.",
    "-DZ": "Chuvisco leve.",
    "DZ": "Chuvisco moderado.",
    "+DZ": "Chuvisco forte.",
    "-RA": "Chuva leve.",
    "RA": "Chuva moderada.",
    "+RA": "Chuva forte.",
    "-SN": "Neve leve.",
    "SN": "Neve moderada.",
    "+SN": "Neve forte.",
    "-SG": "Grãos de neve leve.",
    "SG": "Grãos de neve moderado.",
    "+SG": "Grãos de neve forte.",
    "-PL": "Pelotas de gelo leve.",
    "PL": "Pelotas de gelo moderado.",
    "+PL": "Pelotas de gelo forte.",
    "-GR": "Granizo leve.",
    "GR": "Granizo moderado.",
    "+GR": "Granizo forte.",
    "-GS": "Granizo pequeno e/ou grãos de neve leve.",
    "GS": "Granizo pequeno e/ou grãos de neve moderado.",
    "+GS": "Granizo pequeno e/ou grãos de neve forte.",
    "-BR": "Névoa úmida leve.",
    "BR": "Névoa úmida moderada.",
    "+BR": "Névoa úmida densa.",
    "-FG": "Nevoeiro leve.",
    "FG": "Nevoeiro moderado.",
    "+FG": "Nevoeiro denso.",
    "-FU": "Fumaça leve.",
    "FU": "Fumaça moderada.",
    "+FU": "Fumaça densa.",
    "-VA": "Cinzas vulcânicas leve.",
    "VA": "Cinzas vulcânicas moderada.",
    "+VA": "Cinzas vulcânicas densa.",
    "-DU": "Poeira extensa leve.",
    "DU": "Poeira extensa moderada.",
    "+DU": "Poeira extensa densa.",
    "-SA": "Areia leve.",
    "SA": "Areia moderada.",
    "+SA": "Areia densa.",
    "-HZ": "Névoa seca leve.",
    "HZ": "Névoa seca moderada.",
    "+HZ": "Névoa seca densa.",
    "-PO": "Poeira/areia em redemoinhos leve.",
    "PO": "Poeira/areia em redemoinhos moderada.",
    "+PO": "Poeira/areia em redemoinhos densa.",
    "-SQ": "Tempestade leve.",
    "SQ": "Tempestade moderada.",
    "+SQ": "Tempestade forte.",
    "-FC": "Nuvem(ns) funil (tornado ou tromba d’água) leve.",
    "FC": "Nuvem(ns) funil (tornado ou tromba d’água) moderada.",
    "+FC": "Nuvem(ns) funil (tornado ou tromba d’água) densa.",
    "-SS": "Tempestade de areia leve.",
    "SS": "Tempestade de areia moderada.",
    "+SS": "Tempestade de areia densa.",
    "-DS": "Tempestade de poeira leve.",
    "DS": "Tempestade de poeira moderada.",
    "+DS": "Tempestade de poeira densa.",
    "-TS": "Trovoada, Raios e Relâmpagos leve.",
    "TS": "Trovoada, Raios e Relâmpagos moderada.",
    "+TS": "Trovoada, Raios e Relâmpagos densa.",
    "RERA": "Fenômenos meteorológicos recentes.",
    "WS": "Tesoura de vento (windshear)",
    "NSC": "No Significant Cloud, podem haver algumas nuvens, mas nenhuma está abaixo de 5000 pés ou dentro de 10 quilômetros.",
    "VCSH": "Chuva leve na vizinhança do aeroporto",
    "TSRA": "Trovoada com chuva.",
    "+TSRA": "Trovoada com chuva forte.",
    "VCTS": "Trovoada na vizinhança"
}

def decode_metar(metar: str) -> dict:
    #metar = "METAR SBSP 290400Z AUTO 19008KT 160V220 9999 FEW006 SCT008 BKN010 16/14 Q1025="
    #metar = "METAR SBSP 290400Z AUTO VRB08KT 160V220 9999 FEW006 SCT008 BKN010 16/14 Q1025="
    #metar = "METAR SBMN 061300Z 31015G27KT 280V350 5000 1500W -RA BKN010 SCT020 FEW025TCU 25/24 Q1014 RERA WS RWY17 W12/H75="

    try:
        metar = metar.split(" ")
        day = int(metar[0][0:2])
        hour = int(metar[0][2:4])
        minute = int(metar[0][4:6])
    except ValueError:
        return [(" ", "METAR indisponível.")]

    ret = []

    ts_utc = datetime(day=day, month=datetime.utcnow().month, year=datetime.utcnow().year, hour=hour, minute=minute)
    ts_local = ts_utc - timedelta(hours=3)
    ret.append((metar[0], f"METAR válido para dia {ts_local.day} as {ts_local.hour}:{ts_local.minute:02d} (hora de Brasília)"))

    metar = metar[1:]

    for item in metar:
        if item == "AUTO":
            ret.append((item, "Informação obtida automaticamente."))
        
        elif item == "9999":
            ret.append((item, "Visibilidade ilimitada"))
        
        elif (vis := re.findall("^(\d{4})$", item)) != [] and vis != "9999":
            [vis] = vis
            ret.append((item, f"Visibilidade {vis} metros."))
        
        elif (vis := re.findall("^(\d{4})([A-Z]+)$", item)) != []:
            [(vis, sector)] = vis
            if sector == "N": sector = "norte"
            elif sector == "S": sector = "sul"
            elif sector == "W": sector = "oeste"
            elif sector == "E": sector = "leste"
            elif sector == "NE": sector = "nordeste"
            elif sector == "NW": sector = "noroeste"
            elif sector == "SE": sector = "sudeste"
            elif sector == "SW": sector = "sudoeste"
        
            ret.append((item, f"No setor {sector} do aerodromo, visibilidade {vis}m."))
        
        elif (wind := re.findall("(\d{3})(\d{2})KT", item)) != []:
            [(direction, speed)] = wind
            ret.append((item, f"Vento proa <b>{direction}</b>° com velocidade <b>{speed}</b> nós (kt)."))
        
        elif (wind := re.findall("VRB(\d{2})KT", item)) != []:
            [speed] = wind
            ret.append((item, f"Vento com direção <b>variável</b> e velocidade {speed} nós (kt)."))
        
        elif (wind := re.findall("(\d{3})(\d+)G(\d+)KT", item)) != []:
            [(direction, speed, gust)] = wind
            ret.append((item, f"Vento proa {direction}° com velocidade {speed} nós (kt) e <b>rajadas</b> de {gust} nós."))
        
        elif (wind := re.findall("(\d{3})V(\d{3})", item)) != []:
            [(wind1, wind2)] = wind
            ret.append((item, f"Vento <b>variável</b> de proa {wind1}° até {wind2}°."))
        
        elif (cloud := re.findall("([A-Z]{3})(\d{3})(CB|TCU)*", item)) != []:
            [(cloud_type, cloud_altitude, formation)] = cloud
            cloud_altitude = int(cloud_altitude) * 100

            if cloud_type == "OVC": cloud_type = "Totalmente encoberto"
            elif cloud_type == "BKN": cloud_type = "Nuvens broken (5/8 a 7/8 do céu com nuvens)"
            elif cloud_type == "SCT": cloud_type = "Nuvens espalhadas (3/8 a 4/8 do céu com nuvens)"
            elif cloud_type == "FEW": cloud_type = "Poucas nuvens (1/8 a 2/8 do céu com nuvens)"
            
            extra = ""
            if formation == "CB":
                extra = "Atenção: nuvens de tempestade."
            elif formation == "TCU":
                extra = "Atenção: nuvens de grande extensão vertical."


            ret.append((item, f"{cloud_type} em <b>{cloud_altitude}</b> pés de altitude. {extra}"))

        elif (temp := re.findall("(\d+)/(\d+)", item)) != []:
            [(temperature, dew_point)] = temp
            ret.append((item, f"Temperatura <b>{temperature}</b>°C e ponto de orvalho <b>{dew_point}</b>°C."))
        
        elif (qnh := re.findall("Q(\d{4})", item)) != []:
            [qnh] = qnh
            ret.append((item, f"O altímetro deve ser ajustado para <b>{qnh}</b> hPa ({convert_to_inhg(qnh)} inHg)"))
        
        elif item == "CAVOK":
            ret.append((item, "Ceiling and Visibility OK. Sem nuvens e visibilidade OK."))
        
        elif (runway := re.findall("RWY(\d{2}[RLC]*)", item)) != []:
            [runway] = runway
            ret.append((item, f"Informação anterior se refere a pista {runway}"))
        
        elif item in other_items:
            ret.append((item, other_items[item]))
        
        else:
            ret.append((item, ""))

    return ret

def convert_to_inhg(hpa):
    return round(float(hpa) / 33.8639, 2)


def get_wind_info(metar: str) -> dict:
    if (wind := re.findall("(\d{3})(\d{2})KT", metar)) != []:
        [(direction, speed)] = wind
        return {"direction": int(direction), "speed": int(speed)}
    else:
        raise DecodeError("Could not find wind information.")

def parse_metar(metar_str: str) -> dict:
    wind_regex = re.compile(r'(\d{3})(\d{2})KT')
    temp_regex = re.compile(r'M?(\d{2})/(M?\d{2})')
    qnh_regex = re.compile(r'Q(\d{4})')
    vis_regex = re.compile(r'(\d{4}) ')

    wind_match = wind_regex.search(metar_str)
    temp_match = temp_regex.search(metar_str)
    qnh_match = qnh_regex.search(metar_str)
    vis_match = vis_regex.search(metar_str)

    wind_direction = int(wind_match.group(1)) if wind_match else None
    wind_speed = int(wind_match.group(2)) if wind_match else None
    visibility = int(vis_match.group(1)) if vis_match else None

    if "CAVOK" in metar_str:
        visibility = 9999

    if temp_match:
        temp_str = temp_match.group(1)
        temperature = -int(temp_str[1:]) if temp_str.startswith('M') else int(temp_str)
        dew_str = temp_match.group(2)
        dew_point = -int(dew_str[1:]) if dew_str.startswith('M') else int(dew_str)
    else:
        temperature = None

    qnh = int(qnh_match.group(1)) if qnh_match else None

    return {
        "wind_direction": wind_direction,
        "wind_speed": wind_speed,
        "temperature": temperature,
        "dew_point": dew_point,
        "qnh": qnh,
        "visibility": visibility
    }

class DecodeError(Exception):
    def __init__(self, message):
        super().__init__(message)

if __name__ == "__main__":
    metar = "METAR SBMN 061300Z 31015G27KT 280V350 5000 1500W -RA -DU BKN010 SCT020 FEW025TCU 25/24 Q1014 RERA WS RWY17 W12/H75="
    print(decode_metar(metar))
