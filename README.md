# travel_budget

# dump 

docker exec -t postgres_db pg_dumpall -c -U admin > dump_test_15_06_2025.sql

# restore 

cat dump_travel_budget/dump_test_15_06_2025.sql | docker exec -i postgres_db psql -U admin -d travel_budget_db