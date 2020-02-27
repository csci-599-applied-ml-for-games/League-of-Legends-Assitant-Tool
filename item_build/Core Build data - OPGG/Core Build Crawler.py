from bs4 import BeautifulSoup
from lxml import etree
import requests,sys,math,re,csv

champion_list = ["Aphelios","Ashe","Caitlyn","Cassiopeia","Draven","Ezreal","Heimerdinger","Jhin","Jinx","Kai'Sa","Kalista","Kindred","KogMaw","Lucian","MissFortune","Senna","Sivir","Syndra","Taliyah","Tristana","Twitch","Varus","Vayne","Xayah","Yasuo"]

user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
headers={"User-Agent":user_agent} 
csv_file = open("Core Build.csv","a+")

for champion_name in champion_list:
	print("working for " + champion_name + "\n")
	url='https://www.op.gg/champion/'+ champion_name +'/statistics/bot/item'
	html = requests.get(url,headers=headers).content
	tree = etree.HTML(html)
	contents = tree.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[5]/div[2]/div[1]/div[1]/div[1]/div[1]/table/tbody')
	
	byte = etree.tostring(contents[0],pretty_print=True) #for test
	f_export = open("export.html","wb")
	f_export.write(byte)
	f_export.close()
	
	f_content = open("export.html","r")
	contents_tree = etree.parse("export.html") #parse the tabe html to a etree
	all_buildsequence = contents_tree.getroot().getchildren() # [<Element tr at 0x113805370> * 8]
	
	for sequence in all_buildsequence:  #<tr> each sequence will include three <td>
		build = sequence[0].getchildren()[0].getchildren()  # <ul class="champion-stats__list">
		print("this build have", math.ceil(len(build)/2), "items") # 5 -> 3 item
		if(len(build)==5):
			index_list = [0,2,4]
			flag = 0
		elif(len(build)==7):
			index_list = [0,2,4,6]
			flag = 1
		
		export_entry = champion_name + ", "  
		for index in index_list:  # get the name of each item 
			title = build[index].get("title")
			pattern = "<b style='color: #00cfbc'>.*</b>"
			item_name = re.match(pattern, title).group().replace("<b style='color: #00cfbc'>","").replace("</b>","")       
			export_entry = export_entry + item_name + ", "
		
		pick_rate = sequence[1].text.strip() # <td class="champion-stats__table__cell champion-stats__table__cell--pickrate">
		win_rate = sequence[2].text.strip() # <td class="champion-stats__table__cell champion-stats__table__cell--winrate">
		
		if(flag == 1):	
			export_entry = export_entry + pick_rate + ", " + win_rate + '\n'
		else:
			export_entry = export_entry[0:-1] + ", " + pick_rate + ", " + win_rate + '\n'
		
		print(export_entry) 		
		csv_file.write(export_entry)

	