# Random ideas - thinking out loud.


## Data model for Eve Argus

### Proposal - make market histories a limited range of dates.
1. Download market history.
2. Check if the data is in the curent 20+ day collection for that region.
3. If not, add it to the collection.
4. check if older data is in the archived collection. (Archive by year)
5. If not, add it to the archived collection.

### Proposal - Only keep market history summary data in app.
Given that it is impossible to download less than the full year of market history data and all work done in the app is with history summaries.
1. Check for required history summary data in the database that meets effective_date criteria.
2. If not available, download the full year of market history data.
3. Create a summary of the data.
4. Store the summary in the database.
5. Option to store the full download of data in an export file.

### Proposal - make an export file format for market history downloads.
Because there is a cost in time to download the market history for a region, it would be useful not to have to reaquire data between each invocation of the cli app.
1. consider jsonl format so that metadata can be stored in the first line.
2. Store all the requested data per session and region_id on one file.
   e.g. 300 type_ids for region x in one file, or limit # of type_ids per file, so multiple files per session
3. Store time of request, region_id and list of type_ids in metadata.
4. Its possible to chunk the type_ids in market, and split data files that way. e.g 5000 ids per file.
5. Or, when a download is requested, check for already aquired data, and only download new data.
6. Later, implement code to deduplicate and archive data (Downloads of same history on different days).

### Proposal - make an export file format for market orders.
Because there is a cost in time to download the market orders for a region, It would be useful not to have to reaquire data between each invocation of the cli app.
1. Use jsonl format to store metadata on the first line.
2. include effective date and region_id in metadata

### Proposal  - figure out common code for working with jsonl files.
1. Make a simple jsonl file format, with a dict on the first line that contains arbitrary metadata.
2. Each succeeding line is a json string of the same data structure.
3. Make generic reader and writer functions with these assumptions.
5. Make a csv export function for the jsonl format.
6. Make this a mini-project.