from urllib.request import urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import youtube_dl
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def get_video_url(query):
    query = {'search_query': '{}'.format(query)}
    url = 'https://www.youtube.com/results?' + urlencode(query)
    response = urlopen(url)
    soup = BeautifulSoup(response.read().decode(), 'html.parser')
    for tag in soup.find_all('a', {'rel': 'spf-prefetch'}):
        video_url = 'https://youtube.com' + tag['href']
        return video_url


def start(bot, update):
    """
    Send a message when command /start is issued.
    """
    update.message.reply_text('Hey there!')


def help(bot, update):
    """
    Send a help  information when /help is issued.
    """
    update.message.reply_text("Commands are \start\n \help\n \download song_name\n")


def handle_bad(bot, update):
    """
    Handle the bad messages in commands.
    """
    update.message.reply_text('Didn\'t understand that')


def download(bot, update, video_url):
    """
    Donloads a music file in mp3 format when '/download query_start' is issued.
    """
    query_str = update.message.text
    video_url = get_video_url(query_str)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


def main():
    """
    Start the bot.
    """
    updater = Updater('484919626:AAHZbvtIURPJbG-sRnRVfP60y2Hkyl1hNQ4')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('download', download))
    bad_message = MessageHandler(Filters.text, handle_bad)
    dp.add_handler(bad_message)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

