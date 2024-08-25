import re

taf_items = {
    "SH": "Pancada(s) moderada.",
    "+SH": "Pancada(s) forte.",
    "-FZ": "Congelante leve.",
    "FZ": "Congelante moderado.",
    "+FZ": "Congelante forte.",
    "-DZ": "Chuvisco leve.",
    "DZ": "Chuvisco moderada.",
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

def decode_taf(taf: str) -> list:
    taf_lines = taf.split()
    ret = []

    # Header and time of issue
    issue_time = taf_lines[0]
    ret.append((issue_time, f"Disponibilizado em {issue_time[2:4]}:{issue_time[4:6]}Z no dia {issue_time[0:2]}"))

    # Validity period
    valid_period = taf_lines[1]
    start_day = int(valid_period[:2])
    start_hour = int(valid_period[2:4])
    end_day = int(valid_period[5:7])
    end_hour = int(valid_period[7:9])
    ret.append((valid_period, f"Válido do dia {start_day} as {start_hour}:00Z até dia {end_day} as {end_hour}:00Z"))

    context = ""

    for item in taf_lines[2:]:
        if item in ["BECMG", "TEMPO"]:
            context = item
        elif re.match(r"^\d{4}/\d{4}$", item):
            from_time, to_time = item.split('/')
            if context == "BECMG":
                ret.append((f"{context} {item}", f"Condições previstas do dia {from_time[:2]} as {from_time[2:4]}:00(UTC) até dia {to_time[:2]} as {to_time[2:4]}:00(UTC)"))
                context = ""
            elif context == "TEMPO":
                ret.append((f"{context} {item}", f"Condições temporárias previstas do dia {from_time[:2]} as {from_time[2:4]}:00(UTC) até dia {to_time[:2]} as {to_time[2:4]}:00(UTC)"))
                context = ""
            else:
                ret.append((item, f"Do dia {from_time[:2]} as {from_time[2:4]}:00(UTC) até dia {to_time[:2]} as {to_time[2:4]}:00(UTC)"))

        elif (wind := re.findall("(\d{3})(\d{2})KT", item)) != []:
            [(direction, speed)] = wind
            ret.append((item, f"Vento proa <b>{direction}</b>° com velocidade <b>{speed}</b> nós (kt)."))

        elif (wind := re.findall("VRB(\d{2})KT", item)) != []:
            [speed] = wind
            ret.append((item, f"Vento com direção <b>variável</b> e velocidade {speed} nós (kt)."))

        elif (wind := re.findall("(\d{3})(\d+)G(\d+)KT", item)) != []:
            [(direction, speed, gust)] = wind
            ret.append((item, f"Vento proa {direction}° com velocidade {speed} nós (kt) e <b>rajadas</b> de {gust} nós."))

        elif item == "CAVOK":
            ret.append((item, "Ceiling and Visibility OK. Sem nuvens e visibilidade OK."))

        elif re.match(r"^\d{4}$", item):
            visibility = int(item)
            ret.append((item, f"Visibilidade {visibility} metros"))

        elif item in taf_items:
            ret.append((item, taf_items[item]))

        elif re.match(r"^\d{4}/\d{4}$", item):
            from_time, to_time = item.split('/')
            ret.append((item, f"Do dia {from_time[0:2]} as {from_time[2:4]}:00(UTC) até dia {from_time[0:2]} as {to_time[2:4]}:00(UTC)"))

        elif re.match(r"^PROB\d{2}$", item):
            probability = item[4:]
            ret.append((item, f"Probabilidade de {probability}% de ocorrer estas condições"))

        elif re.match(r"^NSW$", item):
            ret.append((item, "Sem fenômenos significativos"))

        elif re.match(r"^VV\d{3}$", item):
            vertical_visibility = int(item[2:]) * 100
            ret.append((item, f"Visibilidade vertical {vertical_visibility} pés"))

        elif re.match(r"^TN\d{2}/\d{4}Z$", item):
            temperature = item[2:4]
            day = item[5:7]
            hour = item[7:9]
            ret.append((item, f"A temperatura mínima é de {temperature}°C prevista de ocorrer dia {day} as {hour}"))

        elif re.match(r"^TX\d{2}/\d{4}Z$", item):
            temperature = item[2:4]
            day = item[5:7]
            hour = item[7:9]
            ret.append((item, f"A temperatura máxima é de {temperature}°C prevista de ocorrer dia {day} as {hour}"))

        elif (cloud := re.findall("([A-Z]{3})(\d{3})(CB|TCU)*", item)) != []:
            [(cloud_type, cloud_altitude, formation)] = cloud
            cloud_altitude = int(cloud_altitude) * 100

            if cloud_type == "OVC": cloud_type = "Totalmente encoberto"
            elif cloud_type == "BKN": cloud_type = "Nuvens broken (5/8 a 7/8 do céu com nuvens)"
            elif cloud_type == "SCT": cloud_type = "Nuvens espalhadas (3/8 a 4/8 do céu com nuvens)"
            elif cloud_type == "FEW": cloud_type = "Poucas nuvens (1/8 a 2/8 do céu com nuvens)"

            extra = ""
            if formation == "CB":
                extra = "<b>Atenção:</b> nuvens de tempestade."
            elif formation == "TCU":
                extra = "<b>Atenção:</b> nuvens de grande extensão vertical."


            ret.append((item, f"{cloud_type} em <b>{cloud_altitude}</b> pés de altitude. {extra}"))

        else:
            ret.append((item, "Item desconhecido"))

    grouped_taf = []
    group = []
    grouped_started = False
    for (item, meaning) in ret:
        if item.startswith("BECMG ") or item.startswith("TEMPO "):
            grouped_started = True
            if group != []:
                grouped_taf.append(group)    
                group = []
            group.append((item, meaning))
        else:
            if grouped_started:
                group.append((item, meaning))
            else:
                grouped_taf.append((item, meaning))
    if group != []:
        grouped_taf.append(group)

    return grouped_taf

if __name__ == "__main__":
    taf = """112008Z 1200/1224 19006KT 9999 SCT025 TN21/1209Z TX27/1215Z
  TEMPO 1207/1212 4000 RA BR BKN010 OVC040
  BECMG 1213/1215 10010KT RMK PGX
"""
    decoded_taf = decode_taf(taf)
    print(decoded_taf)