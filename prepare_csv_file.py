"""
Module providing an produced file to be integrated.
"""

import csv
import datetime
from decimal import Decimal
import re
import unicodedata
import math

handyFile = 'HandyLibrary.csv'
shopifyFile = 'handy_result.csv'
count = 0
comma = ','
blank = ' '
semicolon = ';'
# Letters for comment field
E = T = P = ''
bonneEtat = 'Bon état'
imparfait = 'Imparfait'
neuf = 'Neuf'
commeNeuf = 'Comme neuf'
tresBonEtat = 'Très bon état'

def manage_author(author):
    author = author.split(comma)
    author.reverse()
    author = blank.join(author)
    return author.strip()


def vendor_field(author):
    author = author.split(semicolon)
    result = ''
    i = 0
    for current in author:
        if i > 0:
            result += comma + blank
        result += manage_author(current)
        i += 1
    return result


def apply_discount(price, condition):
    if (condition == neuf):
        return price
    elif (condition == imparfait):
        return price * 0.4
    elif (condition == bonneEtat):
        return price * 0.6
    elif (condition == tresBonEtat):
        return price * 0.7
    return price * 0.8


def calculate_price(price, condition):
    discount = float("{:.2f}".format(apply_discount(float(price), condition)))
    amount = int(math.ceil(float(100 * discount) / 5)) * 5 / Decimal(100)
    return "{:.2f}".format(Decimal(amount))

def extract_from_comment_field(comment):
    global E, T, P
    search_e = re.search('E (.+?)\n', comment)
    if search_e:
        E = search_e.group(1).strip()
        if (E == 'N' or E == 'Neuf'):
            E = neuf
        elif (E == 'C' or E == 'Comme neuf'):
            E = commeNeuf
        elif (E == 'B' or E == 'Bon état'):
            E = bonneEtat
        elif (E == 'I' or E == 'Imparfait'):
            E = imparfait
        elif (E == 'T' or E == 'Très bon état'):
            E = tresBonEtat
        else:
            raise ValueError(
                "E which is Etat du livre should be a value between [N,C,B,I,T] and not '"+E+"'")
    search_t = re.search('T (.+?)\n', comment)
    if search_t:
        T = search_t.group(1).strip()
    search_p = re.search('P (\d+)$', comment)
    if search_p:
        P = search_p.group(1).strip()


def format_date_parution(date2format: str) -> str:
    if date2format and (len(date2format) > 3):
        date_time_obj = datetime.datetime.strptime(date2format[0:4], '%Y')
        date2format = date_time_obj.year
        if date2format < 1900 or date2format > 2100:
            print("Error in Date de parution, date not added : " + str(date2format))
            return ""
    return str(date2format)


def clean_list(s: str, isbn) -> str:
    return "".join([x for x in s if x.isalnum() or x.isspace() or x == '-']).strip().lower().replace('   ', '-').replace('  ', '-').replace(' ', '-') + "-" + isbn


def check_if_empty(tag: str) -> str:
    if tag.split():
        return tag + ", "
    return ""


def convert_age_to_tag_label(age):
    if age in ["0", "1", "2"]:
        return "Tout petit"
    elif age in ["3", "4", "5"]:
        return "A partir de 3 ans"
    elif age in ["6", "7", "8"]:
        return "A partir de 6 ans"
    elif age in ["9", "10", "11"]:
        return "A partir de 9 ans"
    elif age in ["12", "13", "14"]:
        return "A partir de 12 ans"
    elif age in ["15", "16", "17"]:
        return "Jeunes adultes"
    return "Adulte"

def age_spelling(age):
    return age + " an" if (age == '0' or age == '1') else age + " ans"

###### BODY HTML ######
body = "<p style=\"text-align: left;\"><span style=\"font-weight: 400;\"><meta charset=\"utf-8\"> <em>A partir de {}</em></span></p><p style=\"text-align: left;\"><span style=\"font-weight: 400;\">{}</span></p><p><span><em><meta charset=\"utf-8\">État : {}, <a href=\"https://williamcrocodile.com/pages/etat-des-livres\" target=\"_blank\" title=\"État des livres\" rel=\"noopener noreferrer\">en savoir plus</a></em></span></p><p><span><em><meta charset=\"UTF-8\">{}{}{} pages</em></span></p><p><span><em><meta charset=\"UTF-8\">{}{}{}ISBN : {}</em></span></p><p><span><em>Langue : {}</em></span></p>"

