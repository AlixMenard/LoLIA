## Frame data :
- ### Player data :
  - kills <sup>x</sup>
  - deaths<sup>x</sup>
  - assists<sup>x</sup>
  - total gold<sup>x</sup>
  - level
  - creepScore
  - currentHealth
  - maxHealth
  - *killParticipation*
  - wardsPlaced
  - wardsDestroyed
  - AD
  - AP
  - critChance
  - AS
  - lifeSteal
  - armor
  - magicResistance
  - tenacity
  - championDamageShare
- ### Team data :
  - inhibitors<sup>x</sup>
  - towers<sup>x</sup>
  - baron
  * **dragons** :
    * infernal
    * wind
    * ocean
    * earth
    * chemtech
    * hextech
    * elder
    * *hasSoul*
- ### Frame data :
  - timeStamp

<sup>x</sup> `+ 5min delta`


## Tables Structure
### Metadata

| Column  | Data Type | Description                              |
|---------|-----------|------------------------------------------|
| id      | INTEGER   | Primary key, unique identifier           |
| gameId  | INTEGER   | Game ID                                  |
| date    | DATE      | Date of the game                         |
| year    | INTEGER   | Year of the game                         |
| playoff | BOOLEAN   | Indicates if it is a playoff game        |
| win     | INT       | Indicates blue team score after the game |
| time    | INTEGER   | Indicates in-game time in seconds        |

### Team data
Column names should be preceded by the related team (e.g. *redInhib* and *blueInhib*) 

| Column    | Data Type | Description                                |
|-----------|-----------|--------------------------------------------|
| Inhib     | INTEGER   | Destroyed inhibitors                       |
| Inhib_5   | INTEGER   | Destroyed inhibitors in the last 5 minutes |
| Towers    | INTEGER   | Destroyed towers                           |
| Towers_5  | INTEGER   | Destroyed towers in the last 5 minutes     |
| Barons    | INTEGER   | Killed barons                              |
| Barons_5  | INTEGER   | Killed barons in the last 5 minutes        |
| Dragons   | INTEGER   | Killed drakes                              |
| Dragons_5 | INTEGER   | Killed drakes in the last 5 minutes        |
| Infernals | INTEGER   | Killed infernal drakes                     |
| Clouds    | INTEGER   | Killed cloud drakes                        |
| Oceans    | INTEGER   | Killed ocean drakes                        |
| Mountains | INTEGER   | Killed mountain drakes                     |
| Chemtechs | INTEGER   | Killed chemtech drakes                     |
| Hextechs  | INTEGER   | Killed hextech drakes                      |
| Elders    | INTEGER   | Killed elder drakes                        |
| Elders_5  | INTEGER   | Killed elder drakes  in the last 5 minutes |

### Player data
Column names should be preceded by the related team, followed by the role (e.g. *redTopKills* and *blueTopKills*).\
Roles are Top, Jungle, Mid, Bot, Supp.

| Column         | Data Type | Description                           |
|----------------|-----------|---------------------------------------|
| Kills          | INTEGER   | Ennemies killed                       |
| Kills_5        | INTEGER   | Ennemies killed in the last 5 minutes |
| Deaths         | INTEGER   | Deaths                                |
| Deaths_5       | INTEGER   | Deaths in the last 5 minutes          |
| Assists        | INTEGER   | Kill assists                          |
| Assists_5      | INTEGER   | Kill assists in the last 5 minutes    |
| Golds          | INTEGER   | Earned golds                          |
| Golds_5        | INTEGER   | Earned golds in the last 5 minutes    |
| Level          | INTEGER   | Player level                          |
| CS             | INTEGER   | Player creep score                    |
| Health         | INTEGER   | Player health points                  |
| MaxHealth      | INTEGER   | Player maximum health points          |
| KP             | REAL      | Player kill participation             |
| WardsPlaced    | INTEGER   | Number of wards placed                |
| WardsDestroyed | INTEGER   | Numbre of wards destroyed             |
| AD             | INTEGER   | Player attack damage                  |
| AP             | INTEGER   | Player ability power                  |
| Crit           | REAL      | Player critical strike chance         |
| AS             | INTEGER   | Player attack speed                   |
| LifeSteal      | INTEGER   | Player life steal                     |
| MR             | INTEGER   | Player magic resistance               |
| Armor          | INTEGER   | Player armor                          |
| Tenacity       | INTEGER   | Player tenacity                       |
| DamageShare    | REAL      | Player team damage share              |
