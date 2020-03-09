import sys,os, re,csv
import requests
from bs4 import BeautifulSoup

def get_match_list(player_name):
    base = "https://www.op.gg/summoner/userName="
    # url = base + urllib.parse.quote_plus(palyer_name)
    url = base + player_name
    # url = "https://www.op.gg/summoner/userName=%ED%98%84%EC%98%B9%EA%B3%BC+%EC%83%81%ED%8B%B8%EB%8B%A4"
    r = requests.get(url)
    soup_page_one = BeautifulSoup(r.text,'html.parser')

    # get summoner ID
    user_info = {}
    div_GameListContainer = soup_page_one.find(name='div',attrs={'class':'GameListContainer'}).attrs
    user_info['data-summoner-id'] = div_GameListContainer['data-summoner-id']
    user_info['data-last-info'] = div_GameListContainer['data-last-info']

    div_GameItemWrap_page_one = soup_page_one.find_all(name='div',attrs={'class':'GameItemWrap'})
    match_info_page_one = []
    for i in range(len(div_GameItemWrap_page_one)):
        this_match = list(div_GameItemWrap_page_one[i].children)[1].attrs
        match_info_page_one.append(this_match)
    print("player {} page 1, done.".format(player_name))

    # Page 2
    first_show_more_url = "https://www.op.gg/summoner/matches/ajax/averageAndList/startInfo={}&summonerId={}".format(user_info['data-last-info'],user_info['data-summoner-id'])
    response_page_two = requests.get(first_show_more_url)
    if response_page_two.status_code == 200:
        print('Page 2, Status Code: 200, Success!')
        if response_page_two.headers['content-type'] == 'text/json;charset=UTF-8':
            soup_page_two = BeautifulSoup(response_page_two.json()['html'],'html.parser')
    elif response_page_two.status_code == 404:
        print('Not Found.',first_show_more_url)
    # grab the useful info from page 2
    div_GameItemWrap_page_two = soup_page_two.find_all(name='div',attrs={'class':'GameItemWrap'})
    match_info_page_two = []
    for i in range(len(div_GameItemWrap_page_two)):
        this_match = list(div_GameItemWrap_page_two[i].children)[1].attrs
        # this_match.pop('class')
        match_info_page_two.append(this_match)
    print("player {} page 2,done.".format(player_name))

    # Page 3
    second_show_more_url = "https://www.op.gg/summoner/matches/ajax/averageAndList/startInfo={}&summonerId={}".format(match_info_page_two[-1]['data-game-time'],match_info_page_two[-1]['data-summoner-id'])
    response_page_three = requests.get(second_show_more_url)
    if response_page_three.status_code == 200:
        print('Page 3, Status Code: 200, Success!')
        if response_page_three.headers['content-type'] == 'text/json;charset=UTF-8':
            soup_page_three = BeautifulSoup(response_page_three.json()['html'],'html.parser')
    elif response_page_three.status_code == 404:
        print('Not Found.',second_show_more_url)

    div_GameItemWrap_page_three = soup_page_three.find_all(name='div',attrs={'class':'GameItemWrap'})
    match_info_page_three = []
    for i in range(len(div_GameItemWrap_page_three)):
        this_match = list(div_GameItemWrap_page_three[i].children)[1].attrs
        # this_match.pop('class')
        match_info_page_three.append(this_match)

    print("player {} page 3, done.".format(player_name))

    match_list = []
    match_list.append(match_info_page_one)
    match_list.append(match_info_page_two)
    match_list.append(match_info_page_three)
    print("Got the match list of three pages.\n")

    return(match_list) # match_list[page][match]

