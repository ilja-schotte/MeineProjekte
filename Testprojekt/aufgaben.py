


alter = int(input(f'Ihr Alter:'))


match alter:
    case _ if (14 <= alter < 18):
        print(f'jugendlich')
    case _ :
        print(f'nicht jugendlich')

