# randomisedString v1.3.1

```pip install randomisedString --upgrade```


###### <br>A well maintained program to generate randomised strings. Can be used for assigning unique IDs of any specified size. Can be alpha only or numeric or alphanumeric as specified.


<br>To install: 
```
pip install randomisedString --upgrade
pip3 install randomisedString --upgrade
python -m pip install randomisedString --upgrade
python3 -m pip install randomisedString --upgrade
```


#### <br><br>Using this program is as simple as:
```
from randomisedString import Generator as StringGenerator

generator = StringGenerator()

print(generator.AlphaNumeric(10, 10))
>> 45HCMJ4SCy
print(generator.OnlyNumeric(10, 10))
>> cmkntCBmdp
print(generator.OnlyAlpha(10, 10))
>> UjfQZDDOOq
print(generator.AlphaNumeric(5, 10))
>> FxgirdEYB
print(generator.OnlyNumeric(5, 10))
>> XYfzAT
print(generator.OnlyAlpha(5, 10))
>> HqGiHqt
```


### Future implementations:
* Include special characters.


###### <br>This project is always open to suggestions and feature requests.