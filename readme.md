This code was written as part of a code submissiong for a job application process. The outline was to 
use python to write an application to pull data from an online source of rocket launches to see if there
is a correlation between the number of sunlight hours before launch and the Right Ascension of the Ascending 
Node (RAAN). What follows below is the readme that was submitted along with the code. 


## RAAN Sunlight Correlation Analyser

### Setup

For this project I used version 3.12.4 of python, installed via homebrew on macOS Sonoma.
I made use of the VSCode IDE, along with the recommended Python plugin. 

The following packages may need to be installed with pip and are listed in the requirements.txt file:
- requests
- pandas
- matplotlib
- suntimes
- pytz
- tzlocal
- jdcal

As part of development, I made use of launch configs to create PROD and DEV versions. These set their 
respective PROD or DEV to the "API_ENV" environment variable, meaning the app can access this via the 
os module. This was utilised in `LaunchDataFetchService` to select the dev or prod URL for fetching data. 
It should also be noted that the class defaults to prod if the environment variable is not found.

With the above modules installed and the desired launch config selected, it should be possible to run
with VSCode's Run/Debug button if this environment is being used. Failing that, the software should
run by invoking main.py from a command line.

### Usage

- After launching the application, you are presented with the data entry tab.
- You can fetch records by entering the number of records you wish to pull and press the `Fetch!` button.
    - When the download is complete, a message box will appear and the UI will upate.
    - You can enter a number of records and fetch again up to 15 times an hour.
    - The fetch will get previous records, so if you request the same number of records each time, no new
    records will be added to the database.
    - If you don't enter a number of records to fetch, the server defaults to return 10 records.
- The record page shows the launch name and id, as well as some other information about that launch.
- You should now be able to browse between records via the `Next` and `Previous` buttons. The browser control
will also show what record you're viewing and out of how manu. 
- To the bottom-left of the window you will see the RAAN value entry component. 
    - If a RAAN value is already present, it will be displayed, but if not, then the entry field remains blank.
    - You can enter a decimal value between 0 and 360 representing the RAAN value for this launch.
    - Press the `Confirm` button to commit that value to the database.
- If you wish to view the data to see if there is a correlation, navigate to the `Analysis` tab.
    - If no values are entered for the RAAN value in the data entry section, the generated graph will be empty. 
- Note the check box on the left of the page. As explained in the text, this changes which mode is used for analysis.
    - When checked, the graph and csv export will map the RAAN to the total hours of sunlight on the launch day.
    - If the checkbox remains unchecked, the app will calculate the amount of sunlight hours elapsed before the launch.
        - This will mean negative values for pre-dawn launches.
        - Launches that happened after sunset will have their sunlight hours capped at the amount for that day.
- Pressing on the `Show RAAN/Daylight Graph` button will show a scatter plot in the specified sunlight mode
- Pressing `Export CSV` will dump the data to a csv file, again in the specified sunlight mode.
    - Note that you need to enter a file name (no need to add the extension) for the file to be saved.
- Pressing `Export PDF` will place the generated graph, in the specified sunlight mode, to a pdf.
    - As with csv export, you need to name the export in the apropriate text entry field to save the file.


### Assumptions Made

Over the course of development, there were several assumptions made and changed. However, those that come
to mind while writing this document are as follows:
- I am assuming that the Net property is the actual time of launch. 
    - This was verified by checking RL's missions history page.
- Assuming altitude of 0 when using the suntimes module for calculating hours of sun.
    - It was possible to specify altitude, but finding that data seemed beyond the scope of the task.
- Made the assumption that if a lunch happens before dawn, it should have negative "sunlight hours before launch"
- Also assumed that if a launch was after sunset, the "sunlight hours before launch" should be capped at the total
number of sunlight hours for that day, as while it was after dark, that sunlight still happened "before launch"
- There was another assumption I was not happy about making, so I offered two options in the software.
    - When generating a graph, it is possible to select a mode and either map the RAAN against the total
hours of sunlight for the launch day OR the number of hours on that day before the launch.
    - To get the sunlight hours before launch, I subtracted the sunrise timestamp from the net timestamp, dividing by 3600
    - As I was not sure what was required, offered both options, but in real world, would clarify info like this.
- Finally, I opted not to use a command line, so when fetching the number of launches, the user would enter the
amount of records to fetch in a provided text box and that is used. 


### Other Considerations

There were other considerationgs made during development and some things cut for time or perhaps being unnecessary:
- Storage of time precision of launch net, so we can warn if any data less accurate then to the minute.
    - The theory here being that some data is less accurate, so the user might want to know of dubious data
- Launch success to optionally ignore failed launches (could extend to ignore specific failure reasons
    - The user might wish to filter out failed launches, so launch success state could have been stored.
- Throwing away unneeded data. 
    - While I am storing lat/lon and some other data in the database, I could have discarded it when the sunlight
hours data had been calculated. However, as storage space/size of db wasn't a concern, I am keeping it for now.
- Capping of data times.
    - As mentioned above, when calculating hours of sunlight before a lunch, if a launch happened before dawn
or after sunset, how should that data be handled. 
    - For pre-dawn launches, do we want negative sunlight hours, or clamp it to zero? I opted for negative, in case that
could affect the correlation.
    - For post-sunset launch, would we cap at the total sunlight hours for that day, or reset the value to zero? In the 
project, I opted to cap at the total sunlight hours for that day, as the light did still happen before launch.


### Other Modules

#### TKinter

I had thought about sticking to a command line application, but as the spec mentions user friendly interface, I 
opted to make use of the Tkinter GUI system. I'd not used this before, so there was a learning curve, but it
seems to have produced a nice application that could be improved upon in the future.

#### Pandas and matplotlib

Pandas is a commonly used library for data processing, so while I have only had limited exposure to it, I opted
to make use of it for processing the data (though I ended up performing manipulation in a SQLite query) and
generating the graphs for display and/or export to pdf. I was happy to see how cleanly it integrates with SQLite.

#### Suntimes

From [this link](https://pypi.org/project/suntimes/) I was able to generate hours of sunlight, sunrise and sunset
for a given lat/lon on a specified day. I used UTC times throughout to reduce as much as possible issues that can
arise when working with dates and times across timezones.

#### Requests

I had started using a different library for fetching the data, but came across [this tutorial](https://github.com/TheSpaceDevs/Tutorials/blob/1b1a40a64b18f7d0ab5d0131189d038fd542b7a9/tutorials/getting_started_LL2/launches_past_month.py) on The Space Devs
own docs site.


### Final thoughts

- I've not added tests. This is largely a timing concern.
- It would be wise to put the fetch request on a background thread so as to not block the app. It's not a huge 
volume of data in this state, but that may not always be the case.
- The view class could benefit from extraction of some UI elements.
    - I did have some components as self-contained widgets, but there were other parts of the UI that could benefit.
    - Time and overhead of passing data around meant I skipped this for now.
- It would be possible to make use of pagination offered by the endpoint, but that seemed beyond the project's scope
- The project includes a file called `test_json.py`. I used this so as to not stress the API endpoint. It's not 
necessary to use, but I've included it in the deliverable as it was part of how I developed the app.
- The strings file was used as a way to not jsut extract hard coded strings, but as a potential starting point for 
localization. Though I think maybe that's beond the scope of internal tooling at this point.

