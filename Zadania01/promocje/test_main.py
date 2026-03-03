import unittest
from main import *

class TestKoszyk(unittest.TestCase):

    def setUp(self):
        self.klient = {'id': 'K1', 'lojalnosc': 'silver'}

    def test_bez_promocji(self):
        produkty = [
            {'sku': 'A1', 'nazwa': 'Produkt A', 'kategoria': 'inne',
             'cena': 100.0, 'ilosc': 1}
        ]

        promocje = []

        suma = oblicz_koszyk(produkty, self.klient, promocje)

        # 100 + 15 dostawa = 115
        self.assertEqual(suma, 115.0)

    def test_2plus1(self):
        produkty = [
            {'sku': 'A1', 'nazwa': 'Produkt A', 'kategoria': 'inne',
             'cena': 90.0, 'ilosc': 3}
        ]

        promocje = [
            {'typ': '2+1', 'nazwa': '2+1', 'sku': 'A1'}
        ]

        suma = oblicz_koszyk(produkty, self.klient, promocje)

        # 3 sztuki po 90 → płacimy za 2 → 180 + 15 dostawa
        self.assertEqual(suma, 195.0)

    def test_kupon(self):
        produkty = [
            {'sku': 'A1', 'nazwa': 'Produkt A', 'kategoria': 'inne',
             'cena': 200.0, 'ilosc': 1}
        ]

        promocje = [
            {'typ': 'kupon', 'nazwa': 'Kupon20', 'kwota': 20, 'min_wartosc': 100}
        ]

        suma = oblicz_koszyk(produkty, self.klient, promocje)

        # 200 - 20 + 15 dostawa
        self.assertEqual(suma, 195.0)

    def test_darmowa_dostawa_lojalnosc(self):
        klient = {'id': 'K1', 'lojalnosc': 'gold'}

        produkty = [
            {'sku': 'A1', 'nazwa': 'Produkt A', 'kategoria': 'inne',
             'cena': 50.0, 'ilosc': 1}
        ]

        suma = oblicz_koszyk(produkty, klient, [])

        # brak dostawy dla gold
        self.assertEqual(suma, 50.0)

    def test_najtanszy_50(self):
        produkty = [
            {'sku': 'O1', 'nazwa': 'Drogi', 'kategoria': 'outlet',
             'cena': 100.0, 'ilosc': 1},
            {'sku': 'O2', 'nazwa': 'Tani', 'kategoria': 'outlet',
             'cena': 60.0, 'ilosc': 1}
        ]

        promocje = [
            {'typ': 'najtanszy-50', 'nazwa': '-50%', 'kategoria': 'outlet'}
        ]

        suma = oblicz_koszyk(produkty, self.klient, promocje)

        # 60 → 30, więc 100 + 30 + 15 dostawa
        self.assertEqual(suma, 145.0)


if __name__ == "__main__":
    unittest.main()
