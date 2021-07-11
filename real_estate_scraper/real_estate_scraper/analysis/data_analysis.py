import mysql.connector
from prettytable import PrettyTable

conn = mysql.connector.connect(
    host="localhost",
    user="psz",
    password="psz2021",
    database='real_estate_db'
)


def print_query_results(query):
    t = PrettyTable()

    cursor = conn.cursor()
    cursor.execute(query)
    t.field_names = cursor.column_names
    data = cursor.fetchall()
    for d in data:
        t.add_row(d)
    print(t)


def main():
    input("Izlistati koliki je broj nekretnina za prodaju, a koliki je broj koji se iznajmljuju.")
    print("Prodaja:\n")
    query = """select count(*) from real_estate where offer_type = 'prodaja'"""
    print_query_results(query)
    print('\n')
    print("Iznajmljivanje:\n")
    query = """select count(*) from real_estate where offer_type = 'iznajmljivanje'"""
    print_query_results(query)
    print('\n')

    input("Izlistati koliko nekretnina se prodaje u svakom od gradova (izlistati sve gradove, obuhvatiti i kuce i stanove).")
    query = """select city, count(*) from real_estate where offer_type = 'prodaja' group by city"""
    print_query_results(query)
    print('\n')

    input("Izlistati koliko je uknjizenih, a koliko neuknjizenih kuca, a koliko stanova.")
    print("Uknjizene kuce:\n")
    query = """select count(*) from real_estate where estate_type = 'kuca' and registration = 'Da'"""
    print_query_results(query)
    print('\n')
    print("Neuknjizene kuce:\n")
    query = """select count(*) from real_estate where estate_type = 'kuca' and registration = 'Ne'"""
    print_query_results(query)
    print('\n')
    print("Uknjizeni stanovi:\n")
    query = """select count(*) from real_estate where estate_type = 'stan' and registration = 'Da'"""
    print_query_results(query)
    print('\n')
    print("Neuknjizeni stanovi:\n")
    query = """select count(*) from real_estate where estate_type = 'stan' and registration = 'Ne'"""
    print_query_results(query)
    print('\n')

    input("Prikazati rang listu prvih 30 najskupljih kuca koje se prodaju, i 30 najskupljih stanova koji se prodaju u Srbiji.")
    print("30 najskupljih kuca u Srbiji:\n")
    query = """select * from real_estate where estate_type = 'kuca' and offer_type = 'prodaja' order by price desc limit 0, 30"""
    print_query_results(query)
    print('\n')
    print("30 najskupljih stanova u Srbiji:\n")
    query = """select * from real_estate where estate_type = 'stan' and offer_type = 'prodaja' order by price desc limit 0, 30"""
    print_query_results(query)
    print('\n')

    input("Prikazati rang listu prvih 100 najvecih kuca i 100 najvecih stanova po povrsini (kvadraturi).")
    print("100 najvecih kuca:\n")
    query = """select * from real_estate where estate_type = 'kuca' order by size desc limit 0, 100"""
    print_query_results(query)
    print('\n')
    print("100 najvecih stanova:\n")
    query = """select * from real_estate where estate_type = 'stan' order by size desc limit 0, 100"""
    print_query_results(query)
    print('\n')

    input("Prikazati rang listu svih nekretnina izgradjenih u 2020. godini, i izlistati ih opadajuce prema ceni prodaje, odnosno ceni iznajmljivanja.")
    print("Kuce i stanovi izgradjeni u 2020. godini - prodaja:\n")
    query = """select * from real_estate where offer_type = 'prodaja' and year = 2020 order by price desc"""
    print_query_results(query)
    print('\n')
    print("Kuce i stanovi izgradjeni u 2020. godini - iznajmljivanje:\n")
    query = """select * from real_estate where offer_type = 'iznajmljivanje' and year = 2020 order by price desc"""
    print_query_results(query)
    print('\n')

    input("Prikazati nekretnine (top 30) koje imaju najveci broj soba unutar nekretnine.")
    query = """select * from real_estate order by rooms desc limit 0, 30"""
    print_query_results(query)
    print('\n')

    input("Prikazati nekretnine (top 30) koje imaju najvecu kvadraturu (samo za stanove).")
    query = """select * from real_estate where estate_type = 'stan' order by size desc limit 0,30"""
    print_query_results(query)
    print('\n')

    input("Prikazati nekretnine (top 30) koje imaju najvecu povrsinu zemljista (samo za kuce).")
    query = """select * from real_estate where estate_type = 'kuca' order by land_area desc limit 0,30"""
    print_query_results(query)
    print('\n')


if __name__ == "__main__":
    main()

