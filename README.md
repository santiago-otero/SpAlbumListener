# SpAlbumListener
![Captura de pantalla 2024-03-19 104330](https://github.com/santiago-otero/SpAlbumListener/assets/142631458/68299e1a-7f55-41e8-9fac-54932f6afced)

# Video Demo:
https://youtu.be/DaGPmyPFyhs
   
# Description:
Hello everyone!, In this project I created a website using Flask. Flask is a python framework for creating web aplications. I crated this website for the presentation of my final project of the CS50´s Introduction to Programming with Python. 
    
# App ussage:
 The application that i created is for looking up different albums of whatever artist in the world by interacting with the Spotify 
 API to make the searching and displaying of albums and tracks. You can type whatever artist name and my program will return the 
 lastest album they have made. In addition you can swich trough 4 extra albums the artist has in the Spotify plataform in case the 
 artist launched more albums and you can display every track that the album contains. 
    
# Program Logic and understanding: 
    When it comes to using the spotify API for launching an aplication you need to log in in spotify 
    for developers and create an app wich tells you about the amount of users that used your program 
    and requested data. Once completed, our app will handle back some relevant info such as client id, 
    client secret and your redirect url thoose wich you will later need to authenticate. 

    By using teh flask Framework, first i check for a valid token by using the sp.oauth method once 
    loged in. Then I store the Authentication token in my program session which is neccesary for later 
    API request. once obtained the Authentication token you can request the Spotify APi for all the 
    data needed. Firstly i requested for the artist inputed in the html form object JSON. This object 
    JSON which the API return contains multiple artist data such as the id and name. Those are the 
    values that I use in my program.Important: the authentication token has an expirancy of one hour

    By having the artist unique id you can now request for the specific artist albums. that is what my 
    get_artist_albums function does. This function returns a list with each album uris from the artist 
    id specified. Once having the urls_list, i pass the value to the main.html tempalte identified as 
    album_uris and i create an Spotify embed for the initial album wich is the first uri of the list.

    Finally, i have created a button with the function changeAlbum() wich replaces the initial uri 
    with the following index one in the list album_uris. once reached the last uri, if the button 
    is pressed the loop repeats form the first album. 

    The logout button clears the session and redirects the user to the main page. Once there if the 
    validate token does not exist, then it redirects the user to the login. 

# Necesary instalations:
    pip install Flask
    pip install requests
    pip install spotipy
    pip install python-dotenv

# Other Projects: 

# Rock-paper-scisors:
   https://github.com/santiago-otero/Rock-Paper-Scissors

# Home page model:
   https://github.com/santiago-otero/Odinwebpage
    
