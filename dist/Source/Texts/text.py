august_27 = """
#thecatthrifts #thrifting #preloved #secondhand #thriftmalaysia #onlinethriftstore #thriftstore #stylewithus #thriftwithusthursdays #thriftstorefinds #eighthdrop #rainbow #tops #shorts #lowrise #unique #vintage #retro #valuebuy #slowfashionisthewaytogo #sustainablefashion #sustainability #supportsmallbusiness #smallbusiness #staysafestayhome #thecatthriftsavailable
&thecatthriftsavailabletop &thecatthriftsavailablebottom &thecatthriftsavailabledress &thecatthriftsavailablejacket

$$
Red long sleeve shirt

-
fits XS-S
7/10
RM13 (includes postage)

Shoulder 14
Sleeves 20
Bust 13.5
Length 19
&1
$$
Red skirt with safety pants

-
fits M-small L
8/10 
RM13 (includes postage)

Waist 15
Hips 19.5
Length 13.5
&2
$$
Red skort

-
tagged M (fits XS-S)
9/10
RM15 (includes postage)

Waist 13
Hips 20.5
Length 12.5
&2
$$
Red top

-
fits M-small L 
7/10
RM15 (includes postage)

Sleeves 10.5
Length 21.5
&1
$$
Red top

-
tagged S 
6/10
RM13 (includes postage)

Shoulder 14.5
Bust 14
Length 21.5
&1
$$
Pink top 

PADINI
tagged S
6/10
RM13 (includes postage)

Shoulder
Sleeves
Bust 
Length 
&1
$$
Orange top

-
tagged S
7/10 
RM13 (includes postage)

Shoulder 14.5
Bust 14
Length 21.5
&1
$$
Low rise shorts

-
fits XS-S
6/10
RM13 (includes postage)

Waist 15
Hips 18.5
Length 9.5
&2
$$
Mint green t-shirt

-
fits M-small L (ask)
9/10
RM15 (includes postage)

Shoulder 18
Sleeves 6
Bust 19
Length 24
&1
$$
Green top

-
fits S
9/10
RM16 (includes postage)

Shoulder 16
Sleeves 9
Bust 16
Length 23
&1
$$
Green graphic tee

Scribble tees by Old Skool
fits S-M
8/10
RM18 (includes postage)

Shoulder 13
Sleeves 5
Bust 15.5
Length 23
&1
$$
Green cropped top

-
fits XS
9/10
RM15 (includes postage)

Shoulder 13.5
Sleeves 4.5
Bust 15.5
Length 13
&1"""

optimalquote = """
#thecatthrifts #thrifting #preloved #secondhand #thriftmalaysia #onlinethriftstore #thriftstore #stylewithus #thriftwithusthursdays #thriftstorefinds #sixthdrop #camisoles #y2kvibes #tops #dresses #jackets #skirts #unique #vintage #retro #valuebuy #slowfashionisthewaytogo #sustainablefashion #sustainability #supportsmallbusiness #smallbusiness #staysafestayhome #thecatthriftsavailable 
&thecatthriftsavailabletop &thecatthriftsavailablebottom &thecatthriftsavailabledress &thecatthriftsavailablejacket

$$
Black tank top with polka dots

-
fits S
5/10
RM15 (includes postage)

Bust 14.5
Length 23.5
&1

$$
Black tank top with shrimps

-
fits S
12/10
RM15 (includes postage)

Shoulder 20
Bust 16
Length 24
&2
"""

lovequote = """
    """

