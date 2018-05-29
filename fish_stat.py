#! /usr/bin/python2.4

from __future__ import print_function
#from calendar import monthrange
from datetime import datetime, timedelta
import os,time
import sys
import datetime
#import re
#import collections

sys.stdout.write('')
sys.stdout.flush()

#toolbar_width = 40


def my_range(start, end, step):
    while start >= end:
        yield start
        start += step

def show_last_day(year,month):
    from calendar import monthrange
    tmp = monthrange(year, month)
    return tmp[1]

def get_information(directory, days_back, int_relevant_input):
    now = datetime.datetime.now()

        #d_today=(now.year,now.month,now.day)
        #d_first=(2017,9,1)
        #d_last=(2017,9,3)
        #if d_last>d_today>d_first:
        #    print("ok")
        #else:
        #    print("not")

    if int_relevant_input==2: #if choosen 'show' so ask which fish to show
        fish_numbers=raw_input("Enter fish number(s) you wish to see    (100 103 106 .. or 101,103,106):\n\t")
        s=''
        fish_user_relevant_list = []
        for ch in [',']:
            if ch in fish_numbers:
                fish_numbers = fish_numbers.replace(ch, ' ')
        # print ("f_n=", fish_numbers)
        for s in fish_numbers.split():
            if s.isdigit():
                if int(s) not in fish_user_relevant_list:
                    fish_user_relevant_list.append(int(s))
                # print ("s=",s)
        # print (fish_relevant_list)
        if fish_user_relevant_list == []: int_relevant_input = 1

    file_list = []
    fish_traning_database=[]
	
    print_header=False
    last_printed_day=(0,0,0)
    printing_date_from=(2112,12,31)
    printing_date_till=(0,0,0)
    #printing_days=[[31,12],[0,0]]

    toolbar_width=40
    files_count=len(os.listdir(directory))

    progress_bar_count1=files_count
    progress_bar_count2=0
    p_b_div=files_count/toolbar_width
    #print(p_b_div)
    if p_b_div == 0: p_b_div=1
    toolbar_width =files_count/p_b_div
    # setup toolbar
    sys.stdout.write("\t[%s]" % (" " * toolbar_width))
    str_to_add="       (" + str(files_count) + " files)"
    sys.stdout.write(str_to_add)
    sys.stdout.flush()
    sys.stdout.write("\b" * (len(str_to_add)+(toolbar_width+1))) # return to start of line, after '['

    date_today=(now.year, now.month, now.day)
    date_from_raw=str(datetime.date.today() - timedelta(days_back))

    date_from=tuple([int(i) for i in date_from_raw.split("-")])

    for file_name in sorted(os.listdir(directory)):
        if progress_bar_count1>0:
            progress_bar_count2+=1
            #print("(p_b_count/p_b_div)%toolbar_width",end='')
            #print((p_b_count/p_b_div)%toolbar_width)
            if progress_bar_count2==p_b_div:
                sys.stdout.write("-")
                sys.stdout.flush()
                progress_bar_count2=0
            progress_bar_count1-=1
        a = os.stat(os.path.join(directory,file_name))
        file_name_year = file_name[:4]
        file_name_month = file_name[5:7]
        file_name_day = file_name[8:10]

        if file_name_year.isdigit() :
            date_to_check=(int(file_name_year),int(file_name_month),int(file_name_day))

            if date_today>=date_to_check>=date_from:    #date criteria

                day_word_place=((file_name.split())[1].split("_"))[1].lower().find("day")
                dot_sign_place=((file_name.split())[1].split("_"))[1].find(".")
                fish_no=((file_name.split())[1].split("_"))[1][1:day_word_place]
                traning_day_for_fish=((file_name.split())[1].split("_"))[1][day_word_place+3:dot_sign_place]

                if not fish_no == '':  # fish_no.isdigit():
                    if not last_printed_day==date_to_check:
                        last_printed_day=date_to_check
                        print_header=True
                        if printing_date_from>=date_to_check:
                            printing_date_from=date_to_check
                        if printing_date_till<=date_to_check:
                            printing_date_till=date_to_check

                    document_text = open(directory+'/'+file_name, 'r')
                    text_string = document_text.read().lower().split()
				
                    feeds_counter=0
                    bool_print=False
                    first_word=False
                    fish_note=''
                    fish_traning_time_start=0
                    fish_traning_time_end=0
					
                    for word in text_string:
                        word_lower=word

                        if word_lower=="feed": 
                            feeds_counter+= 1
                        if bool_print:
                            if first_word==True:
                                fish_note=fish_note + " " + word[word.find("(")+1:]
                            else:
                                fish_note=fish_note + " " + word
                            if word.find(")")!=-1: # end of note
                                bool_print=False
                                fish_note=fish_note[:len(fish_note)-1]
                        if word_lower=="note":
                            bool_print=True
                            first_word=True
                    fish_record = [fish_no, int(traning_day_for_fish), int(feeds_counter), [int(file_name_year),int(file_name_month),int(file_name_day)], file_name, fish_note, fish_traning_time_start, fish_traning_time_end]
                    fish_traning_database.append(fish_record)

    print ("")
    relevant_fish=[]
    j=0
    old_date=0
    last_printed_day=0

    for item in sorted(fish_traning_database, key=lambda date: date[3], reverse=True):  # Auto find relevant fish
        if old_date == 0: old_date = item[3][2]
        if item[3][2] != old_date:  # Save the oldest date from DB
            old_date = item[3][2]
            # print("Old Date:" + str(old_date))
            j += 1
        if j < 2:  # Definding relevant fish from 2 last tranings
            # print("Rel:" + str(item[0]))
            if item[0] not in relevant_fish: relevant_fish.append(item[0])

    if int_relevant_input == 1:
        for item in sorted(fish_traning_database):
            if item[0] in relevant_fish:
                print('', end='')
                # do nothing
            else:
                fish_traning_database.remove(item)
                # remove it


    if int_relevant_input==2:
        for item in sorted(fish_traning_database):
            if item[0] in fish_user_relevant_list:
                print('',end='')
                # do nothing
            else:
                fish_traning_database.remove(item)
                # remove it

        print("Printing ",days_back, " days back", end='')


    if int_relevant_input==1:
        print ("\t\t Relevant fish->", end='')
        print(sorted(relevant_fish), end='')

    if int_relevant_input==2:
        print ("\t\t Relevant fish (user)->", end='')
        print(sorted(fish_user_relevant_list), end='')

    print("\n")

    if fish_traning_database:

        print ("Fish no.\tFile name\t\t\t\tfeed count\tnote")
        # fish_traning_database[][]=(fish_no), (traning_day_for_fish), (feeds_counter), [(file_name_year),(file_name_month),(file_name_day)], file_name, fish_note]
        for item in sorted(fish_traning_database,  key=lambda func:(func[3], func[0]) ): #show->[date, fish_num, file_name, feeds]
            date_day=item[3][2]
            date_month=item[3][1]
            date_year=item[3][0]
            fish_num=item[0]
            feeds_count=item[2]
            file_name=item[4]
            fish_note=item[5]

            if not last_printed_day==date_day:
                last_printed_day=date_day
                str_for_banner="  " + str(date_day) + "/" + str(date_month)
                if int(date_day)==now.day and int(date_month)==now.month and int(date_year)==now.year:
                    str_for_banner+="    (today)"
                    # print(" today", end='')
                else:
                    if int(date_day)==now.day-1 and int(date_month)==now.month and int(date_year)==now.year: str_for_banner+="    (yesterday)" #print(" yesterday", end='')
                str_for_banner+="  "
                print("   ",end='')
                print(banner(str_for_banner, ch='-', length=85))
            print (fish_num, end='')
            print ("\t\t", end='')
            print (file_name, end='')
            print ("\t\t", end='')
            print (feeds_count, end='')
            if len(fish_note)>0:
                print ("\t\t", end='')
                print (fish_note)
            else:
                print("")

        print ("")

        print ("SUM --> Sorted by fish:", end='')
        print ("  (Dates:  ", end='')
        print (printing_date_from[2], end='')
        print ( "/" , end='')
        print (printing_date_from[1] ,end='')
        if printing_date_from!=printing_date_till :
            print (" - " , end='')
            print (printing_date_till[2] , end='')
            print ("/" , end='')
            print (printing_date_till[1], end='')
            print (") ", end='')

        if int_relevant_input==1:
            print ("\t Relevant fish->", end='')
            print(sorted(relevant_fish), end='')

        if int_relevant_input==2:
            print ("\t Relevant fish (user)->", end='')
            print(sorted(fish_user_relevant_list), end='')

        print("\n")



        print ("Fish no.\t\tTraning days\t\tDays showing\t\tTotal feed count\t\t\tAvg per day\t\t")
        print(banner(None, ch='-', length=100))


        fish_num=sorted(fish_traning_database)[0][0]

        #print("fish_num=", fish_num, end='')
        print(fish_num, end='')
        total_feed_count=0
        days_in_traning=0
        days_showing=0
        for item in sorted(fish_traning_database):
            if fish_num!=item[0]:
                #print(" total_feed_count=", total_feed_count, end='')
                #print(" days_showing=", days_showing,end='')
                #print(" days_in_traning=", days_in_traning, end='')
                #print(" avg_per_day=", total_feed_count/days_showing)

                print("\t\t", days_in_traning, end='')
                print("\t\t", days_showing,end='')
                print("\t\t", total_feed_count, end='')
                print("\t\t\t", total_feed_count/days_showing)

                fish_num=item[0]
                print(fish_num, end='')
                total_feed_count=0
                days_in_traning=0
                days_showing=0
            days_showing+=1
            total_feed_count=total_feed_count+item[2]
            days_in_traning=max(days_in_traning,item[1])
        #print(" total_feed_count=", total_feed_count,end='')
        #print(" days_showing=", days_showing,end='')
        #print(" days_in_traning=", days_in_traning, end='')
        #print(" avg_per_day=", total_feed_count/days_showing)
        print("\t\t", days_in_traning, end='')
        print("\t\t", days_showing,end='')
        print("\t\t", total_feed_count, end='')
        print("\t\t\t", total_feed_count/days_showing)
        print("")
        #print (printing_days)
    else:
        str_for_banner=" NO DATA"
        print(banner(str_for_banner, ch='-', length=85))
        print("")
    return file_list

