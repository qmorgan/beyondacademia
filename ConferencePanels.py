import pandas as pd
import glob
import datetime
import numpy
import os,sys

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


conference_path = 'conferences.txt'
conference_df = pd.DataFrame.from_csv(conference_path,header=0, \
                        sep=';', index_col = 0, parse_dates = ['start_date'])



panel_description_path = 'panel_descriptions.txt'
panel_descriptions_df = pd.DataFrame.from_csv(panel_description_path, header=0, \
                        sep=';', index_col = 0, parse_dates = False)
                        

workshop_description_path = 'workshop_descriptions.txt'
workshop_descriptions_df = pd.DataFrame.from_csv(workshop_description_path, header=0, \
                        sep=';', index_col = 0, parse_dates = False)                        


sponsors_description_path = 'sponsors_descriptions.txt'
sponsors_descriptions_df = pd.DataFrame.from_csv(sponsors_description_path, header=0, \
                        sep=';', index_col = 0, parse_dates = False)

for confindex, conference in conference_df.iterrows():
    current_conference_id = confindex
    start_date = conference['start_date']
    duration = int(conference['duration'])
    
    current_panel_path = '{}/panels.txt'.format(current_conference_id)
    current_panel_df = pd.DataFrame.from_csv(current_panel_path, header=0, \
                            sep=';', index_col = None, parse_dates = False)
    current_panel_df['conference_id'] = current_conference_id

    # SPEAKER TABLE
    #   speaker_id   speaker_shortbio   speaker_bio speaker_picture

    speakernames = []
    speakerdescripts = []
    speakerimgpaths = []
    speakerbios = []
    speakerpath = 'wordpress_testing/speakers/'
    speaker_img_path = "http://www.beyondacademia.org/" + 'img/'
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
            <link rel="stylesheet" href="../wordpress_testing/css/style.css" type="text/css" media="screen, projection">
            <script type="text/javascript" src="js/jquery-1.4.2.min.js">
            </script>
            <script type="text/javascript" src="js/scripts.js">
            </script>
            </script>
        </head>
        <body>
            <h1><b>Speakers</b></h1>
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
    # first grab the list of all the sessions
    sorted_panel_list = list(set(current_panels['panel_session']))
    # sort them by day1a day1b day2a day2b etc. 
    sorted_panel_list.sort()
    for session in sorted_panel_list:
        # Add the header for this session
        # rename session based on conference date
        # day1a => Thursday February 20 - Morning Session
        ampm = ''
        str_date = ''
        if 'day' in session:
            day_offset = datetime.timedelta(int(session[-2]) - 1)
            if session[-1] == 'a': ampm = "Morning"
            if session[-1] == 'b': ampm = "Afternoon"
            str_date = (start_date + day_offset).strftime('%A, %B %d')
            session_text = str_date + ' - ' + ampm + ' Session'
        else:
            session_text = session[1:]
        
        html_block += '''
        <hr>
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
                speaker_string = speaker.strip()
                is_moderator = False
                # can deal with e.g. "thursday: Bob Hope"
                curr_speaker = speaker.split(':')[-1].strip()
                # if it's tagged as a moderator with an 'm' out front, mark it as such
                if curr_speaker[0] == 'm':
                    curr_speaker = curr_speaker[1:].strip()
                    is_moderator = True
                    speaker_string = speaker_string[1:]
                html_block += '''
                    <li>
                    <strong>{}</strong> '''.format(speaker_string)
                if is_moderator:
                    html_block += ' (moderator)'
                # if we have a database entry for the speaker, grab its info
                if curr_speaker in speaker_df.index:
                    speaker_info = speaker_df.loc[curr_speaker]
                    img_block = ""
                    # only add dash if shortbio exists
                    if speaker_info['speaker_shortbio'].strip() != '':
                        html_block += ' - '
                    if speaker_info['speaker_img'].strip() != 'NONE':
                        styletext=''
                        img_block = '<img src="{}" style="float:left;height:100px;" alt="{}" >'.format(speaker_img_path + speaker_info['speaker_img'], curr_speaker)
                    else:
                        # get rid of the min height requirement for the cell
                        styletext=' style="min-height:20px"'
                    html_block += '''<span style="font-size:90%;font-weight:bold;">{}</span>
                    <ul>
                        <li{}>
                            <span>{}<noclick>{}</noclick></span>
                        </li>
                    </ul>'''.format(speaker_info['speaker_shortbio'], styletext, img_block, speaker_info['speaker_bio'])
                html_block += '''
                    </li>'''
            html_block += '''
                </ul>
                </li>
            '''    
        html_block += '''
        '''



    html_block += '''
                </ul>
            </div>
        </body>
    </html>'''

    f = file(current_conference_id+'/panels.html','w')
    f.write(html_block)
    f.close()

    ######## workshop page ######
    current_workshop_path = '{}/workshops.txt'.format(current_conference_id)
    if os.path.exists(current_workshop_path):
        
        current_workshop_df = pd.DataFrame.from_csv(current_workshop_path, header=0, \
                                sep=';', index_col = None, parse_dates = False)
        current_workshop_df['conference_id'] = current_conference_id

        # SPEAKER TABLE
        #   speaker_id   speaker_shortbio   speaker_bio speaker_picture

        speakernames = []
        speakerdescripts = []
        speakerimgpaths = []
        speakerbios = []
        speakerpath = 'wordpress_testing/speakers/'
        speaker_img_path = "http://www.beyondacademia.org/" + 'img/'
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
                <title>Workshops</title>
                <link rel="stylesheet" href="../wordpress_testing/css/style.css" type="text/css" media="screen, projection">
                <script type="text/javascript" src="js/jquery-1.4.2.min.js">
                </script>
                <script type="text/javascript" src="js/scripts.js">
                </script>
                </script>
            </head>
            <body>
                <h1><b>Workshops</b></h1>
                Our workshops for the 2014 Berkeley Conference are listed below.
        
                <div id="listContainer">
                    <div class="listControl">
                        <a id="expandList">Expand All</a><a id="collapseList">Collapse All</a>
                    </div>
                    <ul id="expList">
        
        '''

        # Get all the workshops at the conference of interest
        current_workshops = current_workshop_df[current_workshop_df['conference_id'] == current_conference_id]

        # Loop through all the sessions
        # first grab the list of all the sessions
        sorted_workshop_list = list(set(current_workshops['workshop_session']))
        # sort them by day1a day1b day2a day2b etc. 
        sorted_workshop_list.sort()
        for session in sorted_workshop_list:
            # Add the header for this session
            # rename session based on conference date
            # day1a => Thursday February 20 - Morning Session
            ampm = ''
            str_date = ''
            if 'day' in session:
                day_offset = datetime.timedelta(int(session[-2]) - 1)
                if session[-1] == 'a': ampm = "Morning"
                if session[-1] == 'b': ampm = "Afternoon"
                str_date = (start_date + day_offset).strftime('%A, %B %d')
                session_text = str_date + ' - ' + ampm + ' Workshops'
            else:
                session_text = session[1:]
        
            html_block += '''
            <hr>
                <li style="font-weight:bold;text-align:center">
                {}
                </li>'''.format(session_text)
            # Loop through each workshop
            sub_workshops = current_workshops[current_workshops['workshop_session'] == session]
            for index, row in sub_workshops.iterrows():
                current_descrip = ""
                if row['workshop_name'].strip() in workshop_descriptions_df.index:
                    current_descrip = " <br> "
                    current_descrip += workshop_descriptions_df.loc[row['workshop_name'].strip()]['workshop_description']        
                html_block += '''<a name="{}"></a>
                    <li>
                    <strong>{}</strong> <span style="font-size:80%">{}</span>
                    <ul>
                    '''.format(row['workshop_name'],row['workshop_name'], current_descrip)
                # loop through the speakers    
                for speaker in row['workshop_speakers'].split(','):
                    # can deal with e.g. "thursday: Bob Hope"
                    curr_speaker = speaker.split(':')[-1].strip()
                    html_block += '''
                        <li>
                        <strong>{}</strong> '''.format(speaker.strip())
                        # if we have a database entry for the speaker, grab its info
                    if curr_speaker in speaker_df.index:
                        speaker_info = speaker_df.loc[curr_speaker]
                        img_block = ""
                        # only add dash if shortbio exists
                        if speaker_info['speaker_shortbio'].strip() != '':
                            html_block += ' - '
                        if speaker_info['speaker_img'].strip() != 'NONE':
                            styletext=''
                            img_block = '<img src="{}" style="float:left;height:100px;" alt="{}" >'.format(speaker_img_path + speaker_info['speaker_img'], curr_speaker)
                        else:
                            # get rid of the min height requirement for the cell
                            styletext=' style="min-height:20px"'
                        html_block += '''<span style="font-size:90%;font-weight:bold;">{}</span>
                        <ul>
                            <li{}>
                                <span>{}<noclick>{}</noclick></span>
                            </li>
                        </ul>'''.format(speaker_info['speaker_shortbio'], styletext, img_block, speaker_info['speaker_bio'])
                        html_block += '''
                        </li>'''
                html_block += '''
                    </ul>
                    </li>
                '''    
            html_block += '''
            '''



        html_block += '''
                    </ul>
                </div>
            </body>
        </html>'''

        f = file(current_conference_id+'/workshops.html','w')
        f.write(html_block)
        f.close()
    
    else:
        print "Warning: No workshop files exist for conference_id '{}'".format(current_conference_id)
        print "Not making a workshop page for this conference."
    
    
    
    
    ######## sponsors page ######
    
    current_sponsors_path = '{}/sponsors.txt'.format(current_conference_id)
    if os.path.exists(current_sponsors_path):
        
        current_sponsors_df = pd.DataFrame.from_csv(current_sponsors_path, header=0, \
                                sep=';', index_col = None, parse_dates = False)
        current_sponsors_df['conference_id'] = current_conference_id

        # SPEAKER TABLE
        #   speaker_id   speaker_shortbio   speaker_bio speaker_picture

        speakernames = []
        speakerdescripts = []
        speakerimgpaths = []
        speakerbios = []
        speakerpath = 'wordpress_testing/speakers/'
        speaker_img_path = "http://www.beyondacademia.org/" + 'img/'
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
                <title>Sponsors</title>
                <link rel="stylesheet" href="../wordpress_testing/css/scheduletable.css" type="text/css" media="screen, projection">
            </head>
            <body>
                We are grateful to the following sponsors for the 2014 Berkeley Conference.<br>
                <center>
        '''
        script_block = ""
        sb0 = '''
        <script type="text/javascript">
        //in wordpress, cant have spaces when pasting into editor.
        //create variables from the existing link URLs
        '''
        sb1 = '''//create array that keeps the source of the images and the URLs of their links together during the random sorting
            '''
        sb2 = '''//create varialbe to hold all of this
            var img_name = new Array('''
        sb3 = '''
            //function for creating random sort order
            function randOrd(){ return (Math.round(Math.random())-0.5); } 
            //sort top layer of array for random order
            img_name.sort( randOrd );
            //change the source of the images
            '''
        sb4 = '''//change the URL of the link
        '''
        
        # Get all the sponsors at the conference of interest
        current_sponsors = current_sponsors_df[current_sponsors_df['conference_id'] == current_conference_id]
        
        merged_sponsors = pd.merge(current_sponsors,sponsors_descriptions_df,left_on="sponsor_id",right_index=True)
        
        # using count instead of index in case i want to skip rows
        # the javascript gets screwy otherwise
        count = 0 
        for index,row in merged_sponsors.iterrows():
            if row['sponsor_level'] == 0.0: continue #skip certain rows
            html_block+='''<a href="{}" id="lnk{}"><img src="http://www.beyondacademia.org/img/{}" name="ImagePH{}" style="max-height:100px;" id="one" /></a><br />
'''.format(row['sponsor_website'],count,row['sponsor_logo'],count)
            sb0+='''var dlnk{} = document.getElementById("lnk{}").href
            '''.format(count,count)
            sb1+='''var group{} = new Array("http://www.beyondacademia.org/img/{}",dlnk{});
            '''.format(count,row['sponsor_logo'],count)
            sb2+="group{},".format(count)
            sb3+='''document.ImagePH{}.src = img_name[{}][0];
            '''.format(count,count)
            sb4+='''document.getElementById("lnk{}").href = img_name[{}][1];  
            '''.format(count,count)
            count += 1
                
        sb2 = sb2.rstrip(',')+");"
        html_block += sb0 + sb1 + sb2 + sb3 + sb4 + "</script>"
        html_block += '''
            </center>
            </body>
        </html>'''

        f = file(current_conference_id+'/sponsors.html','w')
        f.write(html_block)
        f.close()
    
    else:
        print "Warning: No sponsors files exist for conference_id '{}'".format(current_conference_id)
        print "Not making a sponsors page for this conference."
    
    ##### SCHEDULE PAGE ######

    speaker_link_page_id='50'


    # aa.strftime('%A %B %d')
    # check to see if there are schedule files
    scheds_paths = '{}/sched*.txt'.format(current_conference_id)
    schedfilelist = glob.glob(scheds_paths)
    # continue if there are no schedule files; don't make any html for this conference
    if duration != len(schedfilelist):
        print "WARNING. Duration is set as {} in {}, but {} files are found in the path {}".format(duration,conference_path,len(schedfilelist),scheds_paths)
    
    if not schedfilelist:
        print "Warning: No schedule files exist for conference_id '{}'".format(current_conference_id)
        print "Not making a schedule page for this conference."
        continue
    html_block2 = '''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>Schedule</title>
            <link rel="stylesheet" href="../wordpress_testing/css/scheduletable.css" type="text/css" media="screen, projection">
        </head>
        <body>        
    
        
    '''
    # loop through each day in the conference
    for day in numpy.arange(duration):
        
        sched_df_path = '{}/sched_{}.txt'.format(current_conference_id,str(int(day+1)))
        if not os.path.exists(sched_df_path):
            print "{} does not exist; not making schedule for this day.".format(sched_df_path)
            continue
        sched_df = pd.DataFrame.from_csv(sched_df_path, header=0, \
                                sep=';', index_col = 0, parse_dates = False)
        
        
        day_offset = datetime.timedelta(int(day))
        str_date = (start_date + day_offset).strftime('%A, %B %d')
        html_block2 += '''
        <h4 style="font-weight:bold;text-align:center">{}</h4>
        <table class=tg-table-paper>
        '''.format(str_date)
        count = 1
        max_colspan = 1 # keeping track of the total number of columns
        
        for time, event in sched_df.iterrows():
            
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
                if colspan > max_colspan:
                    max_colspan = colspan
                
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
                    <td><a href="conference/speakers/#{}">{}</a></td>'''.format(panel,panel)
                html_block2 += '''
                </tr>
                '''
            # do a special row if its a workshop choice
            elif event.values[0][0:5] == 'works':
                workshop_header_text = ''
                if event.values[0][-1] == 'a':
                    workshop_header_text = "AM Workshop (Choose one)"
                if event.values[0][-1] == 'b':
                    workshop_header_text = "PM Workshop (Choose one)"
                
                # "day1a" format
                session = 'day' + str(day+1) + event.values[0][-1]
                
                # grab the workshops that match the day and session
                matched_workshops = current_workshops[current_workshops['workshop_session'] == session]
                
                colspan = len(matched_workshops)
                if colspan > max_colspan:
                    max_colspan = colspan
                
                html_block2 += '''
                <tr{}>
                  <td rowspan="2" class="width-fixed">{}</td>
                  <td colspan="{}" class="mini-header">{}</td>
                </tr>
                '''.format(evenclass,time,colspan,workshop_header_text)
                html_block2 += '''
                <tr{}>'''.format(evenclass)
                for workshop in matched_workshops['workshop_name']:
                    html_block2 += '''
                    <td><a href="conference/workshops/#{}">{}</a></td>'''.format(workshop,workshop)
                html_block2 += '''
                </tr>
                '''
            # Mark Colspan as unknown - replace with true number of columns later
            else:
                html_block2 += '''
                <tr{}>
                  <td class="width-fixed">{}</td>
                  <td colspan="UNKNOWN" class="width-variable">{}</td>
                </tr>
                '''.format(evenclass,time,event.values[0])
            count += 1 
        html_block2 += '''</table>'''
        

    html_block2 += '''
        </body>
    </html>'''
    
    # replace the unknown colspan with the actual max colspan based on number of workshops
    html_block2=html_block2.replace('<td colspan="UNKNOWN"','<td colspan="{}"'.format(max_colspan))
    f = file(current_conference_id+'/schedule.html','w')
    f.write(html_block2)
    f.close()


#### MEDIA PAGE ####
media_path = 'media.txt'
media_df = pd.DataFrame.from_csv(media_path,header=0, \
                        sep=';', index_col = None, parse_dates = ['media_date'])
media_sorted = media_df.sort('media_date',ascending=False)
html_media = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Media</title>
        <link rel="stylesheet" href="../wordpress_testing/css/scheduletable.css" type="text/css" media="screen, projection">
    </head>
    <body>
    <table class=tg-table-paper style="width:100%;text-align:left">
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

f = file('wordpress_testing/media.html','w')
f.write(html_media)
f.close()