excode = """

#
# def text_parser(str):
#     for splitstr in str.split('$'):
#         if splitstr.isspace():
#             continue
#         if len(splitstr) == 0:
#             continue
#         i = 0
#         for c in splitstr:
#             if c.isdigit() is False:
#                 break
#             i += 1
#         sum = 0
#         for a in range(i):
#             sum += int(splitstr[a])*(10**(i-a-1))
#         get_modified_text(sum, splitstr)
#
#
# def simple_text_parser(strin, times=1):
#     hashtags = ''
#     specialtags = ''
#     for id, para in enumerate(strin.strip().split("$$")):
#         if id == 0:
#             splittedtag = para.strip().split("&")
#             for idx, stag in enumerate(splittedtag):
#                 if idx == 0:
#                     for id, tag in enumerate(stag.strip().split("#")):
#                         if id == 0:
#                             continue
#                         hashtags += "#" + tag
#                     continue
#                 specialtags += "#" + stag
#             continue
#         output = ''
#         splittedstring = para.strip().split("\n$")
#         staglist = []
#         for idx, splitstr in enumerate(splittedstring):
#             spllistr = splitstr.split('\n\n')
#             for i, strin in enumerate(spllistr):
#                 if strin.isspace():
#                     continue
#                 if len(strin) == 0:
#                     continue
#                 if i == 0:
#                     strin += '\n(Swipe left for more details)'
#                     output += get_modified_text(1, strin, True)
#                 elif i == 1:
#                     sentences = strin.strip().split('\n')
#                     tempstring = ''
#                     for a, sen in enumerate(sentences):
#                         if a == 0:
#                             tempstring = 'Brand: ' + sen
#                         elif a == 1:
#                             tempstring += '\nSize: ' + sen
#                         elif a == 2:
#                             tempstring += '\nCondition: ' + sen
#                         elif a == 3:
#                             tempstring += '\nPrice: ' + sen
#                     output += '\n' + get_modified_text(2, tempstring, True)
#
#                 if i is len(spllistr)-1:  # measurements; weird situation, i is 0 in the last iteration
#                     newstring = ""
#                     stagspllit = strin.strip().split("&")
#                     for ii, stagstr in enumerate(stagspllit):
#                         if ii == 0:
#                             continue
#                         staglist += [int(stagstr[0])]
#                         strin = strin.strip()[:-2]
#                     sentences = strin.strip().split('\n')
#                     for a, sen in enumerate(sentences):
#                         bust = False
#                         val = 0.0
#                         for t in sen.split():
#                             if t == "Bust" or t == "Waist" or t == "Hips":
#                                 bust = True
#                             try:
#                                 val = (float(t))
#                                 break
#                             except ValueError:
#                                 pass
#                         newstring += sen.split()[0] + ": " + str(val) + "\"" + ("flat" if bust else "") + "/" + str(inch_to_cm(val)) + "cm" + '\n'
#                     newstring = 'Measurements: \n' + preappender(newstring)
#                     output = output + '\n' + get_modified_text(2, newstring, True)
#         print("sending", id)
#         output = append_hashtag(output, hashtags, specialtags.strip().split(' '), staglist)
#         # print(output)
#         for i in range(times):
#             send_to_messenger(output)
#
#
# def standard_text_parser(strin, times = 1):
#
#     hashtags = ''
#     specialtags = ''
#     for id, para in enumerate(strin.strip().split("$$")):
#         if id == 0:
#             splittedtag = para.strip().split("&")
#             for idx, stag in enumerate(splittedtag):
#                 if idx == 0:
#                     for id, tag in enumerate(stag.strip().split("#")):
#                         if id == 0:
#                             continue
#                         hashtags += "#" + tag
#                     continue
#                 specialtags += "#" + stag
#             continue
#         output = ''
#         splittedstring = para.strip().split("\n$")
#         staglist = []
#         for idx, splitstr in enumerate(splittedstring):
#             spllistr = splitstr.split('$')
#             for i, strin in enumerate(spllistr):
#
#                 if strin.isspace():
#                     continue
#                 if len(strin) == 0:
#                     continue
#                 if strin[0].isdigit() is False:
#                     break
#                 if i == 0:  # weird situation, i is 0 in the last iteration
#                     stagspllit = strin.strip().split("&")
#                     for ii, stagstr in enumerate(stagspllit):
#                         if ii == 0:
#                             continue
#                         staglist += [int(stagstr[0])]
#                         strin = strin.strip()[:-2]
#                     strin = preappender(strin)
#                 sum = int(strin[0])
#
#                 output = output + get_modified_text(sum, strin)
#
#                 for a in range(strin.count('\n') - 1):  # add lines to the end of a part
#                     output += '\n'
#             output += '\n'
#         output = append_hashtag(output, hashtags, specialtags.strip().split(' '), staglist)
#         for i in range(times):
#             send_to_messenger(output)
#
#
# def preappender(strin):
#     sentence = '\nModel reference: \nHeight: 162cm \n\nDm to order or if you have any inquiries, we won\'t bite!'
#     return strin.strip() + sentence
#
#
# def append_hashtag(output, hashtags, specialtags, staglist):
#     dots = ''
#     for i in range(8):
#         dots += ".\n"
#     output = output.strip() + '\n' + dots + hashtags.strip()
#     for number in staglist:
#         output += " " + specialtags[number-1].strip()
#     return output
#

# def get_modified_text(index, strin, autoadd=False):
#     if autoadd is True:
#         strin = str(index) + strin
#     textfield.clear()
#     textfield.send_keys(strin)
#     time.sleep(0.4)
#     # sentences = browser.find_element_by_id('ghetto-text').get_attribute('value').split('\n')
#     # sentences = browser.find_element_by_id('ghetto-text').get_attribute('value').split(str(index))
#
#     if index == 1:
#         sentences = instatext.find_element_by_id('ghetto-text').get_attribute('value').split('𝟏', 1)
#         sentences = sentences[1].split('𝟭', 1)
#     elif index == 2:
#         sentences = instatext.find_element_by_id('ghetto-text').get_attribute('value').split('𝟮', 1)
#         sentences = sentences[1].split('2', 1)
#     return sentences[0].strip()
#
#
# def send_to_messenger(finishedstr):
#     pyperclip.copy(finishedstr)
#     messenger.find_element_by_xpath("//*[@data-editor]").click()
#
#     # for i in range(times):
#     actions = ActionChains(messenger)
#     actions.key_down(Keys.CONTROL)
#     actions.send_keys('a')
#     actions.send_keys('v')
#     actions.perform()
#     actions.key_up(Keys.CONTROL)
#     actions.send_keys(Keys.ENTER)
#     actions.perform()

#
# def inch_to_cm(inch):
#     return round(inch * 2.54, 1)
"""