###### Write ######
with open(handyFile, 'r', encoding='utf-8') as handCSV:
    csv_reader = csv.reader(handCSV, delimiter=comma)
    with open(shopifyFile, mode='w', newline='', encoding='utf-8') as shopify_file:
        generated_csv = csv.writer(
            shopify_file, delimiter=comma, quoting=csv.QUOTE_MINIMAL)
        generated_csv.writerow(['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value', 'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty', 'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Position', 'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description',
                                'Google Shopping / Google Product Category', 'Google Shopping / Gender', 'Google Shopping / Age Group', 'Google Shopping / MPN', 'Google Shopping / AdWords Grouping', 'Google Shopping / AdWords Labels', 'Google Shopping / Condition', 'Google Shopping / Custom Product', 'Google Shopping / Custom Label 0', 'Google Shopping / Custom Label 1', 'Google Shopping / Custom Label 2', 'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4', 'Variant Image', 'Variant Weight Unit', 'Variant Tax Code', 'Cost per item', 'Status'])
        for row in csv_reader:
            if count == 0:
                count += 1
            else:
                count += 1
                # Commentaires
                extract_from_comment_field(row[26])

                # Date de parution format YYYY
                row[3] = format_date_parution(row[3])

                # Tags
                tmpTags = []
                tmpTags.append(row[2])
                tmpTags.append(E)
                tmpTags.append(T)
                tmpTags.append(row[3])
                tmpTags.append(row[4])
                tmpTags.append(row[6])
                tmpTags.append(convert_age_to_tag_label(row[7]))
                tmpTags.append(row[8])
                tmpTags.append(row[18])

                # File
                tmpRow = []
                tmpRow.append(unicodedata.normalize('NFKD', clean_list(
                    row[0], row[9])).encode('ascii', 'ignore').decode('utf8'))  # 0
                tmpRow.append(row[0])  # 1
                # 2 Template dans equivalence fichier ligne 3
                tmpRow.append(body.format(
                    age_spelling(row[7]), row[15], E, check_if_empty(T), check_if_empty(row[4].replace('roché', 'roché, couverture souple')), row[5], check_if_empty(row[2]), check_if_empty(row[6]), check_if_empty(row[3]), row[9], row[8]))
                tmpRow.append(vendor_field(row[1]))  # 3
                tmpRow.append(T)  # 4
                tmpRow.append(comma.join(tmpTags))  # 5
                tmpRow.append('TRUE')  # 6
                tmpRow.append('Title')  # 7
                tmpRow.append('Default Title')  # 8
                tmpRow.append('')  # 9
                tmpRow.append('')  # 10
                tmpRow.append('')  # 11
                tmpRow.append('')  # 12
                tmpRow.append(row[28])  # 13
                tmpRow.append(P)  # 14
                tmpRow.append('shopify')  # 15
                tmpRow.append('1')  # 16
                tmpRow.append('deny')  # 17
                tmpRow.append('manual')  # 18
                if row[17] == '':
                    row[17] = 0
                tmpRow.append(calculate_price(row[17], E))  # 19
                tmpRow.append(row[17])  # 20
                tmpRow.append('TRUE')  # 21
                tmpRow.append('FALSE')  # 22
                tmpRow.append(row[9])  # 23
                tmpRow.append('')  # 24
                tmpRow.append('')  # 25
                tmpRow.append('')  # 26
                tmpRow.append('FALSE')  # 27
                tmpRow.append('')  # 28
                tmpRow.append('')  # 29
                tmpRow.append('')  # 30
                tmpRow.append('')  # 31
                tmpRow.append('')  # 32
                tmpRow.append('')  # 33
                tmpRow.append('')  # 34
                tmpRow.append('')  # 35
                tmpRow.append('')  # 36
                tmpRow.append('')  # 37
                tmpRow.append('')  # 38
                tmpRow.append('')  # 39
                tmpRow.append('')  # 40
                tmpRow.append('')  # 41
                tmpRow.append('')  # 42
                tmpRow.append('')  # 43
                tmpRow.append('g')  # 44
                tmpRow.append('')  # 45
                tmpRow.append('')  # 46
                tmpRow.append('draft')  # 47
                generated_csv.writerow(tmpRow)

###### Check write ######
check_write_count = 0
with open(shopifyFile, encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        check_write_count += 1

if (check_write_count != count):
    print("Error : Input ({}) and output ({}) file dont have same line numbers".format(
        check_write_count, count))
