
select __key__ from hero order by __scatter__

select * from hero where __key__ >= $1 and __key__ < $2 order by __key__


select f1, f2, f3 from k where ...

select ... from k
where f1 >= $f1 and f2 >= $f2 and f3 >= $f3
and   f1 < $f1 and f2 < $f2 and f3 < $f3 
