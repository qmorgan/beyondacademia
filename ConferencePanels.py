import pandas as pd
import glob
import datetime
import numpy

# CONFERENCE TABLE
#   conference_id   conference_date     conference duration conference_location

# PANEL TABLE              
#   panel_id       panel_name   conference_id   panel_description  panel_session

# 
# panel_list = [
# "Science Policy",
# "Non-Academic Research: Biology/Bioengineering",
# "Non-Academic Research: Psychology/Neuroscience",
# "Science Communication",
# "Education",
# "Scientific Consulting",
# "Startups",
# "Senior Science Management",
# "Tech - Non Data Analytics",
# "Entrepreneurship",
# "Management Consulting",
# "Tech - Data Analytics"
# ]
# 
# 
# speaker_placement = [
# "Science Policy",
# "Non-Academic Research: Biology/Bioengineering",
# "Non-Academic Research: Psychology/Neuroscience",
# "Science Communication",
# "Education",
# "Scientific Consulting",
# "Startups",
# "Senior Science Management",
# "Tech - Non Data Analytics",
# "Entrepreneurship",
# "Management Consulting",
# "Tech - Data Analytics"
# ]
# 
# 
# panel_description_list = [
# "Science Policy - Health and education advocacy, counsel to legislature, state and national science policy foundations",
# "Non-Academic Research (Psych/Neuro) - PhDs who conduct research in think tanks, non-profits, and R&D. Speakers in this panel will have a neuroscience/psychology background. ",
# "Non-Academic Research (Biotech) - PhDs who conduct research in the biotech industry, non-profits, and R&D. Speakers in this panel will have a bioengineering/biology background.",
# "Communication - PhDs working as editors, science writers, publishers, and in science outreach",
# "Education - ",
# "Scientific Consulting - Consulting careers that emphasize specific PhD training",
# "Startups - PhDs employed by startup companies",
# "Senior Science Management - PhDs with 10+ years of experience, who have transitioned to leadership/management positions",
# "Tech (non-data) - Panel will discuss careers available to PhDs in the technology industry such as User Experience, Marketing, and Strategy ",
# "Entrepreneurs - Panelists comprise PhDs involved in founding new companies",
# "Management Consulting -  Consulting careers that do not require training in a specific PhD discipline",
# "Data Analytics - PhDs from various quantitative backgrounds will discuss the field of big data analytics and statistics"
# ]
# 
# 
# conference_id = 0
# 
# panel_session_list = ["Feb. 21 - AM"]*3 + \
#                     ["Feb. 21 - PM"]*3 + \
#                     ["Feb. 22 - AM"]*3 + \
#                     ["Feb. 22 - PM"]*3
# 
# 
# 
# 
# panel_df = pd.DataFrame({"panel_name":panel_list,
#                         "conference_id":conference_id,
#                         "panel_session":panel_session_list
#                         })


# change this to a dataframe


conference_path = '/Users/amorgan/Desktop/ExpandableMenuTest/conferences.txt'
conference_df = pd.DataFrame.from_csv(conference_path,header=0, \
                        sep=';', index_col = 0, parse_dates = ['start_date'])



panel_description_path = '/Users/amorgan/Desktop/ExpandableMenuTest/panel_descriptions.txt'
panel_descriptions_df = pd.DataFrame.from_csv(panel_description_path, header=0, \
                        sep=';', index_col = 0, parse_dates = False)

