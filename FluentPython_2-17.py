from collections import namedtuple

'''
City = namedtuple('City', 'name country population coordinates')
LatLong = namedtuple('LatLong', 'lat long')

tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
print(tokyo.population)
print(City._fields)

delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28613889, 77.208889))
delhi = City._make(delhi_data)
print(delhi)
print(delhi._asdict())
for key, value in delhi._asdict().items():
    print(key + ':', value)
'''    
    
l = [10, 20, 30, 40, 50, 60]
print(l[2:])