def get_int(prompt):
    while True:
        try:
            input_var=raw_input(prompt)
            #print (type(input_var))
            #print ("len=", len(input_var))
            if len(input_var)==0:
                print('0', end='')
                input_var='0'
            return int(input_var)
        except ValueError:
            print ("Thats not an integer, silly!")

def query_yes_no_show(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"show":2, "s": 2, "yes": 1, "y": 1, "ye": 1,
             "no": 0, "n": 0}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        #sys.stdout.write(question + prompt)
        #sys.stdout.write(question)
        print(question, end='')
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' or 's' "
                             "(or 'y' or 'n').\n")

def banner(text, ch='=', length=78):
    """Return a banner line centering the given text.

        "text" is the text to show in the banner. None can be given to have
            no text.
        "ch" (optional, default '=') is the banner line character (can
            also be a short string to repeat).
        "length" (optional, default 78) is the length of banner to make.

    Examples:
        >>> banner("Peggy Sue")
        '================================= Peggy Sue =================================='
        >>> banner("Peggy Sue", ch='-', length=50)
        '------------------- Peggy Sue --------------------'
        >>> banner("Pretty pretty pretty pretty Peggy Sue", length=40)
        'Pretty pretty pretty pretty Peggy Sue'
    """
    if text is None:
        return ch * length
    elif len(text) + 2 + len(ch)*2 > length:
        # Not enough space for even one line char (plus space) around text.
        return text
    else:
        remain = length - (len(text) + 2)
        prefix_len = remain / 2
        suffix_len = remain - prefix_len
        if len(ch) == 1:
            prefix = ch * prefix_len
            suffix = ch * suffix_len
        else:
            prefix = ch * (prefix_len/len(ch)) + ch[:prefix_len%len(ch)]
            suffix = ch * (suffix_len/len(ch)) + ch[:suffix_len%len(ch)]
        return prefix + ' ' + text + ' ' + suffix

def main(dir='', int_days_input=100, int_relevant_input=1):
    #print("How many days back? ", end='')
    #int_days_input=get_int('')
    #int_relevant_input=query_yes_no_show("\tPrint relevant only (last trained)?\t\t Y / N(All) / S(show only->)")
    arguments = sys.argv
    dir = arguments[1]
    int_days_input = int(arguments[2])
    int_relevant_input = int(arguments[3])
    print ('dir={}, days={}, rel={}'.format(dir, int_days_input, int_relevant_input))

    #dir = "/Users/talzoor/Documents/FishLabInfo/log"
    get_information(dir, int_days_input, int_relevant_input)


if __name__ == '__main__':
    main()

