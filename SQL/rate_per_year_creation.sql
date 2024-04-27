CREATE TABLE rate_per_year
select YEAR(month) as year, erd.eviction_filing_rate
  from final_project.eviction_rate_data erd
      where erd.site = 'all_sites' and erd.month like '%-12-01%';
      
            
select * from rate_per_year;

select * from final_project.eviction_rate_data e
where e.site = 'all_sites';