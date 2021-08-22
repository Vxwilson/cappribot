from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyperclip
import Source.Texts.text


def text_parser(str):
    for splitstr in str.split('$'):
        if splitstr.isspace():
            continue
        if len(splitstr) == 0:
            continue
        i = 0
        for c in splitstr:
            if c.isdigit() is False:
                break
            i += 1
        sum = 0
        for a in range(i):
            sum += int(splitstr[a])*(10**(i-a-1))
        get_modified_text(sum, splitstr)


def simple_text_parser(strin, times=1):
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
                    output += get_modified_text(1, strin, True)
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
                    output += '\n' + get_modified_text(2, tempstring, True)

                if i is len(spllistr)-1:  # measurements; weird situation, i is 0 in the last iteration
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
                        newstring += sen.split()[0] + ": " + str(val) + "\"" + ("flat" if bust else "") + "/" + str(inch_to_cm(val)) + "cm" + '\n'
                    newstring = 'Measurements: \n' + preappender(newstring)
                    output = output + '\n' + get_modified_text(2, newstring, True)
        print("sending", id)
        output = append_hashtag(output, hashtags, specialtags.strip().split(' '), staglist)
        # print(output)
        for i in range(times):
            send_to_messenger(output)


def standard_text_parser(strin, times = 1):

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
            spllistr = splitstr.split('$')
            for i, strin in enumerate(spllistr):

                if strin.isspace():
                    continue
                if len(strin) == 0:
                    continue
                if strin[0].isdigit() is False:
                    break
                if i == 0:  # weird situation, i is 0 in the last iteration
                    stagspllit = strin.strip().split("&")
                    for ii, stagstr in enumerate(stagspllit):
                        if ii == 0:
                            continue
                        staglist += [int(stagstr[0])]
                        strin = strin.strip()[:-2]
                    strin = preappender(strin)
                sum = int(strin[0])

                output = output + get_modified_text(sum, strin)

                for a in range(strin.count('\n') - 1):  # add lines to the end of a part
                    output += '\n'
            output += '\n'
        output = append_hashtag(output, hashtags, specialtags.strip().split(' '), staglist)
        for i in range(times):
            send_to_messenger(output)


def preappender(strin):
    sentence = '\nModel reference: \nHeight: 162cm \n\nDm to order or if you have any inquiries, we won\'t bite!'
    return strin.strip() + sentence


def append_hashtag(output, hashtags, specialtags, staglist):
    dots = ''
    for i in range(8):
        dots += ".\n"
    output = output.strip() + '\n' + dots + hashtags.strip()
    for number in staglist:
        output += " " + specialtags[number-1].strip()
    return output


def get_modified_text(index, strin, autoadd=False):
    if autoadd is True:
        strin = str(index) + strin
    textfield.clear()
    textfield.send_keys(strin)
    time.sleep(0.4)
    # sentences = browser.find_element_by_id('ghetto-text').get_attribute('value').split('\n')
    # sentences = browser.find_element_by_id('ghetto-text').get_attribute('value').split(str(index))

    if index == 1:
        sentences = instatext.find_element_by_id('ghetto-text').get_attribute('value').split('𝟏', 1)
        sentences = sentences[1].split('𝟭', 1)
    elif index == 2:
        sentences = instatext.find_element_by_id('ghetto-text').get_attribute('value').split('𝟮', 1)
        sentences = sentences[1].split('2', 1)
    return sentences[0].strip()


def send_to_messenger(finishedstr):
    pyperclip.copy(finishedstr)
    messenger.find_element_by_xpath("//*[@data-editor]").click()

    # for i in range(times):
    actions = ActionChains(messenger)
    actions.key_down(Keys.CONTROL)
    actions.send_keys('a')
    actions.send_keys('v')
    actions.perform()
    actions.key_up(Keys.CONTROL)
    actions.send_keys(Keys.ENTER)
    actions.perform()


def inch_to_cm(inch):
    return round(inch * 2.54, 1)

if __name__ == '__main__':

    #include path to chromedriver here
    chromepath = "E:/Users/Documents/UsefulExes/chromedriver.exe"
    edgepath = "E:/Users/Documents/UsefulExes/msedgedriver92.exe"
    # instatext = webdriver.Chrome(chromepath)
    instatext = webdriver.Edge(edgepath)
    textfield = ''
    instatext.get('https://lingojam.com/FontsForInstagram')
    try:
        textfield = instatext.find_element_by_id('english-text')
    except:
        print("no element found");
    # messenger = webdriver.Chrome(path)
    messenger = webdriver.Edge(edgepath)
    # messenger.get('https://www.messenger.com/t/100014533062209')  #yongie
    messenger.get('https://www.messenger.com/t/100000178957922')  #kreg
    # messenger.get('https://www.messenger.com/t/100000244705887')  #jon

    try:
        time.sleep(0.5)
        email = messenger.find_element_by_id('email')
        email.send_keys('veixhen@hotmail.com')
        password = messenger.find_element_by_id('pass')
        password.send_keys('snorlaxmangAli01')
        button = messenger.find_element_by_id('loginbutton')
        button.click()
        time.sleep(5)

    except:
        print("messenger no element found")

    # standard_text_parser(Texts.text.quotey)
    simple_text_parser(Source.Texts.text.quotey)

    time.sleep(0.5)
    instatext.close()
    messenger.close()

