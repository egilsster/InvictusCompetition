# InvictusCompetition
Parser for CrossFit Invictus Competition workouts

# API Usage

Get a specific workout by date (format: [Month] [Day], [Year]).
```
/api/workout/<string:date>
```

Get the pages of workout links on the Invictus Competition site, by page number.
```
/api/workouts/<string:page>
```