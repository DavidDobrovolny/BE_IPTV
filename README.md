# BE IPTV

## Setup

1) Initialize the database
`docker compose run web python manage.py migrate`

2) Run the application
`docker compose up`


## Environment variables

- POSTGRES_[DB, USER, PASSWORD] - database (dockerised) credentials (would be passed via secrets in real application)
- API_URL - URL of the API to download the data from
- LOOP_DELAY - how often, in seconds, is the API read; defaults to 5 minutes if omitted


## Important files

- iptv/api_dl.py - handles downloading the data from the API and saving the data to the database
- iptv/views.py - handles filtering, sorting and passing the saved date to frontend
- iptv/templates/iptv/video_list.html - server-side rendered frontend, which allows user to filter and sort the data


## Remarks

- while downloading and processing the API data, the majority of the time is spent on downloading
  video icons; could be done asynchronously
- when the filters/sorting change on the frontend, the data is fetched again;
  could be done dynamically on the frontend
- if the volume of data got bigger, page load time would be uncomfortably long; could be paginated
