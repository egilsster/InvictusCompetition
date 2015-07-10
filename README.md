# InvictusCompetition
Parser for CrossFit Invictus Competition workouts

# API Usage

Get a specific workout by date (format: [Month] [Day], [Year]).
```
/api/v1.0/workout/<string:date>
```

Get the pages of workout links on the Invictus Competition site, by page number.
```
/api/v1.0/workouts/<string:page>
```