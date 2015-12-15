#!/usr/bin/env python

from math import pi
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from Tkinter import *
from tkFileDialog import askopenfilename
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from bokeh.plotting import figure, show, output_notebook, output_file, ColumnDataSource
from bokeh.palettes import Spectral10, Reds9
from bokeh.models import Range1d, HoverTool


class App:
    def __init__(self, master):
    	column0_padx = 24
        row_pady = 36

        self.filename = '2015-05.csv'
        self.data = pd.DataFrame()
        self.userdata = pd.DataFrame()

        self.btn_ChooseFile = Button(master, text = "Choose file", width = 25, command = self.ChooseFile)
        self.btn_LoadData = Button(master, text = "Load Data", width = 25, command = self.LoadData)
        self.btn_ShowUsage = Button(master, text = "Show Usage", width = 25, command = self.ShowUsage)
        self.btn_ShowUsers = Button(master, text = "Show Users with usages >=", width = 25, command = self.ShowUsers)
        self.Rank = Entry(master)
        self.btn_LoadUserData = Button(master, text="Load Data for User:", width = 25, command = self.LoadUserData)
        self.uid = Entry(master)
        self.btn_HabitsRecord = Button(master, text="User's Habits Record", width = 25, command = self.HabitsRecord)
        self.btn_HabitsCompSkipRecord = Button(master, text="User's Habits Complete/Skip Record", width = 30, command = self.HabitsCompSkipRecord)
        self.btn_HabitsCompSkipRecord_W = Button(master, text="User's Habits Complete/Skip Record in weeks", 
            width = 35, command = self.HabitsCompSkipRecord_W)

        self.btn_ChooseFile.grid(row = 0, column = 0, pady = 12, sticky = 'w', padx = column0_padx)
        self.btn_LoadData.grid(row = 0, column = 1, pady = 12, sticky = 'w', padx = column0_padx)
        self.btn_ShowUsage.grid(row = 0, column = 2, pady = 12, sticky = 'w', padx = column0_padx)
        self.btn_ShowUsers.grid(row = 1, column = 0, pady = 12, sticky = 'w', padx = column0_padx)
        self.Rank.grid(row = 1, column = 1, pady = 12, sticky = 'w', padx = column0_padx)
        self.btn_LoadUserData.grid(row = 2, column = 0, pady = 12, sticky = 'w', padx = column0_padx)
        self.uid.grid(row=2, column=1, pady = 12, sticky='w', padx = column0_padx)
        self.btn_HabitsRecord.grid(row = 3, column = 0, pady = 12, sticky = 'w', padx = column0_padx)
        self.btn_HabitsCompSkipRecord.grid(row = 3, column = 1, pady = 12, sticky = 'w', padx = column0_padx)
        self.btn_HabitsCompSkipRecord_W.grid(row = 3, column = 2, pady = 12, sticky = 'w', padx = column0_padx)

    def ChooseFile(self):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        if filename[-4:] != '.csv':
            print "Please choose a '.csv' file"
            print "Or the program will try to load file '" + self.filename + "' in the current folder"
        else:
            self.filename = filename
            print("====== csv file to be loaded: " + self.filename + " ======")

    def LoadData(self):
    	print 'loading data, please wait'
    	fname = self.filename
    	df00 = pd.read_csv(fname,low_memory=False)
    	df00.rename(columns={df00.columns[0]:'event'}, inplace=True)
    	# print df00.columns[0]
    	
    	t = df00.property_time
    	print 'data started at ' + datetime.fromtimestamp(min(t)).strftime('%Y-%m-%d %H:%M:%S') + \
    	', ended at ' + datetime.fromtimestamp(max(t)).strftime('%Y-%m-%d %H:%M:%S')
    	
    	namelist = pd.read_csv('./useful_column_names.txt')
    	useful_column_names = [n[1:-1] for n in namelist['useful_column_names']]
    	df01 = df00[useful_column_names]
    	self.data = df01
    	del df00
    	del df01
    	print '='*20

    def ShowUsage(self):
    	print '-'*20
    	print 'showing the usage informaiton for this dataset'
    	df01 = self.data
    	uid = df01['property_userId'];
    	print 'total number of usage = %d' %len(uid)
    	print 'total number of users = %d' %len(set(uid))
    	uidRank = pd.DataFrame(uid.value_counts())
    	uidRank.reset_index(inplace = True)
    	uidRank.columns = ['userID','num']
    	print 'top users are:'
    	print uidRank.head()

    	f, axarr = plt.subplots(2, sharex=False)
    	p1 = axarr[0].hist(np.clip(uidRank.num, 0, 100), bins = 10)
    	axarr[0].set_xlim(0,100)
    	axarr[0].set_ylabel('Number of users')
    	# axarr[0].set_xlabel('Number of users')
    	axarr[0].set_title('Number of usages')
    	p2 = axarr[1].hist(np.clip(uidRank.num, 100, 3000), bins = 10)
    	axarr[1].set_xlim(100, 2100)
    	axarr[1].set_ylim(0, p2[0][1]*1.1)
    	axarr[1].set_ylabel('Number of users')
    	axarr[1].set_xlabel('Number of usages')
    	plt.show()

    def ShowUsers(self):
        df01 = self.data
        uid = df01['property_userId'];
        uidRank = pd.DataFrame(uid.value_counts())
        uidRank.reset_index(inplace = True)
        uidRank.columns = ['userID','num']

        N_usage = int(self.Rank.get())
        # print N_usage
        select_uid = uidRank[uidRank.num >= N_usage].tail(10).userID
        print uidRank[uidRank.num >= N_usage].tail(10)


    def LoadUserData(self):
    	select_uid = self.uid.get()
    	# print select_uid
        df01 = self.data
        df_user = df01[df01['property_userId'] == select_uid]
        self.userdata = df_user
        print 'data for user ' + select_uid + ' have been loaded.'

    def HabitsRecord(self):
        df_user = self.userdata
        df_tmp = df_user[['property_lastHabitAdded','property_lastHabitAddedDate']].dropna()
        hbt_add = df_tmp.property_lastHabitAdded
        hbt_add_time = df_tmp.property_lastHabitAddedDate
        idx = [list(hbt_add_time).index(n) for n in set(hbt_add_time)]

        tmp = list(hbt_add)
        user_habit_added = [tmp[n] for n in sorted(idx)]
        # print 'this user added %d habits.' %len(user_habit_added)
        print 'this user added %d habits. (%d unique ones)' %(len(user_habit_added), len(set(user_habit_added)))
        if len(user_habit_added) <= 20:
            print user_habit_added

        tmp = list(hbt_add_time)
        t_habit_added = [tmp[n] for n in sorted(idx)]
        if len(t_habit_added) <= 20:
            print 'this user added those habits on:'
            print t_habit_added
        t_habit_added = [datetime.strptime(n, '%Y-%m-%dT%H:%M:%S') for n in t_habit_added]
        # dates = [datetime.strptime(n, '%Y-%m-%dT%H:%M:%S') for n in df02.SkippedDate.values if n[0] == '2']
        # print t_habit_added

        OneDay = timedelta(hours=24, minutes=0, seconds=0)
        
        output_file("Hbts_Added_Rec_uid_" + self.uid.get() + ".html", title="Habits Comp/Skip Record")
        p = figure(title = 'Number of added habits',
                   tools="pan, wheel_zoom, hover, save, reset",
                   plot_width=800, plot_height=300,
                   x_axis_type = "datetime")
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Number of habits'

        hover = p.select(dict(type=HoverTool))

        hover.tooltips = [
            ('#','@num'),
            ("Habit", "@habits"),
            ("Time added","@dates_disp")
            ]

        dates_list = list(t_habit_added)
        source = ColumnDataSource(
                    data = dict(
                        habits = list(user_habit_added),
                        num = range(1,len(t_habit_added)+1),
                        dates = dates_list,
                        dates_disp = [str(n) for n in dates_list]
                        )
                    )

        p.line(x = 'dates', y = 'num', source = source, color = 'black', line_width=2)
        p.circle(x = 'dates', y = 'num', source = source, color = 'black', fill_color = 'white', size=8)

        x_left_lim = dates_list[0] - OneDay
        x_right_lim = dates_list[-1] + OneDay
        p.set(x_range=Range1d(x_left_lim, x_right_lim))
        p.xaxis.major_label_orientation = pi/4
        show(p)

    def HabitsCompSkipRecord(self):
        df_user = self.userdata

        df_tmp = df_user[['property_lastHabitCompleted','property_lastHabitCompletedDate']].dropna()
        hbt_cmp = df_tmp.property_lastHabitCompleted
        hbt_cmp_time = df_tmp.property_lastHabitCompletedDate
        df_tmp = df_user[['property_lastHabitSkipped','property_lastHabitSkippedDate']].dropna()
        hbt_skp = df_tmp.property_lastHabitSkipped
        hbt_skp_time = df_tmp.property_lastHabitSkippedDate

        idx = [list(hbt_cmp_time).index(n) for n in set(hbt_cmp_time)]
        idx = sorted(idx)
        user_habit_completed = [list(hbt_cmp)[n] for n in idx]
        t_habit_completed = [list(hbt_cmp_time)[n] for n in idx]
        t_habit_completed = [datetime.strptime(n, '%Y-%m-%dT%H:%M:%S') for n in t_habit_completed]

        idx = [list(hbt_skp_time).index(n) for n in set(hbt_skp_time)]
        idx = sorted(idx)
        user_habit_skipped = [list(hbt_skp)[n] for n in idx]
        t_habit_skipped = [list(hbt_skp_time)[n] for n in idx]
        t_habit_skipped = [datetime.strptime(n, '%Y-%m-%dT%H:%M:%S') for n in t_habit_skipped]

        df_habit_completed = pd.DataFrame({'habit_completed': user_habit_completed,
                                     'habit_completed_date': t_habit_completed})
                                    # 'completed':1})
        df_habit_skipped = pd.DataFrame({'habit_skipped': user_habit_skipped,
                                     'habit_skipped_date': t_habit_skipped})
                                    # 'skipped':0.95})

        print df_habit_completed.head()
        print df_habit_skipped.head()

        output_file("Hbts_Cmp_Skp_Rec_ByDay_uid_" + self.uid.get() + ".html", title="Habits Comp/Skip Record")
        
        habit_list = list(df_habit_completed.habit_completed) + list(df_habit_skipped.habit_skipped)
        dates_list = list(df_habit_completed.habit_completed_date) + list(df_habit_skipped.habit_skipped_date)

        if len(set(habit_list)) > 20:
            print 'there are to many habits records, showing only habits (%d) that had been skipped' \
            %len(set(list(df_habit_skipped.habit_skipped)))
            yRange = list(set(list(df_habit_skipped.habit_skipped)))
        else:
            yRange = list(set(habit_list))

        PlotHeight = 400*(len(set(list(df_habit_skipped.habit_skipped)))/20 + 1)

        p = figure(title = 'Habits completed   and skipped  ',
                   tools="pan, wheel_zoom, hover, save, reset",
                   plot_width=800, plot_height=PlotHeight,
                   y_range = yRange,
                   x_axis_type = "datetime")
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Habit'

        hover = p.select(dict(type=HoverTool))

        hover.tooltips = [
            ("Habit", "@habits"),
            ("Action", '@action'),
            ("Time","@dates_disp")
            ]

        source = ColumnDataSource(
                    data = dict(
                        habits = habit_list,
                        action = ['Completed']*len(df_habit_completed) + ['Skipped']*len(df_habit_skipped),
                        color = ['green']*len(df_habit_completed) + ['red']*len(df_habit_skipped),
                        dates = dates_list,
                        dates_disp = [str(n) for n in dates_list]
                        )
                    )

        p.circle(x = 'dates', y = 'habits', source = source, color = 'color', fill_alpha=0.5, size=10)
        p.xaxis.major_label_orientation = pi/4
        show(p)

    def HabitsCompSkipRecord_W(self):
        df_user = self.userdata

        df_tmp = df_user[['property_lastHabitCompleted','property_lastHabitCompletedDate']].dropna()
        hbt_cmp = df_tmp.property_lastHabitCompleted
        hbt_cmp_time = df_tmp.property_lastHabitCompletedDate
        df_tmp = df_user[['property_lastHabitSkipped','property_lastHabitSkippedDate']].dropna()
        hbt_skp = df_tmp.property_lastHabitSkipped
        hbt_skp_time = df_tmp.property_lastHabitSkippedDate

        idx = [list(hbt_cmp_time).index(n) for n in set(hbt_cmp_time)]
        idx = sorted(idx)
        user_habit_completed = [list(hbt_cmp)[n] for n in idx]
        t_habit_completed = [list(hbt_cmp_time)[n] for n in idx]
        t_habit_completed = [datetime.strptime(n, '%Y-%m-%dT%H:%M:%S') for n in t_habit_completed]

        idx = [list(hbt_skp_time).index(n) for n in set(hbt_skp_time)]
        idx = sorted(idx)
        user_habit_skipped = [list(hbt_skp)[n] for n in idx]
        t_habit_skipped = [list(hbt_skp_time)[n] for n in idx]
        t_habit_skipped = [datetime.strptime(n, '%Y-%m-%dT%H:%M:%S') for n in t_habit_skipped]

        df_habit_completed = pd.DataFrame({'habit_completed': user_habit_completed,
                                     'habit_completed_date': t_habit_completed})
                                    # 'completed':1})
        df_habit_skipped = pd.DataFrame({'habit_skipped': user_habit_skipped,
                                     'habit_skipped_date': t_habit_skipped})
                                    # 'skipped':0.95})

        print df_habit_completed.head()
        print df_habit_skipped.head()

        output_file("Hbts_Cmp_Skp_Rec_ByWeek_uid_" + self.uid.get() + ".html", title="Habits Comp/Skip Record")

        habit_list = list(df_habit_completed.habit_completed) + list(df_habit_skipped.habit_skipped)
        print len(set(habit_list))
        dates_list = list(df_habit_completed.habit_completed_date) + list(df_habit_skipped.habit_skipped_date)
        wkdy = [n.weekday() for n in dates_list]

        Weekdays_dic = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday',
                       5: 'Saturday', 6: 'Sunday'}

        weekdays_map = pd.Series(wkdy).map(Weekdays_dic);

        if len(set(habit_list)) > 20:
            print 'there are to many habits, showing only habits that had been skipped'
            yRange = list(set(list(df_habit_skipped.habit_skipped)))
        else:
            yRange = list(set(habit_list))

        PlotHeight = 400*(len(set(list(df_habit_skipped.habit_skipped)))/20 + 1)

        p = figure(title = 'Habits completed and skipped',
                   tools="pan, wheel_zoom, hover, save, reset",
                   plot_width=800, plot_height=400,
                   y_range = yRange,
                   x_range = list(Weekdays_dic.values())
        #            x_axis_type = "datetime"
                  )
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Habit'

        hover = p.select(dict(type=HoverTool))

        hover.tooltips = [
            ("Habit", "@habits"),
            ("Action", '@action'),
        #     ("Time","@dates_disp"),
            ("Time","@weekdays")
            ]

        source = ColumnDataSource(
                    data = dict(
                        habits = habit_list,
                        action = ['Completed']*len(df_habit_completed) + ['Skipped']*len(df_habit_skipped),
                        color = ['green']*len(df_habit_completed) + ['red']*len(df_habit_skipped),
                        dates = dates_list,
                        dates_disp = [str(n) for n in dates_list],
                        weekdays = weekdays_map,
                        )
                    )

        p.circle(x = 'weekdays', y = 'habits', source = source, color = 'color', fill_alpha=0.5, size=10)
        p.xaxis.major_label_orientation = pi/4
        show(p)


if __name__ == '__main__':
    root = Tk()
    root.title("CSV Data Plotting Tool v0.4")
    root.minsize(800, 400)
    app = App(root)
    root.mainloop()

