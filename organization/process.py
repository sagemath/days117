
# 5 evening    -> 0
# 6 breakfast  -> 1
# 6 lunch      -> 2
# 6 dinner     -> 3
# 7            -> 4, 5, 6
# 8            -> 7, 8, 9
# 9            -> 10, 11, 12
# 10           -> 13, 14, 15
# 11 breakfast -> 16

import csv

def date_index(entry, end=False):
    ans = entry.split(' ')
    if len(ans) == 2:
        date = int(ans[0].strip())
        time = ans[1]
        if time == 'morning':
            shift = 0
        elif time == 'afternoon':
            shift = 1
        elif time == 'evening':
            shift = 2
        else:
            print('WARNING: what is time={!r}?'.format(time))
            shift = 0 if date > 5 else 1
        return 3 * (date - 5) + shift - 1
    else:
        return 17 if end else 0

def write_meals():
    meal_numbers = [0] * 17
    with open('nights_and_food.csv') as csvfile:
        data = csv.DictReader(csvfile, delimiter=',')
        for row in data:
            arrival = row['arrival']
            departure = row['departure']
            for i in range(date_index(arrival), date_index(departure, end=True)):
                meal_numbers[i] += 1

    with open('output/meals.csv', 'w') as meals:
        meals.write('dim 5 dîner,')
        meals.write('lun 6 petit déj, lun 6 midi, lun 6 soir,')
        meals.write('mar 7 petit déj, mar 7 midi, mar 7 soir,')
        meals.write('mer 8 petit déj, mer 8 midi, mer 8 soir,')
        meals.write('jeu 8 petit déj, jeu 8 midi, jeu 8 soir,')
        meals.write('ven 9 petit déj, ven 9 midi, ven 9 soir,')
        meals.write('sam 10 petit déj\n')
        meals.write(','.join(map(str, meal_numbers)))

write_meals()
