from address_routes.einstein_units import hospitalar_units_lat_lon as rts

def load_deliveries_info(city: str) -> dict[int, dict[str, float]]:
    cityroutes = rts[city]

    if city == "SP":
        d1 = cityroutes['Einstein Morumbi']
        d2 = cityroutes['Einstein Alphaville']
        d3 = cityroutes['Einstein Alto de Pinheiros']
        d4 = cityroutes['Einstein Anália Franco']
        d5 = cityroutes['Einstein Chácara Klabin']
        d6 = cityroutes['Einstein Ibirapuera']
        d7 = cityroutes['Einstein Jardins']
        d8 = cityroutes['Einstein Parque da Cidade']
        d9 = cityroutes['Einstein Parque Ibirapuera']
        d10 = cityroutes['Einstein Perdizes']
        d11 = cityroutes['Einstein Vila Mariana']
        d12 = cityroutes['Centro de Terapias Avançadas em Oncologia e Hematologia Einstein']
        d13 = cityroutes['Espaço Einstein Bem-Estar e Saúde Mental']
        d14 = cityroutes['Espaço Einstein Esporte e Reabilitação']
        d15 = cityroutes["Einstein Alphaville"]
        d16 = cityroutes["Einstein Perdizes"]
        d17 = cityroutes["Einstein Chácara Klabin"]
        d18 = cityroutes['Einstein Jardins']
        d19 = cityroutes['Einstein Alto de Pinheiros']
        d20 = cityroutes['Einstein Morumbi']
        d21 = cityroutes['Espaço Einstein Bem-Estar e Saúde Mental']
        d22 = cityroutes['Einstein Ibirapuera']
        d23 = cityroutes['Einstein Alphaville']
        d24 = cityroutes['Einstein Morumbi']
        d25 = cityroutes['Einstein Alto de Pinheiros']

        return {
            1: {"lat": d1[0], "lon": d1[1], "demand": 8,  "priority": 3},
            2: {"lat": d2[0], "lon": d2[1], "demand": 12, "priority": 2},
            3: {"lat": d3[0], "lon": d3[1], "demand": 15, "priority": 1},
            4: {"lat": d4[0], "lon": d4[1], "demand": 10, "priority": 3},
            5: {"lat": d5[0], "lon": d5[1], "demand": 6,  "priority": 2},
            6: {"lat": d6[0], "lon": d6[1], "demand": 8,  "priority": 3},
            7: {"lat": d7[0], "lon": d7[1], "demand": 12, "priority": 2},
            8: {"lat": d8[0], "lon": d8[1], "demand": 15, "priority": 1},
            9: {"lat": d9[0], "lon": d9[1], "demand": 10, "priority": 3},
            10: {"lat": d10[0], "lon": d10[1], "demand": 6,  "priority": 2},
            11: {"lat": d11[0], "lon": d11[1], "demand": 6,  "priority": 2},
            12: {"lat": d12[0], "lon": d12[1], "demand": 6,  "priority": 2},
            13: {"lat": d13[0], "lon": d13[1], "demand": 6,  "priority": 2},
            14: {"lat": d14[0], "lon": d14[1], "demand": 6,  "priority": 2},
            15: {"lat": d15[0], "lon": d15[1], "demand": 8,  "priority": 3},
            16: {"lat": d16[0], "lon": d16[1], "demand": 12, "priority": 2},
            17: {"lat": d17[0], "lon": d17[1], "demand": 15, "priority": 1},
            18: {"lat": d18[0], "lon": d18[1], "demand": 10, "priority": 3},
            19: {"lat": d19[0], "lon": d19[1], "demand": 6,  "priority": 2},
            20: {"lat": d20[0], "lon": d20[1], "demand": 8,  "priority": 3},
            21: {"lat": d21[0], "lon": d21[1], "demand": 12, "priority": 2},
            22: {"lat": d22[0], "lon": d22[1], "demand": 15, "priority": 1},
            23: {"lat": d23[0], "lon": d23[1], "demand": 10, "priority": 3},
            24: {"lat": d24[0], "lon": d24[1], "demand": 6,  "priority": 2},
            25: {"lat": d25[0], "lon": d25[1], "demand": 6,  "priority": 2}
        }
    else:
        raise ValueError(f"City '{city}' without definied deliveries routes.")
        
