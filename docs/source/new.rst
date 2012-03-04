What's new in 0.6.0
===================

API Change
**********

formating
---------

* for the sake of consistency added a pformat for the pprint
* change keys value separator in tformat to **:**.

.. warning:
    Dont use this for serialization unless you want to go into trouble.
    This is only for pretty printing purposes.


not is a problem
****************

Can't find how to overload *! atree*. *__not__* is **not** behaving the way I want. 
I cannot write *a ^ b = ( a & (!b) ) | ( (!a) & b )*

Their will be an inconsistency in the logical operation **notation** because of this pecular side of OO programming as considered right by python specifications. 

Planning on using **rand / ror / rnot / rxor** in the meaning of recursive ... operations. 

I should change all methods naming according to this. Least surprise principle they said :( it is pretty surprising to me that operator overloading cannot be done when all is object... and that it work 99% of the time. 

Too much of a headache write now I postpone thinking

future API change for logical operations
****************************************

**or** behaviour mixes its behaviour with union and or, and **and** with intersection and logical and.
As a dramatic result : 
**xor** does not give the same results as **not xand**. So I will decide either to standardize a three value boolean algebrae where 

* value & undefined  = False
* value | undefined = value

which would be equivalent to state **None = False** but python says : 

 >>> None == False
 False
 >>> None is False
 False
 
or 

