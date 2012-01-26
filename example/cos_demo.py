#!env python
# -*- coding: utf-8 -*-
"""
playing with cos and dot product of dict

"""
import os, sys, inspect
cmd_folder = os.path.abspath(
    os.path.join(
        os.path.split(
            inspect.getfile( inspect.currentframe() )
        )[0] ,
        ".."
    )
)
if cmd_folder not in sys.path:
   sys.path.insert(0, cmd_folder)

from math import sqrt
from numpy import array
from vector_dict.VectorDict import VectorDict


def assert_is_cos(func):
    """verify that a functions returns an int or a float in [-1;1]
    sneakily cast the return value in float to check the return value
    is castable as float
    """
    def wrapper(*a, **kw):
        res = func(*a, **kw)
        if 1 >= float(res) >= -1:
            try:
                return float(res)
            except Exception as e:
                raise Exception(
                    "wrong type %r for cos return (%r)" % (
                    res.__class, e
                    )
                )
        else:
            raise Exception("Cosinus : invalid range %r %r(%r ,%r) " % (
                    res, func, a, kw
                )
            )
        return res
    return wrapper

data = [
    dict(
        physical = dict(
            eye = "00FF00",
            heigth = 1.92,
            weigth = 52.1
        ),
        name = "jenny",
        salary = 500.00,
        presentation= [
            ("modeling show", "Paris", 2012),
            ("green cover", "Vogue", 2011),
        ],
    ),
    dict(
        physical = dict(
            eye = "00FFA0",
            heigth = 1.72,
            weigth = 48.1
        ),
        name = "noxco",
        salary = 700.00,
        presentation= [
            ("green cover", "Vogue", 2011),
            ("catholic fashion show", "Roma", 1977),
        ],
        program = ["python"],
    ),
    dict(
        physical = dict(
            eye = "000000",
            heigth = 1.65,
            weigth = 52.1
        ),
        name = "Derpina",
        salary = 300.00,
        program = ["python", "Perl"],
        hobby = ["sky", "9gag"]
    ),
]


@assert_is_cos
def bankable_cos( input_dict ):
    """the more a model has been exposed the more valuable it is"""
    return 1.0 * (  2.0 *  min( len(input_dict.get("presentation",[])), 3) / 3 - 1 )

def matrix( input_dict ):
    return VectorDict( float, 
        dict( 
            eye = eye_cos( "00FF00", input_dict ),
            fitness = imc_cos( 
                imc( 
                    input_dict.get("physical", dict() )
                ), 
                14.0, 
                5
            ),
            ## as long as its between -1, 1 it is a cos :) why bother 
            ## the more someone took parts in event (given a threshold) 
            ## then he or she is bankable
            bankable = bankable_cos( input_dict ),
            extra = extra_cos( input_dict ),
            not_too_expensive = wage_cos(300.0, 700, input_dict )
       )
    )

@assert_is_cos
def extra_cos( input_dict ):
    """discrete cos value sample : 
    1 (ideal) if has hobbies + python
    2 mixed case if has hobby and program in perl & python or
    program in python only
    3 null if orthogonal (no values in fields or projection is 0
    """
    return ( 
        ( "python" in input_dict.get("program", [] ) and 1 or -1 ) - 
        ( "Perl" in input_dict.get("program", [] ) and -1 or 0 ) + 
        ( input_dict.get("hobby") is not None and 1 or 0 )
    ) / 2
    
@assert_is_cos
def wage_cos(optimal, max_salary, input_dict ):
    """sample of float value illustrating what a cos means for float
    in regard to the utility
    1) max (1)  if you dont have to pay (salary = 0)
    2) orthogonal if not knwon or pay what you expect 
    3) (-1) min if you pay more than what you expected with a floor"""
    salary = input_dict.get("salary", max_salary )
    if salary >= max_salary:
        return -1
    if salary > optimal:
        return  (  optimal - salary ) / (  max_salary - optimal)
    return  ( salary / optimal )  - 1.0 

def scalar( v1, v2 ):
    """norm of the dot product of two vectors"""
    return (v1 ).dot(v2 ) 

def norm( v1 ):
    """ norm of a numpy array"""
    return sqrt( scalar( v1, v1 ) )

def imc( phys_dict ):
    """I really hate imc stuff, so this is a random formula"""
    weigth = 1.0 * phys_dict.get("weigth",120.0) 
    heigth = 1.0 *  phys_dict.get("heigth",1.55) 
    return  weigth * weigth / ( 100.0 * heigth  )

@assert_is_cos
def imc_cos( imc, ideal_imc, max_var):
    """return 1 if it is exactly the imc
    -1 if imc belongs to [ imc + max_var, inf [ or ] 0; imc - max_var ]
    linear in between"""
    return  max( - 2 *  abs( imc - ideal_imc )  / ( max_var ) + 1 , -1 )

@assert_is_cos 
def eye_cos( prefered_color, input_dict):
    """ a true simmilaruty cosins the way it is supposed to be done
    after we have split color in usual css format to a rgb vector
    """
    phys = input_dict.get("physical", dict())
    rgb_vect = array( [ int(x) for x in bytearray.fromhex( 
        phys.get( "eye", "000000" ) )[0::1]
    ] )
    prefered_vect =  array([ int(x) for x in bytearray.fromhex(prefered_color)[0::1] ] )
    max_size = norm( prefered_vect ) * norm( rgb_vect ) 
    return  max_size > 0  and  ( 
                1.0 * sum( prefered_vect * rgb_vect)  / ( max_size )
            ) or -1


criterion_ponderation = VectorDict(float, dict( 
    eye = 1 ,
    fitness = 5,
    bankable = 4,
    extra = .5,
    not_too_expensive = .1
) )

norm_of_choice = criterion_ponderation.dot(criterion_ponderation)


for candidate,ldot in    map ( 
            lambda x :  [ 
                VectorDict(VectorDict,x) , criterion_ponderation.dot( 
                    criterion_ponderation * matrix( x ) 
                )
            ] , 
            data
        ) : 
    if ldot > .5:
         candidate.pprint()
         print "fitting with a projection of %f" % ldot

criterion_ponderation = VectorDict(float, dict( 
    eye = 1.0,
) )
print "\n"
print "*" * 80
print "must have green eyes " 

for candidate,ldot in    map ( 
            lambda x :  [ 
                VectorDict(VectorDict,x), criterion_ponderation.dot( matrix( x ) )
            ] ,
            data
        ) : 
    #criterion_ponderation.homothetia(matrix(candidate)).pprint()
    if 1.0 == ldot:
         print "MATCH"
         candidate.pprint()
         print "has a projection on maximum fit of 1 %f" % ldot

criterion_ponderation = VectorDict(float, dict( 
    fitness = 1.0 ,
) )

by_fitness = map ( 
            lambda x :(   
                VectorDict(VectorDict,x), criterion_ponderation.dot(matrix( x ) )
                ), 
            data
    )  

print "*" * 80

print "best candidate IMC is " 
candidate , ldot = sorted( by_fitness, cmp= lambda x,y : - cmp( x[1], y[1] ))[0]
print "with a projection of %f" % ldot 
candidate.pprint()