def get_detail_soup(p,m,info):
    page = p
    match = m
    match_info = info
    print("Working:page {}, match {} (Player Count {})".format(page,match,working_count))        

    request_parameters = dict()
    request_parameters['gameId']= match_info[page][match]['data-game-id']
    request_parameters['summonerId']=match_info[page][match]['data-summoner-id']
    request_parameters['gameTime']=match_info[page][match]['data-game-time']
    detail_url = "https://www.op.gg/summoner/matches/ajax/detail/gameId={}&summonerId={}&gameTime={}".format(request_parameters['gameId'],request_parameters['summonerId'],request_parameters['gameTime'])

    # start fetch the detail of a match
    detail_request = requests.get(detail_url)
    detail_soup = BeautifulSoup(detail_request.text,'html.parser')

    divGameDetailTableWrap = detail_soup.find(name='div',attrs={'class':'GameDetailTableWrap'})
    
    return(divGameDetailTableWrap)


def get_match_info(p,m,d_soup,info):
    page = p
    match = m
    match_info = info
    # print("Working on page {}, match {}".format(page,match))        

    # request_parameters = dict()
    # request_parameters['gameId']= match_info[page][match]['data-game-id']
    # request_parameters['summonerId']=match_info[page][match]['data-summoner-id']
    # request_parameters['gameTime']=match_info[page][match]['data-game-time']
    # detail_url = "https://www.op.gg/summoner/matches/ajax/detail/gameId={}&summonerId={}&gameTime={}".format(request_parameters['gameId'],request_parameters['summonerId'],request_parameters['gameTime'])

    # # start fetch the detail of a match
    # detail_request = requests.get(detail_url)
    # detail_soup = BeautifulSoup(detail_request.text,'html.parser')

    # divGameDetailTableWrap = detail_soup.find(name='div',attrs={'class':'GameDetailTableWrap'})

    divGameDetailTableWrap = d_soup

    # Ally Team
    allyteam_soup = list(divGameDetailTableWrap.children)[1]
    allyteam_player = []
    tbodyContent_list = list(allyteam_soup.find(name='tbody',attrs={'class':'Content'}).children)

    for i in range(1,10,2):
        allyteam_player.append(tbodyContent_list[i])
    allyteam = []
    export_list_ally = []
    for i in range(len(allyteam_player)): # 0,1,2,3,4
        # get the information a player
        a_player = list(allyteam_player[i].children)

        champion_name = re.findall(r"[a-zA-Z&' ]+",a_player[1].get_text())[0]
        champion_level = re.findall(r"\d+",a_player[1].get_text())[0]
        summoner_spell = a_player[3]
        rune = a_player[5]
        this_player_name = a_player[7].get_text().strip()
        tier_level = a_player[9].get_text().strip()

        item_build_soup = list(a_player[-2].children)
        item_build = []
        
        for i in range(1,len(item_build_soup),2):
            item = re.findall(r'img alt="[a-zA-Z \'-]+"',str(item_build_soup[i]))
            if item == []:
                item_build.append("")
            else:
                item_build.append(item[0].replace("img alt=","")[1:-1])

        export_dict_ally = {}
        export_dict_ally['Alignment'] = "Ally"
        export_dict_ally['Player Name'] = this_player_name
        export_dict_ally['Champion'] = champion_name
        export_dict_ally['Item Build'] = item_build
        export_dict_ally['Level'] = champion_level
        export_dict_ally['Tier Level'] = tier_level
        export_dict_ally['Summoner Spell'] = summoner_spell
        export_dict_ally['Rune'] = rune
        export_list_ally.append(export_dict_ally)


    # Enemy Team
    enemyteam_soup = list(divGameDetailTableWrap.children)[5]
    enemyteam_player = []
    tbodyContent_list = list(enemyteam_soup.find(name='tbody',attrs={'class':'Content'}).children)

    for i in range(1,len(tbodyContent_list),2):
        enemyteam_player.append(tbodyContent_list[i])
    enemyteam = []
    export_list_enemy = []
    for i in range(len(allyteam_player)): # 0,1,2,3,4
        # get the information a player
        a_player = list(enemyteam_player[i].children)
        champion_name = re.findall(r"[a-zA-Z&' ]+",a_player[1].get_text())[0]
        champion_level = re.findall(r"\d+",a_player[1].get_text())[0]
        summoner_spell = a_player[3]
        rune = a_player[5]
        this_player_name = a_player[7].get_text().strip()
        tier_level = a_player[9].get_text().strip()

        item_build_soup = list(a_player[-2].children)
        item_build = []

        for i in range(1,len(item_build_soup),2):
            item = re.findall(r'img alt="[a-zA-Z \'-]+"',str(item_build_soup[i]))
            if item == []:
                item_build.append("")
            else:
                item_build.append(item[0].replace("img alt=","")[1:-1])
        
        export_dict_enemy = {}
        export_dict_enemy['Alignment'] = "enemy"
        export_dict_enemy['Player Name'] = this_player_name
        export_dict_enemy['Champion'] = champion_name
        export_dict_enemy['Item Build'] = str(item_build)
        export_dict_enemy['Level'] = champion_level
        export_dict_enemy['Tier Level'] = tier_level
        export_dict_enemy['Summoner Spell'] = str(summoner_spell)
        export_dict_enemy['Rune'] = str(rune)
        
        export_list_enemy.append(export_dict_enemy)

    # fieldnames = ('Page','Match','Game Result', 'Champion','My Item Build','Enemy Team Build')
    f = open(work_file_path,'at')
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    for ally in export_list_ally:
        if ally['Player Name'] == player_name:
            export_dict={}
            export_dict['Page'] = page
            export_dict['Match'] = match
            export_dict['Game Result'] = match_info[page][match]['data-game-result']
            export_dict['Champion'] = ally['Champion']
            export_dict['My Item Build'] = ally['Item Build']
            for enemy in export_list_enemy:
                export_dict['Enemy Team Build'] = enemy['Item Build']
                csv_writer.writerow(export_dict)
        else:
            continue
    
    f.close()   


