
<h1 align="center">
  <br>
  <a href="https://xsvcommunity.com"><img src="http://xsv.is/images/default.png" alt="xsvCommunity presents"></a>
  <br>
  xsv-Plugins.
  <br>
</h1>

<h4 align="center">A Random set of bullshit plugins for discord.</h4>

<p align="center">
  <a href="https://discord.gg/UFmhc2p">
    <img src="https://discordapp.com/api/guilds/281663524323983360/widget.png?style=shield" alt="Discord Server">
  </a>
  <a href="https://www.xsvcommunity.com/donate">
    <img src="https://img.shields.io/badge/Support-xsv!-purple.svg" alt="Support the Community!">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Made%20With-Python%203.8-blue.svg?style=for-the-badge" alt="Made with Python 3.8">
  </a>
  <a href="https://crowdin.com/project/xsvcogs">
    <img src="https://d322cqt584bo4o.cloudfront.net/red-discordbot/localized.svg" alt="Localized with Crowdin">
  </a>
  <a href="https://github.com/Rapptz/discord.py/">
      <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
  </a>
</p>


<p align="center">
  <a href="#overview">Overview</a>
  •
  <a href="#cogs">Installation</a>
  •
  <a href="http://">Documentation</a>
  •
  <a href="#installation ">Plugins</a>
  •
  <a href="#join-the-community">Community</a>
  •
  <a href="#license">License</a>
</p>

# Overview

# Cogs

| Name | Status/Version | Description (Click to see full status)
| --- | --- | --- |
| Aviation | **1.1.2** | <details><summary>A cog built to send various Flight data.  Requested by "actual" pilots...</summary></details>|
| Steam | **1.3.8**| <details><summary>Various steam commands and checks.  Game server lists and details, user details and gamelists, sale/wishlist tracker.</summary> This cog has a lot has a few installation requirements to function.  Please visit ... for details</details> |
| Battlefield | **1.2.0** | <details><summary>A cog to send various Battlefield 4 stats.</summary>Note: Due to EA's current non-existant support of any current games.  We are limited to what we can munipulate.</details> |


# Notes/TODO
* Aviation Cog
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



# License

| MIT License | <details><summary>A cog built to send various Flight data.  Requested by "actual" pilots...</summary></details>|


