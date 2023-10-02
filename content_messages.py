import os

greeting = '''
<b>👋 Добро пожаловать в онлайн магазин luxurywatch_uz</b>

<i>ℹ️ Что-бы сделать заказ, нажмите кнопку ниже</i>
'''

info = '''
Часы и аксессуары | Узбекистан
🔸Онлайн магазин
🔸Часы наивысшего уровня
🔸Бесплатная доставка по Узбекистану
🔸Обмен возврат нет
📱Контакты для заказа +998999895777
https://t.me/luxurywatch_uz1
https://www.instagram.com/luxurywatch_uz/
'''

howto_order = """
<b>🔗 Что-бы выбрать товар, отправьте ссылку Инстаграм поста из канала <a href="https://www.instagram.com/luxurywatch_uz/">luxurywatch_uz</a></b>

<i>ℹ️ например:</i>
https://www.instagram.com/reel/CxDFNaksQ6a/?utm_source=ig_web_button_share_sheet&igshid=MzRlODBiNWFlZA==
"""

make_order_button = "Сделать заказ 🛒"
info_button = "Информация про магазин ℹ️"

yes_button = "да"
cannel_button = "отменить заказ"

order_canceled = "<b>Заказ отменён ❌</b>"


regions = [None] * 14
regions[0] = 'Tashkent'
regions[1] = 'Tashkent Region'
regions[2] = 'Andijan Region'
regions[3] = 'Bukhara Region'
regions[4] = 'Jizzakh Region'
regions[5] = 'Kashkadarya Region'
regions[6] = 'Namangan Region'
regions[7] = 'Navoiy Region'
regions[8] = 'Samarkand Region'
regions[9] = 'Surkhandarya Region'
regions[10] = 'Syrdarya Region'
regions[11] = 'Fergana Region'
regions[12] = 'Khorezm Region'
regions[13] = 'Republic of Karakalpakstan'

bts_offices_path = os.path.abspath(".") + r"/bts-offices/"