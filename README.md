I want to add addition to dict in python !

It seems a long time ago in a faraway galaxy some wise men decided
dict() + dict() had no sense amongst the python jedis.

They were wondering : what happens when to keys collides ? 

Well, who cares ? 

If it adds like a duck, commute like a duck, than it is an addition 

#how to test for addition ?#

test.py in this project define a consistent behaviour based on what
someone familiar to addition expect. 

That I resume as follow : 

Addition should follow these rules (cf Mc Graw Hill Linear 
Algebrae Chapter 1 by Seymour Lipschutz)

> a + b = b + a 

> a + neutral = a 

> 1 * a = a 

> an_int * a = a + ... + a (n times ) 

> an_int * a = a * an_int 

> -a = -1 * a 

> a - b = a + ( -1 * b) 

> an_int ( a + b) = an_int *a + an_int * b 

> ( a + b ) + c = a + ( b + c )

> ( an_int + another_int ) a  = an_int * a + another_int * a

> ( an_int * another_int ) a = an_int (  another_int * a ) 



for complete result see : 

https://github.com/jul/ADictAdd_iction/wiki/test_result

You'll notice through some example that some python default objects dont
comply to the addition as we know in linear algebrae.

But, given a magical definition, dict + dict behaves in a consistent way.

#How does a dict that follow these rules behaves ?#

Mostly like an arbitrary vector whose orhtogonal dimensions are those define 
by the path to the keys, and for wich the value is a something that also supports the
same rules. (This at my opinion is just a too strong limitation, but I try to avoid
that some people get apoplexia).

Has it a sense ? 

I don't know, but at least it is consistent.

# Future

I am currently forseeing a definition of dict * dict that would induce the following :

- a distance
- projection
- linear combination. 

Wich would be coherent to usual linear algebrae

As a result of linear combination of dict we therefore will be able to define
matrix, and a whole new sets of operations very usefull in map reduce operations.

In the era of big data we could do in a single operation things such as : 

- correlation matrix ; 
- cosine between dict ;
- projecting vectors from one space to the others (such as natural translations);

And through the sheer help of algorithms we could do stuff unheard in mathematics
such as non linear computed matrix. 

# Where is the bug

One might notice that in geometry there is much more than one algebrae. For instance
we could see also dict as bra and kets as in Hilbertian algebrae. And one might
wonder if it is such a good idea to canonize mul/div/sub/add operations to 
those of linear algebrae since even though it is the most intuitive and used
one, it may not be revelant to everyone.

As a result object supporting add / mul / div / sub may have a property telling
wich algebrae it enforces, and may support more than one algebrae. We might also
therefore have generic unit tests defining algebrae that are to be passed by
object in order to define the behavior. 

We might also wonder if algebra is a behavior of and object (like a quaking definition), or if it is a virtual  object which an oject is derived.

I might say, If anyone dare accept the challenge of accepting this definition of
what a dict is we clearly open a pandora's box which raises the following issues : 
- will this bloat python ? 
- will this break the conceptual integrity of the langage by shifting some code
into algebraic definition ? 
- does it worths the shot in term of performance ? 

I may have a single unpythonic reason to love this idea of introducing consistens
distincts algebrae in a programming langage : 

- it opens new doors to what we can express in few words ;
- it seems utterly fun ! 

And fun is always a good motivation to do stuff


