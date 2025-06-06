motos = {
        1: {
            'nombre': 'KTM Adventure 390',
            'marca': 'KTM',
            'tipo': 'Aventura',
            'precio_dia': 80,
            'descripcion': 'Versátil moto de aventura ligera.',
            'descripcion_larga':
                'La KTM Adventure 390 es perfecta para los aventureros urbanos y off-road. Compacta, ágil y potente, con suspensión de largo recorrido.',
            'imagen': 'Ktm__Adventure_390.png',
            'caracteristicas': [
                '373cc',
                '44HP',
                '158kg',
                '200mm',
                '167km/h',
                'Manual'
            ],
            'stock': 7
        },
        2: {
            'nombre': 'Honda Dream 110',
            'marca': 'Honda',
            'tipo': 'Ciudad',
            'precio_dia': 30,
            'descripcion': 'Eficiente moto urbana para el día a día.',
            'descripcion_larga':
                'La Honda Dream 110 es confiable y económica. Ideal para desplazamientos diarios con bajo consumo de combustible.',
            'imagen': 'Honda__Dream_110.png',
            'caracteristicas': [
                '110cc',
                '8.6HP',
                '112kg',
                'Convencional',
                '90km/h',
                'Manual'
            ],
            'stock': 10
        },
        3: {
            'nombre': 'Suzuki VStrom 800 DE',
            'marca': 'Suzuki',
            'tipo': 'Adventure Touring',
            'precio_hora': 5,
            'precio_dia': 120,
            'descripcion': 'Moto trail potente y robusta.',
            'descripcion_larga':
                'La VStrom 800 DE combina comodidad y capacidad off-road con tecnología avanzada y excelente manejo en largos recorridos.',
            'imagen': 'Suzuki__Vstrom_800_DE_2024.png',
            'caracteristicas': [
                '776cc',
                '83HP',
                '230kg',
                '220mm',
                '191km/h',
                'Manual'
            ],
            'stock': 4
        },
        4: {
            'nombre': 'Yamaha N-Max 155',
            'marca': 'Yamaha',
            'tipo': 'Scooter',
            'precio_hora': 2.00,
            'precio_dia': 50,
            'descripcion': 'Scooter urbano con estilo moderno.',
            'descripcion_larga':
                'El Yamaha N-Max 155 ofrece un balance entre agilidad y confort, ideal para la ciudad con sistema de frenos ABS y diseño atractivo.',
            'imagen': 'Yamaha__NMAX_155_2020.png',
            'caracteristicas': [
                '155cc',
                '15HP',
                '127kg',
                'Convencional',
                '125km/h',
                'Automático'
            ],
            'stock': 6
        },
        5: {
            'nombre': 'BMW R1200GS',
            'marca': 'BMW',
            'tipo': 'Adventure',
            'precio_hora': 6.66,
            'precio_dia': 160,
            'descripcion': 'Referente mundial en motos de aventura.',
            'descripcion_larga': 'La BMW R1200GS es sinónimo de aventura sin límites. Motor potente, gran autonomía y electrónica avanzada para cualquier terreno.',
            'imagen': 'BMW__R1200GS.png',
            'caracteristicas': [
                '1170cc',
                '125HP',
                '244kg',
                '185mm',
                '210km/h',
                'Manual'
            ],
            'stock': 3
        },
        6: {
            'nombre': 'Suzuki V-Strom 650',
            'marca': 'Suzuki',
            'tipo': 'Touring',
            'precio_hora': 18.33,
            'precio_dia': 110,
            'descripcion': 'Trail versátil ideal para largos viajes.',
            'descripcion_larga': 'La Suzuki V-Strom 650 destaca por su fiabilidad y confort, perfecta para viajes largos en carretera o caminos mixtos.',
            'imagen': 'Suzuki__V-strom_650.png',
            'caracteristicas': [
                '645cc',
                '69HP',
                '213kg',
                '170mm',
                '185km/h',
                'Manual'
            ],
            'stock': 5
        },
        7: {
            'nombre': 'Ducati Diavel 1260',
            'marca': 'Ducati',
            'tipo': 'Naked/Crucero',
            'precio_hora': 7.50,
            'precio_dia': 180,
            'descripcion': 'Cruiser deportiva con alma Ducati.',
            'descripcion_larga': 'La Diavel 1260 combina potencia extrema con ergonomía cruiser. Diseño agresivo y confort para viajes rápidos.',
            'imagen': 'ducati__diavel.png',
            'caracteristicas': [
                '1262cc',
                '157HP',
                '218kg',
                '120mm',
                '270km/h',
                'Manual'
            ],
            'stock': 2
        },
        8: {
            'nombre': 'Ducati Monster 937 SP',
            'marca': 'Ducati',
            'tipo': 'Naked',
            'precio_hora': 7.0,
            'precio_dia': 170,
            'descripcion': 'La icónica Monster renovada.',
            'descripcion_larga': 'Con un diseño ligero y agresivo, la Monster 937 SP ofrece una experiencia deportiva pura con electrónica de última generación.',
            'imagen': 'Ducati__Monster_937_SP.png',
            'caracteristicas': [
                '937cc',
                '111HP',
                '186kg',
                '202mm',
                '226km/h',
                'Manual'
            ],
            'stock': 8
        },
        9: {
            'nombre': 'Ducati Streetfighter V4',
            'marca': 'Ducati',
            'tipo': 'Street/Naked',
            'precio_hora': 9.16,
            'precio_dia': 220,
            'descripcion': 'Potencia y agresividad sin carenado.',
            'descripcion_larga': 'La Streetfighter V4 es una bestia en la carretera. Tecnología de MotoGP, control total y una estética feroz.',
            'imagen': 'Ducati__Streetfighter_V4.png',
            'caracteristicas': [
                '1103cc',
                '208HP',
                '178kg',
                '120mm',
                '299km/h',
                'Manual'
            ],
            'stock': 1
        }
    }

def obtener_motos():
    global motos
    return motos

def obtener_moto_por_id(moto_id):
    global motos
    return motos.get(moto_id)

def actualizar_stock(moto_id, cantidad):
    global motos
    if moto_id in motos:
        motos[moto_id]['stock'] = max(0, motos[moto_id].get('stock', 0) + cantidad)
        return True
    return False
