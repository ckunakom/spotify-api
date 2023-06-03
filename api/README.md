### Steps to follow
1. Run `authorization.py`
1. Click on the URL and sign in. You will get a 404 callback error. Just copy the `code` from the URL: https://google.com/callback?code=`AQDXzlJD-sOW3pUwgmkDsr3U5zuKdQjPW7fm7qc3q5ExUgWShvjb25p28lUi81_X-gSV_7QeVFURp5dbZ7vJdepOoKWCjI-7JrAaekkd_TDfjmnT1mHUkjOT0xUEFdUs7Ric2LMqTpcHqYlnR8C-8xYOrBuipq7gTCpVsV9anTHRcoit7eSd9XkW19DnCA`
    - Sorry for the ghetto-ness but this has to do for now.
1. Paste the copied code string to your `.env` file for `code_from_url`
1. Run `artist.py`. This will also run `top_tracks.py`.
    - You can change the `time_range` in  `top_tracks.py`. The default is 6-month.
1. Two json files will get generated. If you want to use tableau dashboard template, then run the `data_cleaning.py`.