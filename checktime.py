import time as t


class chukidar:
    def __ini__(self):
        pass

    def check_face(self, name):
        pass


_hour = t.strftime('%H')
_min = t.strftime('%M')

_dat = str(t.strftime('%D'))
_date = _dat.split('/')
print(_date)




print('Hour = {} , Min = {}, day = {}'.format(_hour,_min, _date))

