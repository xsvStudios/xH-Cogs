<h1 align="center">
  <br>
  <a href="https://xsvcommunity.com"><img src="http://xsv.is/images/default.png" alt="xsvCommunity presents"></a>
  <br>
  A Random set of bullshit cogs.
  <br>
</h1>
# Trusty-cogs V3
[![Red-DiscordBot](https://img.shields.io/badge/Red--DiscordBot-V3-red.svg)](https://github.com/Cog-Creators/Red-DiscordBot)
[![Discord.py](https://img.shields.io/badge/Discord.py-rewrite-blue.svg)](https://github.com/Rapptz/discord.py/tree/rewrite)
[![Join us on Discord]](https://discord.gg/UFmhc2p)

# xsvCogs


## About Cogs

| Name | Status/Version | Description (Click to see full status)
| --- | --- | --- |
| Aviation | **1.1.2** | <details><summary>A cog built to send various Flight data.  Requested by "actual" pilots...</summary></details>|
| Steam | **1.3.8**| <details><summary>Various steam commands and checks.  Game server lists and details, user details and gamelists, sale/wishlist tracker.</summary> This cog has a lot has a few installation requirements to function.  Please visit ... for details</details> |
| Battlefield | **1.2.0** | <details><summary>A cog to send various Battlefield 4 stats.</summary>Note: Due to EA's current non-existant support of any current games.  We are limited to what we can munipulate.</details> |


# Notes/TODO
## Aviation Cog
### Commands
### Weather METAR
#### Command: !metar
##### Parameter: Station ID.

#### Data:
* Flight Category: VFR
* Raw Text
* Station ID:  The ID of the airport.  Lookup table https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat
* Station ID Actual Name: The full name for the station ID
* observation time: Data timestamp
* Temp:
* Dewpoint
* Wind Direction
* Wind Speed
* Wind Gust
* Visibility
* altimeter:  Inches in Mercury? Precision is 2 decimal places. x.00
* Sea Level
* Sky condition

### Bot Output (exising depracated bot)
* METAR for KARM
* KARM 190015Z AUTO 08007KT 10SM SCT110 17/00 A3023 RMK AO2 T01671003

* Station: KARM
* Observed at: 2019-03-19 00:15:00Z
* Temperature: 16.700°C (62.060°F)
* Dewpoint: -0.300°C (31.460°F)
* Winds: 7 knots at 80°
* Visibility: 16093m (10.00sm)
* Pressure: 1024 hPa (30.23 in Hg.)
* Sky Conditions
* Scattered clouds at 11000
* Flight Category: VFR
* Retrieved in 7ms.

### Flightinfo
    - Departure location
    - Arrival Location
    - Flight times
    - Speed
    - Altitude
    - Weather?
    - Map

# Battlefield
## TODO
