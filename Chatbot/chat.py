import random
import json
import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import wikipedia
driver = webdriver.Chrome(ChromeDriverManager().install())
class ChatBot():
    def __init__(self):
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')

        self.driver=driver
        with open('intents.json', 'r') as json_data:
            self.intents = json.load(json_data)

        FILE = "data.pth"
        data = torch.load(FILE)

        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]

        self.all_words = data['all_words']
        self.tags = data['tags']

        model_state = data["model_state"]

        self.model = NeuralNet(input_size, hidden_size,
                               output_size).to(self.device)
        self.model.load_state_dict(model_state)
        self.model.eval()

        ''' 
        option = input("Hey, Do you want to name your bot?(Y/N)\n")
        if (option.lower() == 'yes' or option.lower() == 'y'):
            name = input("Enter Bot name\n")

        if (option.lower() == 'no' or option.lower() == 'n'):
            name = 'Sam'
        '''

        print("Let's chat! (type 'quit' to exit)")

    def get_response(self, sentences):
        print(type(sentences))
        sentence = tokenize(sentences)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in self.intents['intents']:
                if tag == intent["tag"]:
                    return (f"{random.choice(intent['responses'])}")
        else:
            return  self.__takeCommand(sentences)

    def __takeCommand(self, query):
                url = 'https://www.google.com/search?channel=crow2&client=firefox-b-d&q='
                l = query.strip().lower().split()
                if ('who' in l[0]) or ('what' in l[0]):
                    print(l[0])
                    return wikipedia.summary(query.replace(l[0],'').lower(), sentences=2)
                elif "weather" in query:
                    res = self.__google_weather(url + query)
                    response = '\n'.join(res)
                    return response

                else:  # 'quora' in query:
                    try:
                        link = self.__get_browser(url + query + ' quora')
                        response = self.__quora_answer(link)
                        return random.choice(response)
                    except:
                        url = 'https://www.reddit.com/search/?q='
                        # word=query+str(' reddit')
                        url = url + query
                        link = self.__get_browser(url)
                        a = self.driver.find_element_by_xpath(
                            "//a[@class='SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE']")
                        u = a.get_attribute('href')
                        self.driver.get(u)
                        a = self.driver.find_elements_by_xpath(
                            "//div[@class='_292iotee39Lmt0MkQZ2hPV RichTextJSON-root']")
                        # t=[i.text for i in a]
                        return a[1].text

    def __get_browser(self, url):
        self.driver.get(url)
        div = self.driver.find_elements_by_xpath("//div[@class='yuRUbf']")
        for d in div:
            a = d.find_element_by_tag_name("a")
            link = a.get_attribute('href')
            if 'answers.yahoo' in link:
                # print(link)
                return (link)
            elif 'quora.com' in link:
                # print(link)
                return link

    def __reddit_answer(self, url):
        t = []
        self.driver.get(url)
        button = self.driver.find_element_by_xpath(
            "//button[@class='j9NixHqtN2j8SKHcdJ0om _2iuoyPiKHN3kfOoeIQalDT _10BQ7pjWbeYP63SAPNS8Ts HNozj_dKjQZ59ZsfEegz8 _2nelDm85zKKmuD94NequP0']")
        button.click()
        for i in range(5):
            screen_height = self.driver.execute_script("return window.screen.height;")
            self.driver.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        b = self.driver.find_elements_by_xpath("//div[@data-test-id='comment' and @class='_3cjCphgls6DH-irkVaA0GM']")
        for j in b:
            t.append(j.text)
        return t

    def __google_weather(self, url):
        res = []
        # url='https://www.google.com/search?channel=crow2&client=firefox-b-d&q='
        # url=url +str(query)
        self.driver.get(url)
        taks = self.driver.find_element_by_xpath("//span[@id='wob_dc']").text
        # print(taks)
        res.append(taks)
        jaw = self.driver.find_elements_by_xpath("//div[@class='vk_gy vk_sh']")
        for j in jaw:
            div = j.find_elements_by_tag_name("div")
            for d in div[:3]:
                # print(j.find_element_by_tag_name('div').text)
                # print(d.text)
                res.append(d.text)
        harr = self.driver.find_element_by_xpath("//div[@class='vk_bk TylWce']").text
        harr = harr + str('°C')
        res.append(harr)
        return res

    def __quora_answer(self, url):
        t = []
        self.driver.get(url)
        for i in range(5):
            screen_height = self.driver.execute_script("return window.screen.height;")
            self.driver.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        b = self.driver.find_elements_by_xpath(
            "//div[@class='q-relative spacing_log_answer_content puppeteer_test_answer_content']")
        for i in b:
            try:
                i.click()
                t.append(i.text)
            except:
                pass
        return t


''' 
bot = ChatBot()
a = 0
while a != 1:
    s = input("input  ")

    print(bot.get_response(s))
 '''
