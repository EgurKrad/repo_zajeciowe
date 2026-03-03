# zaokrąglam do pełnych groszy
def zaokraglij(cena):
    return round(float(cena), 2)


def oblicz_koszyk(produkty, klient, promocje):

    koszyk = []
    for p in produkty:
        koszyk.append({
            'sku': p['sku'],
            'nazwa': p['nazwa'],
            'kategoria': p['kategoria'],
            'cena_pocz': zaokraglij(p['cena']),
            'cena': zaokraglij(p['cena']),
            'ilosc': p['ilosc'],
            'rabaty': []
        })

    # promocje
    uzyto_2plus1 = False

    # 1. 2+1 gratis
    for promo in promocje:
        if promo['typ'] == '2+1' and promo.get('sku'):
            for item in koszyk:
                if item['sku'] == promo['sku'] and item['ilosc'] >= 3:
                    gratis = item['ilosc'] // 3
                    platne = item['ilosc'] - gratis
                    item['cena'] = zaokraglij(item['cena_pocz'] * platne / item['ilosc'])
                    item['rabaty'].append(promo['nazwa'])
                    uzyto_2plus1 = True

    # 2. Najtańszy -50% w kategorii
    for promo in promocje:
        if promo['typ'] == 'najtanszy-50' and promo.get('kategoria'):
            kat = promo['kategoria']
            w_kategorii = [i for i in koszyk if i['kategoria'] == kat]
            if w_kategorii:
                najtanszy = min(w_kategorii, key=lambda x: x['cena'])
                nowa_cena = zaokraglij(najtanszy['cena'] * 0.5)
                if nowa_cena < 1:
                    nowa_cena = 1.0
                najtanszy['cena'] = nowa_cena
                najtanszy['rabaty'].append(promo['nazwa'])

    # 3. Procent na kategorię
    for promo in promocje:
        if promo['typ'] == 'procent-kategoria' and promo.get('kategoria'):
            kat = promo['kategoria']
            procent = promo.get('procent', 0) / 100
            for item in koszyk:
                if item['kategoria'] == kat and kat != 'outlet': # nie dla outletów
                    nowa = zaokraglij(item['cena'] * (1 - procent))
                    if nowa < 1:
                        nowa = 1.0
                    item['cena'] = nowa
                    item['rabaty'].append(promo['nazwa'])

    # 4. Kupon
    kupon_rabat = 0.0
    if not uzyto_2plus1: # tylko jeśli nie było 2+1
        for promo in promocje:
            if promo['typ'] == 'kupon' and promo.get('kwota'):
                min_wartosc = promo.get('min_wartosc', 0)
                wartosc_koszyka = sum(item['cena'] * item['ilosc'] for item in koszyk)
                if wartosc_koszyka >= min_wartosc:
                    kupon_rabat = promo['kwota']
                    break

    # 5. Dostawa
    wartosc_po_rabatach = sum(item['cena'] * item['ilosc'] for item in koszyk)
    dostawa = 15.0

    for promo in promocje:
        if promo['typ'] == 'darmowa-dostawa' and promo.get('od'):
            if wartosc_po_rabatach - kupon_rabat >= promo['od']:
                dostawa = 0.0
                break

    if klient.get('lojalnosc') in ['gold', 'premium']:
        dostawa = 0.0

    # obliczenie ceny
    wartosc_po_kuponie = max(0.0, wartosc_po_rabatach - kupon_rabat)
    suma_brutto = zaokraglij(wartosc_po_kuponie + dostawa)

    wartosc_poczatkowa = sum(item['cena_pocz'] * item['ilosc'] for item in koszyk)
    oszczednosc = zaokraglij(
        wartosc_poczatkowa - wartosc_po_kuponie + (15.0 - dostawa)
    )

    # paragon
    print("\n" + "="*60)
    print("PARAGON FISKALNY")
    print(f"Klient: {klient['id']}   Lojalność: {klient.get('lojalnosc','regular')}")
    print("="*60)

    for item in koszyk:
        rabat_linii = zaokraglij((item['cena_pocz'] - item['cena']) * item['ilosc'])
        print(f"{item['nazwa']} ({item['sku']})  x{item['ilosc']}")
        print(f"   przed: {item['cena_pocz']:.2f} → po: {item['cena']:.2f} zł")
        if rabat_linii > 0:
            print(f"   rabat: {rabat_linii:.2f} zł")
        print("-" * 40)

    print(f"{'-'*60}")
    print(f"Koszt dostawy:          {dostawa:8.2f} zł")
    print(f"RAZEM DO ZAPŁATY:      {suma_brutto:8.2f} zł")
    print(f"Oszczędności:           {oszczednosc:8.2f} zł")
    print("="*60)
    print("Dziękujemy za zakupy!\n")

    return suma_brutto

if __name__ == "__main__":
    koszyk = [
        {'sku': 'OD-NAVY-M', 'nazwa': 'Ocean Dynamics granat M', 'kategoria': 'tshirts',
         'cena': 99.99, 'ilosc': 3},
        {'sku': 'BOOK-SF01', 'nazwa': 'Dune', 'kategoria': 'science-fiction',
         'cena': 59.99, 'ilosc': 1},
    ]

    klient = {'id': 'K12345', 'lojalnosc': 'silver'}

    promocje = [
        {'typ': '2+1', 'nazwa': '2+1 gratis', 'sku': 'OD-NAVY-M'},
        {'typ': 'procent-kategoria', 'nazwa': '-15% Sci-Fi', 'kategoria': 'science-fiction', 'procent': 15},
        {'typ': 'kupon', 'nazwa': 'Kupon-20', 'kwota': 20, 'min_wartosc': 100},
        {'typ': 'darmowa-dostawa', 'nazwa': 'Darmowa od 200', 'od': 200},
        {'typ': 'najtanszy-50', 'nazwa': 'Najtańszy -50% outlet', 'kategoria': 'outlet'},
    ]

    oblicz_koszyk(koszyk, klient, promocje)

