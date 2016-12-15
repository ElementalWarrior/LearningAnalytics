
@echo off

del .\data\documents.csv

rem scrape our document set to recommend from (max 500 records hard coded in spider)
echo Scraping documents
scrapy runspider ".\GawkerScraper\ListScraper.py" -o ".\data\Documents.csv" -a stop_at=500 2> err.txt

rem scrape our history (max 500 records hard coded in spider)
rem in order to get data from our history, we have to request it from google. In order to do that, we need an authorization token and developer keywords
rem using chrome you can retrieve this information by:
rem 	navigating to chrome://flags and disabling the QUIC protocol
rem		launching fiddler with ssl decryption enabled
rem		then refreshing the history page and inspecting the response headers to get the authorization token and developer key
rem I would turn off fiddler after you have your token, as it slows scraping a crazy amount
del ".\data\History.csv"

echo Scraping History 1/2
scrapy runspider ".\HistoryScraper\HistoryScraper.py" -o ".\data\History.csv" -a auth_token="[AUTH_TOKEN]" -a dev_key="[DEV_KEY]" -a stop_at=500 2> err.txt

del .\data\fullhistory.json

echo Scraping History 2/2
scrapy runspider ".\HistoryScraper\CsvScraper.py" -o ".\data\fullhistory.json" -a history=".\data\History.csv" 2> err.txt

rem convert json data to sqlite, used sqlite because it should be more efficient in handling condition based queries
echo Converting history to sqlite
python ".\HistoryScraper\Json2Sqlite.py" ".\data\fullhistory.json" ".\Data\browser_history.db"
