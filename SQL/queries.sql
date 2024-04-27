select * from paws.shelter_in_out;

-- top 5 reasons of intake -- 

SELECT i.type, COUNT(DISTINCT s.animal_id) AS intake_count
FROM paws.shelter_in_out s 
JOIN paws.pet_intake i ON s.intake_id = i.intake_id
GROUP BY i.type
ORDER BY intake_count DESC
LIMIT 5;

-- Euthanized count --

SELECT p.type,     
COUNT(DISTINCT CASE WHEN s.outcome_type = 'EUTHANIZE' THEN s.animal_id END) AS euthanized_count
FROM paws.shelter_in_out s 
JOIN pet_type p ON p.type_id = s.type_id
GROUP BY p.type
ORDER BY euthanized_count DESC;

-- Percentage of animals per outcome_type -- 
SELECT s.outcome_type, COUNT(s.animal_id) as count from paws.shelter_in_out s
WHERE s.outcome_type IS NOT NULL
GROUP BY s.outcome_type
ORDER BY count DESC
LIMIT 5;

-- Now in percentage -- 
SELECT s.outcome_type,
    COUNT(animal_id) AS outcome_count,
    ROUND(((COUNT(s.animal_id)/ (SELECT COUNT(s.animal_id) FROM paws.shelter_in_out s))* 100.0) , 2) AS percentage
FROM paws.shelter_in_out s
GROUP BY s.outcome_type
ORDER BY percentage DESC
LIMIT 5;

-- Number of animals intake and outcome by animal type: 
SELECT p.type,
    COUNT(DISTINCT s.animal_id) AS intake_count,
    COUNT(outcome_type) AS outcome_count
FROM paws.shelter_in_out s
JOIN paws.pet_type p on s.type_id = p.type_id
GROUP BY p.type;









