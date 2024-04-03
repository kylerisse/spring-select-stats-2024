# spring-select-stats-2024

Script to generate and maintain [Sports Club Stats](http://www.sportsclubstats.com) league data for the AYSO Section 1 Areas N and R [2024 Spring Select](https://ayso.bluesombrero.com/Default.aspx?tabid=948335) season.

- [10U Girls](http://www.sportsclubstats.com/You/Area1NR10ug.html)
- [12U Boys](http://www.sportsclubstats.com/You/Area1NR12ub.html)
- [12U Girls](http://www.sportsclubstats.com/You/Area1NR12ug.html)
- [14U Boys](http://www.sportsclubstats.com/You/Area1NR14ub.html)
- [14U Girls](http://www.sportsclubstats.com/You/Area1NR14ug.html)
- [16U Boys](http://www.sportsclubstats.com/You/Area1NR16ub.html)
- [16U Girls](http://www.sportsclubstats.com/You/Area1NR16ug.html)

For the most part, the rules match those defined for the league. Where they differ is when dealing with standings tiebreakers and how points deductions are handled. The cases where these will have any impact should be very rare.

- The 2nd tiebreaker is head to head total goals scored with a max of 5 per game. Setting a max goals per game just for tiebreakers doesn't seem possible in the documentation.
- The 6th, 7th, and 8th tiebreakers revolve around fewest games with cautions and send-offs, which are either not available (cautions) or not displayed per game (send-offs) on the standings spreadsheet. We get pretty close by using the `FairPlay` score to track send-offs and using that as the tiebreaker.
- 1 Standings point is reduced per team for both send-offs and reporting violations. There wasn't a way to add negative points as part of individual game results, so I leverage the `StartPoints` score as a work around and regenerate the league each import. The main downside of this is that teams will appear to start with negative scores on the graph rather than accurately reflecting them as they happen throughout the season.

## Not Implemented

- Automatic scraping of the source spreadsheet. I chose to maintain my own CSVs instead. This is partially because the fields are overloaded in the spreadsheet, with `${TEAMNAME}-${GOALS}` as a typical format which could just be string split, but I don't trust that the pattern will always be 100% followed. The second is that a lot of games are being rescheduled due to heavy rain and that information is communicated inconsistently through blank fields and color coding. Given the additional complexity and maintenance burden this would add to the code vs the low effort of updating my records once a week, I chose the latter.
- Automatic email sending. I'll probably add this next.
