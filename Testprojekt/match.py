



alter = 28
items = [1, 2, 2, 3, 5, 4]
daten = {'Name': 'Max', 
         'Nachname': 'Mustermann', 
         'Ort': 'Potsdam', 
         'PLZ': 14469}

print(f'"Match" mit "Catch All" Muster')
match alter:
    case _ if alter >= 18:                      # Gilt immer, aber unter der 
        print(f'volljährig\n')                    # Einschränkung alter >= 18
    
    case _ :
        print(f'nicht volljährig\n')



print(f'"Match" mit exakter Länge oder *splat-Operator für beliebige Länge.')
match items:
    case [x, y, 0]:
        print(f'Liste mit 3 Items {x}, {y} und 0 an Ende\n')
    
    case [x, y, *z]:
        print(f'x = {x}')
        print(f'y = {y}')
        print(f'z = {z}\n')

    case _ :
        print(f'Etwas Anderes\n')



print(f'"Match" mit Prüfung auf Dictionary.')
match daten:
    case dict():
        print(f'Das Objekt ist ein Dictionary.\n')
    
    case _ :
        print(f'Das Objekt ist etwas Anderes.\n')


print(f'"Match" mit Prüfung auf Keys.')
match daten:
    case {'Name': name, 'Nachname': nachname}:
        print(f"""Das Dictionary besitzt die Schlüssel:
              Name: {name},
              Nachname: {nachname}\n""")
    case _ :
        print(f'Das Objekt besitzt die erforderlichen Keys nicht.\n')

print(f'"Match" mit Prüfung auf bestimmten Wert unter Keys.')
match daten:
    case {'Name': 'Max', 'Nachname': 'Mustermann'}:
        print(f"""Das Dictionary besitzt die Schlüssel:
              Name: {name},
              Nachname: {nachname}
Und die Werte entsprechen den Anforderungen.""")
        
    case _ :
        print(f'Das Objekt besitzt die erforderlichen Werte unter Keys nicht.\n')