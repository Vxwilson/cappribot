from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyperclip


def inch_to_cm(inch):
    return round(inch * 2.54, 1)


# append hashtag based on globally defined hashtags and special tags (specific use case)
def append_hashtag(output, hashtags, specialtags, staglist):
    dots = ''
    for i in range(8):
        dots += ".\n"
    output = output.strip() + '\n' + dots + hashtags.strip()
    for number in staglist:
        output += " " + specialtags[number - 1].strip()
    return output


class Handler(object):
    def __init__(self):
        # include path to chromedriver here
        self.chromepath = "E:/Users/Documents/UsefulExes/chromedriver.exe"
        self.edgepath = "Source/Resources/Drivers/msedgedriver92.exe"
        self.lingo_text_field = None
        self.textfield = None
        self.messenger = None

    def text_sender(self, string, times=1):
        split_string = string.strip().split("$$")
        for i in range(times):
            for s in enumerate(split_string):
                self.send_to_messenger(s[1].replace("<>", f"{i+1}"))

    def yongie_text_parser(self, strin, times=1):
        self.lingo_text_field = webdriver.Edge(self.edgepath)
        self.lingo_text_field.set_window_position(-10000, 0)
        self.lingo_text_field.get('https://lingojam.com/FontsForInstagram')

        try:
            self.textfield = self.lingo_text_field.find_element_by_id('english-text')
        except:
            print("no element found")

        hashtags = ''
        specialtags = ''
        for id, para in enumerate(strin.strip().split("$$")):
            if id == 0:
                splittedtag = para.strip().split("&")
                for idx, stag in enumerate(splittedtag):
                    if idx == 0:
                        for id, tag in enumerate(stag.strip().split("#")):
                            if id == 0:
                                continue
                            hashtags += "#" + tag
                        continue
                    specialtags += "#" + stag
                continue
            output = ''
            splittedstring = para.strip().split("\n$")
            staglist = []
            for idx, splitstr in enumerate(splittedstring):
                spllistr = splitstr.split('\n\n')
                for i, strin in enumerate(spllistr):
                    if strin.isspace():
                        continue
                    if len(strin) == 0:
                        continue
                    if i == 0:
                        strin += '\n(Swipe left for more details)'
                        output += self.get_modified_text(1, strin, True)
                    elif i == 1:
                        sentences = strin.strip().split('\n')
                        tempstring = ''
                        for a, sen in enumerate(sentences):
                            if a == 0:
                                tempstring = 'Brand: ' + sen
                            elif a == 1:
                                tempstring += '\nSize: ' + sen
                            elif a == 2:
                                tempstring += '\nCondition: ' + sen
                            elif a == 3:
                                tempstring += '\nPrice: ' + sen
                        output += '\n' + self.get_modified_text(2, tempstring, True)

                    if i is len(spllistr) - 1:  # measurements; weird situation, i is 0 in the last iteration
                        newstring = ""
                        stagspllit = strin.strip().split("&")
                        for ii, stagstr in enumerate(stagspllit):
                            if ii == 0:
                                continue
                            staglist += [int(stagstr[0])]
                            strin = strin.strip()[:-2]
                        sentences = strin.strip().split('\n')
                        for a, sen in enumerate(sentences):
                            bust = False
                            val = 0.0
                            for t in sen.split():
                                if t == "Bust" or t == "Waist" or t == "Hips":
                                    bust = True
                                try:
                                    val = (float(t))
                                    break
                                except ValueError:
                                    pass
                            # print(f"value: {val}")
                            newstring += sen.split()[0] + ": " + str(val) + "\"" + ("flat" if bust else "") + "/" + str(
                                inch_to_cm(val)) + "cm" + '\n'

                        newstring = 'Measurements: \n' + newstring.strip() + \
                                    '\nModel reference: \nHeight: 162cm \n\nDm to order or if you have any inquiries,' \
                                    ' we won\'t bite!'
                        # newstring = 'Measurements: \n' + self.preappender(newstring) + newstring.strip() +
                        # '\nModel reference: \nHeight: 162cm \n\nDm to order or if you have any inquiries,
                        # we won\'t bite!'
                        output = output + '\n' + self.get_modified_text(2, newstring, True)
            print("sending", id)
            output = append_hashtag(output, hashtags, specialtags.strip().split(' '), staglist)
            # print(output)
            for i in range(times):
                output = output.replace("<>", f"<{i + 1}>")
                self.send_to_messenger(output)
        self.lingo_text_field.close()

    def get_modified_text(self, index, strin, autoadd=False):
        if autoadd is True:
            strin = str(index) + strin
        self.textfield.clear()
        self.textfield.send_keys(strin)
        time.sleep(0.4)
        # sentences = browser.find_element_by_id('ghetto-text').get_attribute('value').split('\n')
        # sentences = browser.find_element_by_id('ghetto-text').get_attribute('value').split(str(index))
        sentences = None
        if index == 1:
            sentences = self.lingo_text_field.find_element_by_id('ghetto-text').get_attribute('value').split('𝟏', 1)
            sentences = sentences[1].split('𝟭', 1)
        elif index == 2:
            sentences = self.lingo_text_field.find_element_by_id('ghetto-text').get_attribute('value').split('𝟮', 1)
            sentences = sentences[1].split('2', 1)
        return sentences[0].strip()

    # actual action of sending messages to facebook messenger
    def send_to_messenger(self, finishedstr):
        pyperclip.copy(finishedstr)
        self.messenger.find_element_by_xpath("//*[@data-editor]").click()

        # for i in range(times):
        actions = ActionChains(self.messenger)
        actions.key_down(Keys.CONTROL)
        actions.send_keys('a')
        actions.send_keys('v')
        actions.perform()
        actions.key_up(Keys.CONTROL)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    # opens scrapper and select handling method based on [option] parameter
    def handle_message(self, text, emailtext, passwordtext, linktext, option="yongie", iteration=1):
        self.messenger = webdriver.Edge(self.edgepath)
        link_str = 'https://www.messenger.com/t/' + linktext
        self.messenger.set_window_position(-10000, 0)
        self.messenger.get(link_str)
        try:
            time.sleep(0.9)
            email = self.messenger.find_element_by_id('email')
            email.send_keys(emailtext)
            password = self.messenger.find_element_by_id('pass')
            password.send_keys(passwordtext)
            button = self.messenger.find_element_by_id('loginbutton')
            button.click()
            time.sleep(4.5)
        except:
            print("messenger no element found")

        if option == 'Plain text':
            self.text_sender(text, iteration)
        elif option == 'Caption':
            self.yongie_text_parser(text, iteration)

        time.sleep(0.5)
        self.messenger.close()
        return True
