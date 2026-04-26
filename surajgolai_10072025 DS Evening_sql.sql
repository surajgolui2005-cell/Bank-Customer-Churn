create database bank_customber;
use bank_customber;
show tables;

#1 

select i.customer_id,i.country, s.balance from account_fact s join customer_dim i on s.customer_id = i.customer_id;

#2

select customer_id,credit_card from account_fact where credit_card != 0;

#3

select count(customer_id) from account_fact;

#4

select 
    i.country, 
    avg(s.balance) AS average_balance, 
    count(*) AS total_customer
from account_fact s 
join customer_dim i 
    on s.customer_id = i.customer_id
group by i.country
having COUNT(*) > 50;

#5
select 
    i.gender, 
    avg(s.credit_score) as average_balance, 
    count(*) as total_customer
from account_fact s 
join customer_dim i 
    on s.customer_id = i.customer_id 
where s.active_member = 1
group by i.gender;

#6 

select count(customer_id) as number_churn from account_fact where churn = 1;

#7

select avg(credit_score) as avg_credit_Score from account_fact where active_member = 1;

#8
select customer_id , balance from account_fact where balance > (select avg (balance) from account_fact);


#9

select 
    i.country, 
    avg(s.balance) AS average_balance, 
    count(churn) AS total_churn
from account_fact s 
join customer_dim i 
    on s.customer_id = i.customer_id
group by i.country
having COUNT(churn) > 10;












