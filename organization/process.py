
# Sun 5 evening    -> 0
# Mon 6 breakfast  -> 1
# Mon 6 lunch      -> 2
# Mon 6 dinner     -> 3
# Tue 7            -> 4, 5, 6
# Wed 8            -> 7, 8, 9
# Thu 9            -> 10, 11, 12
# Fri 10           -> 13, 14, 15
# Sat 11 breakfast -> 16

import csv
import warnings

# additional meals
guests = [
    ('Elise', 'Goujard', [5]),
    ('Baptiste', 'Louf', [8]),
    ('Mireille', 'Bousquet-Mélou', [11])
    ]

def date_index(entry, end=False):
    ans = entry.split(' ')
    date = shift = None

    try:
        date = int(ans[0].strip())
    except ValueError:
        warnings.warn('unknown date {!r}'.format(ans[0]))

    if len(ans) == 2:
        time = ans[1]
        if time == 'morning':
            shift = 0
        elif time == 'afternoon':
            shift = 1
        elif time == 'evening':
            shift = 2
        else:
            warnings.warn('unknown time {!r}'.format(ans[1]))

    if date is None:
        date = 11 if end else 5

    if shift is None:
        if not end:
            if date == 5:
                shift = 1
            else:
                shift = 0
        else:
            if date == 11:
                shift = 0
            else:
                shift = 2

    i = 3 * (date - 5) + shift - 1
    assert 0 <= i < 18, (entry, i)
    return i

def write_meals():
    with open('output/meals.csv', 'w') as meals:
        meals.write('first name,')
        meals.write('last name,')
        meals.write('dim 5 dîner,')
        meals.write('lun 6 petit déj, lun 6 midi, lun 6 soir,')
        meals.write('mar 7 petit déj, mar 7 midi, mar 7 soir,')
        meals.write('mer 8 petit déj, mer 8 midi, mer 8 soir,')
        meals.write('jeu 8 petit déj, jeu 8 midi, jeu 8 soir,')
        meals.write('ven 9 petit déj, ven 9 midi, ven 9 soir,')
        meals.write('sam 10 petit déj\n')

        csv_rows = []
        with open('nights_and_food.csv') as csvfile:
            data = csv.DictReader(csvfile, delimiter=',')
            for row in data:
                start = date_index(row['arrival'])
                end = date_index(row['departure'], end=True)
                first_name = row['first name']
                last_name = row['last name']

                csv_row = [row['first name'], row['last name']]
                csv_row += [int(start <= x < end) for x in range(17)]

                if first_name == 'Nicolas' and last_name == 'Delbovier':
                    # jeune intermittant
                    csv_row[3::3] = [0] * 6
                    print('nico')

                if first_name == 'Zoé' and last_name == 'Varin':
                    # Zoé Varin ne sera pas la au petit dej et au repas du midi le mardi
                    print('zoé')
                    csv_row[2 + 4] = csv_row[2 + 5] = 0

                if first_name == 'Clément' and last_name == 'Legrand-Duchesne':
                    # Clément Legrand-Duchesne ne sera pas le au petit dej et au repas du midi le mercredi.
                    print('clément')
                    csv_row[2 + 7] = csv_row[2 + 8] = 0

                csv_rows.append(csv_row)

        for first_name, last_name, presence in guests:
            csv_row = [first_name, last_name] + [0] * 17
            for i in presence:
                csv_row[2 + i] = 1
            csv_rows.append(csv_row)

        meal_numbers = [0] * 17
        for csv_row in csv_rows:
            meals.write(','.join(map(str, csv_row)))
            meals.write('\n')
            for i in range(17):
                meal_numbers[i] += csv_row[i + 2]

        meals.write('TOTAL,,')
        meals.write(','.join(map(str, meal_numbers)))
        meals.write('\n')


def write_mdn_nights():
    with open('nights_and_food.csv') as csvfile:
        data = csv.DictReader(csvfile, delimiter=',')
        with open('output/nights_mdn.csv', 'w') as mdn:
            mdn.write('first name, last name, arrival, departure\n')
            for row in data:
                first_name = row['first name']
                last_name = row['last name']
                arrival = row['arrival']
                departure = row['departure']
                where = row['where']
                if where == 'maison':
                    mdn.write('{},{},{},{}\n'.format(first_name, last_name, arrival.split()[0], departure.split()[0]))

write_meals()
write_mdn_nights()
