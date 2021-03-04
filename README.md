## Aineopintojen harjoitustyö (Helsingin yliopisto):
# Tietokantasovellus, kevät 2021

## Yleistä
Kuvakilpailun äänestyssovellus

Sovelluksen avulla valokuvausseura ym. voi arvostella kuvakilpailujensa kuvia. Sovelluksella on pääkäyttäjä, joka lataa kuvat sovellukseen. Sovellukseen pääsee sisälle myös vierailijana, mutta tällöin kuvia voi vain katsella. Äänestämiseen edellytetään kirjautumista.

Sovellusta voi testata Herokussa:
https://valokuvan-aanestys.herokuapp.com/

## Ohjeet
Sovelluksessa on kolme käyttäjätasoa; vierailija, rekisteröitynyt käyttäjä sekä pääkäyttäjä.
Huom! Jos käytät sovellusta locaalisti omalla koneellasi, perusta pääkäyttäjä tietokantaan ensimmäisenä,
näin käyttäjätasot toimivat halutulla tavalla.

Vierailija näkee vain etusivun sekä sivun jossa voi katsoa kilpailuun ladattuja kuvia (Katselu).

Rekisteröitynyt käyttäjä voi tämän lisäksi myös suorittaa äänestyksen. Rekisteröitymiseen pääsee etusivulta. Voit halutessasi
rekisteröityä sovellukseen ja suorittaa äänestyksen. Äänestyssivulla on ohjeet äänestykseen liittyen. Äänestyksen voi
suorittaa vain kerran per käyttäjä.

Pääkäyttäjän tehtävä on ladata kuvat äänestykseen (Lataaminen) jossa kuvalle annetaan myös kuvaajan nimi. Kuvalle on 
määritelty myös maksimikoko. Kuvia voi myös poistaa sovelluksen tietokannasta (Muokkaa). Samalla poistuu myös kyseisen
kuvan kuvaaja sekä kuvalle annetut pisteet. Tästä ohjeet kyseisellä sivulla. Muokkaa-sivulla voi myös nollata
äänestyksen pisteet. Samalla myös nollataan tietokanta, jossa pidetään kirjaa äänestäneistä, näin jokainen rekistöitynyt
käyttäjä voi suorittaa äänestyksen uudelleen. Pääkäyttäjä näkee myös äänestyksen tulokset (Tulokset). Sovelluksen tarkoituksena 
on toimia vain äänestysalustana ja lopulliset tulokset julkaistaan muissa foorumeissa.

Ulkoasu on muokattu Bootstrap:in avulla. Suuria muutoksia oletusulkoasuun ei ole tehty.

Pääkäyttäjän tunnukset saa minulta kurssin Telegram-kanavan kautta pyytämällä niitä yksityisviestillä.

## Sovelluksen kehitysvaihe
Sovellus sisältää kaikki sille aluperin suunnitellut ominaisuudet. Viimeisenä lisäyksenä on tehty
äänestyksen nollaaminen Muokkaa-sivulle.



