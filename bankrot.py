import argparse
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
# display.start()

from transliterate import translit, get_available_language_codes


URL = 'https://bankrot.fedresurs.ru/Messages.aspx?attempt=1'
SEARCH = 'ctl00_cphBody_ibMessagesSearch'
SELECT = 'ctl00_cphBody_ucRegion_ddlBoundList'

TRANSLIT = 'ru'


# driver.find_element_by_name('ctl00$cphBody$cldrBeginDate$tbSelectedDate').clear()

# ctl00$cphBody$cldrBeginDate$tbSelectedDate 
# ctl00$cphBody$cldrEndDate$tbSelectedDate

# ctl00_cphBody_trINN


# driver.find_element_by_name('ctl00$cphBody$cldrBeginDate$tbSelectedDate').send_keys('05.09.2017')
# driver.find_element_by_id('ctl00_cphBody_ibMessagesSearch').click()

class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Использование: '

        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)


class Crawler:
	def __init__(self, ndfile=None):
		self.br = webdriver.Chrome()
		self._start = 1
		self._stop = 88
		self._language = 'ru'
		self._new = None
		self._ndfile = ndfile


	def _translit(self, text):
		en = translit(text, self._language, reversed=True)
		return en

	def check(self):
		if os.path.isfile(self._ndfile):
			self._new = False
		else:
			self._new = True


	def _write(self):
		pass


	def build(self):
		pass


	def _dnjson(self, text):
		pass

	def parser(self):
		self.br.get(URL)
		select = Select(self.br.find_element_by_id(SELECT))
		
		for _ in range(self._start, self._stop):
			select.select_by_index(_)
			time.sleep(1)
			print(select.first_selected_option.text, '\t', _, '\t', self._translit(
				select.first_selected_option.text))

			self.br.find_element_by_id(SEARCH).click()
			self.br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			paginate = self.br.find_elements_by_css_selector('tr.pager td')
			paginate_len = len(paginate)

			for num, pag in enumerate(paginate):
				self.br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(1)
				try:
					self.br.find_elements_by_css_selector('tr.pager td')[num+1].click()
				except Exception:
					self.br.execute_script("scrollBy(0,250);")
					break
				time.sleep(3)
				self.br.execute_script("scrollBy(0, -1000);")
				time.sleep(2)
				break


	def go(self):
		time.sleep(5)
		self.parser()
		self.br.close()



def do_go():
	arg_parser = argparse.ArgumentParser(
		description='Парсер',
		formatter_class=CapitalisedHelpFormatter,
		add_help=False)
	arg_parser.add_argument(
		'-o', '--output', default='file.ndjson',
		help='Файл для сохранения', type=str)
	arg_parser.add_argument(
		'-s', '--start', default=False,
		help='Парсим все данные которые есть на сервере', type=bool)
	arg_parser.add_argument(
		'-a', '--add', default=True,
		help='Парсим данные которые обновились за сутки', type=bool)
	arg_parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
        help='Показать это справочное сообщение и выйти.')
	arg_parser._positionals.title = 'Позиционные аргументы'
	arg_parser._optionals.title = 'Аргументы'
	args = arg_parser.parse_args()
	return args


if __name__ == '__main__':
	print("НАЧАЛО РАБОТЫ")
	do_go()
	craw = Crawler()
	craw.go()




# select = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "//select[@class='select' and @name='fruits']"))))
