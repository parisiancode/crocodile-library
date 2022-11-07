import csv
import datetime
import re
import unicodedata

handyFile = 'HandyLibrary.csv'
shopifyFile = 'example_result.csv'
count = 0
comma = ','
blank = ' '
semicolon = ';'
# Letters for comment field
E = T = P = ''
bonneEtat = 'Bon état'
imparfait = 'Imparfait'


def manageAuthor(author):
    author = author.split(comma)
    author.reverse()
    author = blank.join(author)
    return author.strip()


def vendorField(author):
    author = author.split(semicolon)
    result = ''
    i = 0
    for current in author:
        if i > 0:
            result += comma + blank
        result += manageAuthor(current)
        i += 1
    return result


def ourPrice(price, condition):
    if (condition == imparfait):
        return price * 0.4
    elif (condition == bonneEtat):
        return price * 0.6
    return price * 0.8


def extractFromCommentField(comment):
    global E, T, P
    searchE = re.search('E (.+?)\n', comment)
    if searchE:
        E = searchE.group(1).strip()
        if (E == 'C' or E == 'Comme neuf'):
            E = 'Comme neuf'
        elif (E == 'B' or E == 'Bon état'):
            E = 'Bon état'
        elif (E == 'I' or E == 'Imparfait'):
            E = 'Imparfait'
        else:
            raise ValueError(
                "E which is Etat du livre should be a value between [C,B,I] and not '"+E+"'")
    searchT = re.search('T (.+?)\n', comment)
    if searchT:
        T = searchT.group(1).strip()
    searchP = re.search('P (\d+)$', comment)
    if searchP:
        P = searchP.group(1).strip()


def formatDateParution(dateToFormat: str) -> str:
    if dateToFormat and (len(dateToFormat) > 3):
        date_time_obj = datetime.datetime.strptime(dateToFormat[0:4], '%Y')
        dateToFormat = date_time_obj.year
        if dateToFormat < 1900 or dateToFormat > 2100:
            print("Error in Date de parution, date not added : " + str(dateToFormat))
            return ""
    return str(dateToFormat)


def clean_list(s: str, isbn) -> str:
    return "".join([x for x in s if x.isalnum() or x.isspace() or x == '-']).strip().lower().replace('   ', '-').replace('  ', '-').replace(' ', '-') + "-" + isbn


def checkIfEmpty(tag: str) -> str:
    if tag.split():
        return tag + ", "
    return ""


def convertAgeToTagLabel(age):
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
    elif age in ["15", "16", "17", "18"]:
        return "Jeunes adultes"
    return ""


###### BODY HTML ######
body = "<p style=\"text-align: left;\"><span style=\"font-weight: 400;\"><meta charset=\"utf-8\"> <em>A partir de {} ans</em></span></p><p style=\"text-align: left;\"><span style=\"font-weight: 400;\">{}</span></p><p><span><em><meta charset=\"utf-8\">État : {}, <a href=\"https://williamcrocodile.com/pages/etat-des-livres\" target=\"_blank\" title=\"État des livres\" rel=\"noopener noreferrer\">en savoir plus</a></em></span></p><p><span><em><meta charset=\"UTF-8\">{}{}{} pages</em></span></p><p><span><em><meta charset=\"UTF-8\">{}{}{}ISBN : {}</em></span></p><p><span><em>Langue : {}</em></span></p>"

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
                extractFromCommentField(row[24])

                # Date de parution format YYYY
                row[3] = formatDateParution(row[3])

                # Tags
                tmpTags = []
                tmpTags.append(row[2])
                tmpTags.append(E)
                tmpTags.append(T)
                tmpTags.append(row[3])
                tmpTags.append(row[4])
                tmpTags.append(row[6])
                tmpTags.append(convertAgeToTagLabel(row[7]))
                tmpTags.append(row[8])
                tmpTags.append(row[18])

                # File
                tmpRow = []
                tmpRow.append(unicodedata.normalize('NFKD', clean_list(
                    row[0], row[9])).encode('ascii', 'ignore').decode('utf8'))  # 0
                tmpRow.append(row[0])  # 1
                # 2 Template dans equivalence fichier ligne 3
                tmpRow.append(body.format(
                    row[7], row[15], E, checkIfEmpty(T), checkIfEmpty(row[4].replace('roché', 'roché, couverture souple')), row[5], checkIfEmpty(row[2]), checkIfEmpty(row[6]), checkIfEmpty(row[3]), row[9], row[8]))
                tmpRow.append(vendorField(row[1]))  # 3
                tmpRow.append(T)  # 4
                tmpRow.append(comma.join(tmpTags))  # 5
                tmpRow.append('TRUE')  # 6
                tmpRow.append('Title')  # 7
                tmpRow.append('Default Title')  # 8
                tmpRow.append('')  # 9
                tmpRow.append('')  # 10
                tmpRow.append('')  # 11
                tmpRow.append('')  # 12
                tmpRow.append(row[16]+row[25])  # 13
                tmpRow.append(P)  # 14
                tmpRow.append('shopify')  # 15
                tmpRow.append('1')  # 16
                tmpRow.append('deny')  # 17
                tmpRow.append('manual')  # 18
                if row[17] == '':
                    row[17] = 0
                tmpRow.append("{:.2f}".format(
                    ourPrice(float(row[17]), E)))  # 19
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