examplequote = """
Example (notice the symbols)
__________(remove everything on and before this line)____________
#thecatthrifts #thrifting #preloved #secondhand #thriftmalaysia #onlinethriftstore #thriftstore #stylewithus #thriftwithusthursdays #thriftstorefinds #eighthdrop #rainbow #tops #shorts #lowrise #unique #vintage #retro #valuebuy #slowfashionisthewaytogo #sustainablefashion #sustainability #supportsmallbusiness #smallbusiness #staysafestayhome #thecatthriftsavailable
&thecatthriftsavailabletop &thecatthriftsavailablebottom &thecatthriftsavailabledress &thecatthriftsavailablejacket

$$
Red long sleeve shirt

-
fits XS-S
7/10
RM13 (includes postage)

Shoulder 14
Sleeves 20
Bust 13.5
Length 19
&1
$$
Red skirt with safety pants

-
fits M-small L
8/10 
RM13 (includes postage)

Waist 15
Hips 19.5
Length 13.5
&2
"""

link_tooltip = """
Enter the numerical part of the web link to recipient.\n
For example, from the link \'https://www.messenger.com/t/100014936762209/\',\n
you would want to enter 100014936762209
"""

input_tooltip ="""
First paragraph consists of global hashtags (marked by \'#\');\n
Second paragraph consists of optional hashtags (marked by \'&\')\n
Start each entry with \'$$\', followed by -name-, -brand-, \n
-size-, -price-; then measurements in inch. Space each entry with \'$$\' \n
and use optional hashtags with \'&{index}\'
"""

save_cred_tooltip = """
If checked, credentials (EXCEPT password) will be saved upon pressing the \n
button 'Send to Messenger' and can be auto-filled next time the program \n
is opened."""