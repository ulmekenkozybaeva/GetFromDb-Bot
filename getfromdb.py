import telebot
import mysql.connector

bot = telebot.TeleBot('token')

db_config = {
    'host': 'your host',
    'user': 'your username',
    'password': 'your password',
    'database': 'database name'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Select the manufacturer:", reply_markup=get_manufacturers_markup())

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data in ['Apple', 'Samsung']:
        manufacturer = call.data
        products = get_products_by_manufacturer(manufacturer)
        if products:
            product_info = "\n".join(products)
            bot.send_message(call.message.chat.id, f"Product info: {manufacturer}:\n{product_info}")
        else:
            bot.send_message(call.message.chat.id, f"There is no information about {manufacturer}")
    else:
        bot.send_message(call.message.chat.id, "Select the manufacturer:", reply_markup=get_manufacturers_markup())

def get_manufacturers_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton('Apple', callback_data='Apple'),
               telebot.types.InlineKeyboardButton('Samsung', callback_data='Samsung'))
    return markup

# replace the 'database' to your database name
def get_products_by_manufacturer(manufacturer):
    query = f"SELECT * FROM database WHERE Manufacturer = '{manufacturer}'"
    cursor.execute(query)
    result = cursor.fetchall()
    products_info = []
    for product in result:
        products_info.append(f"ProductName: {product[1]}, \n Model: {product[2]}, \n Price: {product[4]}, \n Img: '{product[5]}'")
    return products_info


bot.polling(none_stop=True)