def one_player(name):
    match_info = get_match_list(name)
    
    for i in range(len(match_info)):   # page
        for j in range(len(match_info[i])):    # match
            if 'Remake' in match_info[i][j]['class']:
                print("Remake, Skipped")
            else:
                soup = get_detail_soup(i,j,match_info)
                if soup != None:
                    try:
                        get_match_info(i,j,soup,match_info)
                    except(IndexError):
                        print("IndexError, Passed!")
                        continue
                else:
                    print("Soup is empty, skipped")

def main():
    global player_name
    global fieldnames
    global work_file_path
    global working_count
    
    fieldnames = ('Page','Match','Game Result', 'Champion','My Item Build','Enemy Team Build')

    #working_champion = "Cassiopeia"
    working_champion = sys.argv[1]

    print("working_champion is",working_champion)
    
    path = "/Users/oscar/Dropbox/! Schoolwork/CSCI 599 Applied Machine Learning for Games/item-build/player_name ranking/{}.txt".format(working_champion)
    save_path = "/Users/oscar/Dropbox/! Schoolwork/CSCI 599 Applied Machine Learning for Games/item-build/export/{}/".format(working_champion)

    try: 
        os.mkdir(save_path) 
    except OSError as error: 
        print("folder exists")

    with open(path,"r") as file:
        content = file.read()
    player = eval(content)
    
    starting_from = 0
    try:
        starting_from = sys.argv[2]
        print("Arguemnt received,Starting from", starting_from)
    except(IndexError):
        starting_from = 0
        print("No arguemnt, Starting from 0")

    for id in player[int(starting_from):]:
        player_name = id[1]
        working_count = id[2]
        print("Working on Player: ", player_name, "; Number ",working_count)
        
        work_file_path = save_path+player_name+".csv"
        
        f = open(work_file_path,'wt')
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()
        f.close()
        
        try:
            one_player(player_name)
        except(AttributeError,UnboundLocalError) :
            print('error')
        print(player_name,"Done\n")

    # player_name = "E8"

    # f = open(player_name+".csv",'at')
    # csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    # csv_writer.writeheader()
    # f.close()

    # one_player(player_name)
    # print(player_name,"Done\n")

if __name__ == "__main__":
    main()
