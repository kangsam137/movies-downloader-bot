import requests
from bs4 import BeautifulSoup
import telegram 

# Telegram Bot credentials
bot_token = "6041460703:AAEZPbFgnImdBhslrns2MBfUIu4hAuvdl68"
chat_id = "1168046950" 

# Function to send a message to the Telegram bot
def send_message(message):
    bot = telegram.Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text=message) 

# Function to upload a movie to the Telegram bot
def upload_movie(movie_details):
    bot = telegram.Bot(token=bot_token)
    caption = f"{movie_details['title']}\n\n"
    for title, link in movie_details['links'].items():
        caption += f"{title}: {link}\n"
    bot.send_message(chat_id=chat_id, text=caption) 

# Function to search for movies
def search_movies(query):
    movies_list = []
    website = BeautifulSoup(requests.get(f"https://185.53.88.104/?s={query.replace(' ', '+')}", verify=False).text,
                            "html.parser")
    movies = website.find_all("a", {'class': 'ml-mask jt'})
    for movie in movies:
        movie_details = {}
        if movie:
            movie_details["id"] = f"link{movies.index(movie)}"
            movie_details["title"] = movie.find("span", {'class': 'mli-info'}).text
            movie_details["url"] = movie['href']
            movies_list.append(movie_details)
    return movies_list 

# Function to get movie details
def get_movie(query):
    movie_details = {}
    movie_page_link = BeautifulSoup(requests.get(url_list[query], verify=True).text, "html.parser")
    if movie_page_link:
        title = movie_page_link.find("div", {'class': 'mvic-desc'}).h3.text
        movie_details["title"] = title
        img = movie_page_link.find("div", {'class': 'mvic-thumb'})['data-bg']
        movie_details["img"] = img
        links = movie_page_link.find_all("a", {'rel': 'noopener', 'data-wpel-link': 'internal'})
        final_links = {}
        for i in links:
            final_links[i.text] = i['href']
        movie_details["links"] = final_links
    return movie_details 

# Main function
def main():
    query = input("Enter movie search query: ")
    movies_list = search_movies(query)
    if movies_list:
        print("Found movies:")
        for movie in movies_list:
            print(f"{movie['id']}: {movie['title']}")
        movie_id = input("Enter the movie ID to get details: ")
        movie_details = get_movie(movie_id)
        if movie_details:
            upload_movie(movie_details)
        else:
            print("Invalid movie ID.")
    else:
        print("No movies found.") 

if __name__ == '__main__':
    main()