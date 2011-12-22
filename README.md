I want to add addition to dict in python !!

It seems a long time ago in a faraway galaxy some wise men decided
dict() + dict() had no sense amongst the python jedis.

There reasoning was what happens when to keys collides ? 

Well, who cares ? 

If it adds like a duck, commute like a duck, than it is an addition 

#how to test for addition ?#

test.py in this project define a consistent behaviour based on what
someone familiar to addition expect. 

That I resume as follow : 

Addition should follow these rules 

> a + b = b + a 
> a + neutral = a 
> 1 * a = a 
> an_int * a = a + ... + a (n times ) 
> an_int * a = a * an_int 
> -a = -1 * a 
> a - b = a + ( -1 * b) 
> an_int ( a + b) = an_int *a + an_int * b 

for complete result see : 

https://github.com/jul/ADictAdd_iction/wiki/test_result

You'll notice through some example that some python default objects dont
comply to the addition as we know in linear algebrae.

But, given a magical definition, dict + dict behaves in a consistent way.

#How does a dict that follow these rules behaves ?#

Mostly like an arbitrary vector whose orhtogoonal dimensions are those define 
by the path of keys, and for wich the value is a somethin that also supports the
same rules. 

Has it a sense ? 

I don't know, but at least it is consistent
