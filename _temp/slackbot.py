from slacker import Slacker
from time import sleep

slack = Slacker('xoxb-1468925324080-1455173451507-tNWizE0O6j670DAtnELrYKkF')
# slack.chat.post_message('stockbot', 
#     attachments=[
#         {'color':'#ff0000',
#         'author_name':'STOCKBOT',
#         'title':'KOSPI',
#         'title_link':'https://finance.naver.com/sise/sise_index.nhn?code=KOSPI',
#         'image_url':'https://ssl.pstatic.net/imgstock/chart3/day90/KOSPI.png?sidcode=1603758430977'}])

while True:
    slack.chat.post_message('stockbot', '원우 외않와????????')
    sleep(10)
    slack.chat.post_message('stockbot', '배구어누외않와????????')
    sleep(10)