for confindex, conference in conference_df.iterrows():
    current_conference_id = confindex
    start_date = conference['start_date']
    duration = int(conference['duration'])
    
    current_panel_path = '/Users/amorgan/Desktop/ExpandableMenuTest/{}/panels.txt'.format(current_conference_id)
    current_panel_df = pd.DataFrame.from_csv(current_panel_path, header=0, \
                            sep=';', index_col = None, parse_dates = False)
    current_panel_df['conference_id'] = current_conference_id

    # SPEAKER TABLE
    #   speaker_id   speaker_shortbio   speaker_bio speaker_picture

    speakernames = []
    speakerdescripts = []
    speakerimgpaths = []
    speakerbios = []
    speakerpath = '/Users/amorgan/Desktop/ExpandableMenuTest/expandableList/speakers/'
    speaker_img_path = "http://blog.beyondacademia.org/" + 'img/'
    speakerfiles = glob.glob(speakerpath + '*.txt')
    for speaker in speakerfiles:
        f = open(speaker)
        lines = f.readlines()
        speakernames.append(lines[0].strip())
        speakerdescripts.append(lines[1].strip())
        speakerimgpaths.append(lines[2].strip())
        speakerbios.append('\n<br>'.join(lines[3:]))



    speaker_df = pd.DataFrame({"speaker_shortbio":speakerdescripts,
                               "speaker_img":speakerimgpaths,
                               "speaker_bio":speakerbios
                            }, index = speakernames)
    speaker_df.index.name = "speaker_name"

    html_block = '''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>Panels/Speakers</title>
            <link rel="stylesheet" href="css/style.css" type="text/css" media="screen, projection">
            <script type="text/javascript" src="js/jquery-1.4.2.min.js">
            </script>
            <script type="text/javascript" src="js/scripts.js">
            </script>
            </script>
        </head>
        <body>
            <h1><b>Demo ExpandableList</b></h1>
            Our panels and speakers for the 2014 Berkeley Conference are listed below. Click on panel names to see the panelists, and click on panelists to see their biographies. 
        
            <div id="listContainer">
                <div class="listControl">
                    <a id="expandList">Expand All</a><a id="collapseList">Collapse All</a>
                </div>
                <ul id="expList">
        
    '''

    # Get all the panels at the conference of interest
    current_panels = current_panel_df[current_panel_df['conference_id'] == current_conference_id]

    # Loop through all the sessions
    sorted_panel_list = list(set(current_panels['panel_session']))
    sorted_panel_list.sort()
    for session in sorted_panel_list:
        # Add the header for this session
        # rename session based on conference date
        # day1a => Thursday February 20 - Morning Session
        
        ampm = ''
        day_offset = datetime.timedelta(int(session[-2]) - 1)
        if session[-1] == 'a': ampm = "Morning"
        if session[-1] == 'b': ampm = "Afternoon"
        str_date = (start_date + day_offset).strftime('%A, %B %d')
        session_text = str_date + ' - ' + ampm + ' Session'
        
        html_block += '''
            <li style="font-weight:bold;text-align:center">
            {}
            </li>'''.format(session_text)
        # Loop through each panel
        sub_panels = current_panels[current_panels['panel_session'] == session]
        for index, row in sub_panels.iterrows():
            current_descrip = ""
            if row['panel_name'].strip() in panel_descriptions_df.index:
                current_descrip = " <br> "
                current_descrip += panel_descriptions_df.loc[row['panel_name'].strip()]['panel_description']        
            html_block += '''<a name="{}"></a>
                <li>
                <strong>{}</strong> <span style="font-size:80%">{}</span>
                <ul>
                '''.format(row['panel_name'],row['panel_name'], current_descrip)
            # loop through the speakers    
            for speaker in row['panel_speakers'].split(','):
                html_block += '''
                    <li>
                    <strong>{}</strong> '''.format(speaker.strip())
                    # if we have a database entry for the speaker, grab its info
                if speaker.strip() in speaker_df.index:
                    speaker_info = speaker_df.loc[speaker.strip()]
                    html_block += ''' - <span style="font-size:90%;font-weight:bold;">{}</span>
                    <ul>
                        <li>
                            <span><img src="{}" style="float:left;height:100px;" alt="{}" ><noclick>{}</noclick></span>
                        </li>
                    </ul>'''.format(speaker_info['speaker_shortbio'], speaker_img_path + speaker_info['speaker_img'], speaker.strip(), speaker_info['speaker_bio'])
                html_block += '''
                    </li>'''
            html_block += '''
                </ul>
                </li>
            '''    
        html_block += '''
        <hr>'''



    html_block += '''
                </ul>
            </div>
        </body>
    </html>'''

    f = file('panels.html','w')
    f.write(html_block)
    f.close()


    ##### SCHEDULE PAGE ######

    speaker_link_page_id='50'


    # aa.strftime('%A %B %d')


    html_block2 = '''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>Schedule</title>
            <link rel="stylesheet" href="css/scheduletable.css" type="text/css" media="screen, projection">
        </head>
        <body>        
    
        
    '''
    # loop through each day in the conference
    for day in numpy.arange(duration):
        
        day_sched_path = '/Users/amorgan/Desktop/ExpandableMenuTest/{}/sched_{}.txt'.format(current_conference_id,str(int(day+1)))
        day_sched = pd.DataFrame.from_csv(day_sched_path, header=0, \
                                sep=';', index_col = 0, parse_dates = False)
        
        
        day_offset = datetime.timedelta(int(day))
        str_date = (start_date + day_offset).strftime('%A, %B %d')
        html_block2 += '''
        <h4 style="font-weight:bold;text-align:center">{}</h4>
        <table class=tg-table-paper>
        '''.format(str_date)
        count = 1
        for time, event in day_sched.iterrows():
            
            if count%2==0:
                evenclass = ' class="tg-even"'
            else:
                evenclass = ''
            # do a special row if its a panel choice
            if event.values[0][0:5] == 'panel':
                panel_header_text = ''
                if event.values[0][-1] == 'a':
                    panel_header_text = "AM Panel (Choose one)"
                if event.values[0][-1] == 'b':
                    panel_header_text = "PM Panel (Choose one)"
                
                # "day1a" format
                session = 'day' + str(day+1) + event.values[0][-1]
                
                # grab the panels that match the day and session
                matched_panels = current_panels[current_panels['panel_session'] == session]
                
                colspan = len(matched_panels)
                
                html_block2 += '''
                <tr{}>
                  <td rowspan="2" class="width-fixed">{}</td>
                  <td colspan="{}" class="mini-header">{}</td>
                </tr>
                '''.format(evenclass,time,colspan,panel_header_text)
                html_block2 += '''
                <tr{}>'''.format(evenclass)
                for panel in matched_panels['panel_name']:
                    html_block2 += '''
                    <td><a href="index.php?page_id={}#{}">{}</a></td>'''.format(speaker_link_page_id,panel,panel)
                html_block2 += '''
                </tr>
                '''
            #otherwise do a normal table row
            # FIXME: Colspan is fixed at a length of 3.. may not be a choice of 3 panels forever
            else:
                html_block2 += '''
                <tr{}>
                  <td class="width-fixed">{}</td>
                  <td colspan="3" class="width-variable">{}</td>
                </tr>
                '''.format(evenclass,time,event.values[0])
            count += 1 
        html_block2 += '''</table>'''
        

    html_block2 += '''
        </body>
    </html>'''

    f = file('schedule.html','w')
    f.write(html_block2)
    f.close()


#### MEDIA PAGE ####
media_path = '/Users/amorgan/Desktop/ExpandableMenuTest/media.txt'
media_df = pd.DataFrame.from_csv(media_path,header=0, \
                        sep=';', index_col = None, parse_dates = ['media_date'])
media_sorted = media_df.sort('media_date',ascending=False)
html_media = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Media</title>
        <link rel="stylesheet" href="css/scheduletable.css" type="text/css" media="screen, projection">
    </head>
    <body>
    <table class=tg-table-paper style="width:100%;text-align:left>
    '''
count = 1
for index, row in media_sorted.iterrows():

    if count%2==0:
        evenclass = ' class="tg-even"'
    else:
        evenclass = ''
    
    html_media += '''
    <tr{}>
      <td class="width-fixed" style="width:125px;vertical-align:top;text-align:center">{}</td>
      <td class="width-variable"><a href="{}" style="font-weight:bold">{}</a>{}</td>
    </tr>
    '''.format(evenclass,row['media_date'].strftime('%b %d, %Y'), \
        row['media_link'],row['media_title'],row['media_description'])
    count += 1

html_media += '''
      </table>
    </body>
</html>'''

f = file('media.html','w')
f.write(html_media)
f.close()