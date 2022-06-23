import requests, random, telebot, string

bot = telebot.TeleBot('your bot token')  # token

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(
    word_site)  # We make a request to a site with a list of words.
words = response.text.split()
word = ''
wordHidden = []
attempt = 0
fail = []


def newWord():
    global word, wordHidden, attempt, fail
    word = words[random.randint(
        0, len(words))].lower()  # Saves a random word from a variable [words]
    wordHidden = ['-'] * len(word)
    attempt = 0
    fail = []


newWord()


@bot.message_handler(content_types=['text'])
def vis(message):
    global attempt
    messageText = message.text.lower()
    if len(
            messageText
    ) == 1 and messageText in string.ascii_lowercase:  # Checking the entered letter and if it is in the word, then the "-" is replaced
        if word.find(messageText) != -1:
            for i in range(len(word)):
                if messageText == word[i]:
                    if word[i] in wordHidden:
                        bot.send_message(
                            message.from_user.id,
                            f'😡 Re-entering a letter: [{messageText}] 😡')
                    else:
                        wordHidden[i] = word[i]
        else:

            if messageText in fail:
                bot.send_message(message.from_user.id,
                                 f'😡 Re-entering a letter: [{messageText}] 😡')
            else:
                attempt += 1
                fail.append(messageText)

        if '-' not in wordHidden:
            bot.send_message(
                message.from_user.id,
                f'⭐️ Congratulations, you guessed the word [{"".join(wordHidden)}] and saved the man! ⭐️\n📬 New word \n➡️ Enter 1 letter'
            )
            newWord()
        elif attempt == 8:
            bot.send_message(
                message.from_user.id,
                f'☠️ You failed to guess the word [{word}] YOU LOST! ☠️\n📬 New word \n➡️ Enter 1 letter'
            )
            newWord()
        else:
            bot.send_message(
                message.from_user.id,
                f'Word: {"".join(wordHidden)} \nWord length: {len(word)} \nAttempts: {8 - attempt}'
            )

    elif messageText == '/help':
        bot.send_message(message.from_user.id, '➡️ Enter 1 letter')
    else:
        bot.send_message(message.from_user.id, '❌  Error 404 /help  ❌')


bot.polling(
    none_stop=True, interval=1
)  # This function constantly checks whether the user has sent a message, if it is, then the code above processes it.
