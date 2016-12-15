
@echo off
chcp 65001
del data\user1.csv
del data\user2.csv
del data\user3.csv
del data\user4.csv
del data\user5.csv
echo create a user profile from normal history
python ".\User Builder\user_builder.py" "data\browser_history.db" "data\user1.csv"

echo create a user profile up to a certain date
python ".\User Builder\user_builder.py" "data\browser_history.db" "data\user2.csv" -t 2016-12-15T1:00:00Z

echo create a user profile for sports
python ".\User Builder\user_builder.py" "data\browser_history.db" "data\user3.csv" -k "football baseball soccer rugby"

echo create a user profile for programmers
python ".\User Builder\user_builder.py" "data\browser_history.db" "data\user4.csv" -k "sql python programming"

echo create a user profile for foodies
python ".\User Builder\user_builder.py" "data\browser_history.db" "data\user5.csv" -k "recipe sous vide cooking"




rem Recommend docs

echo "Recommendations from normal browser history"
python "Profiler\doc_profiler.py" "data\Documents.csv" "data\user1.csv"

echo "Recommendations from up to a certain date"
python "Profiler\doc_profiler.py" "data\Documents.csv" "data\user2.csv"

echo "Recommendations for sports"
python "Profiler\doc_profiler.py" "data\Documents.csv" "data\user3.csv"

echo "Recommendations for programmers"
python "Profiler\doc_profiler.py" "data\Documents.csv" "data\user4.csv"

echo "Recommendations for gamers"
python "Profiler\doc_profiler.py" "data\Documents.csv" "data\user5.csv"
