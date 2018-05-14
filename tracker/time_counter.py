
import datetime


class TimeCounter:

    def __init__(self):

        self.start_time = datetime.datetime.now()
        [self.t_hr, self.t_min, self.t_sec] =self.start_time.hour,self.start_time.minute,self.start_time.second

        self.old_t_hr = self.t_hr
        self.old_t_min = self.t_min
        self.old_t_sec = self.t_sec

        str_time_start = datetime.datetime.now()

    def get_time_str(self):
        #global str_time_start, str_time, old_str_time

        old_t_sec = self.t_sec
        [self.t_hr, self.t_min, self.t_sec] = datetime.now().hour, datetime.now().minute, datetime.now().second
        str_to_return = 0
        if not old_t_sec == self.t_sec:
            str_to_return = "{0}:{1}.{2}".format(self.t_hr, self.t_min, self.t_sec)

        return str_to_return

    def get_time_diff(self):
        now_time = datetime.datetime.now()

        old_t_sec = self.t_sec
        [self.t_hr, self.t_min, self.t_sec] = now_time.hour, now_time.minute, now_time.second
        str_to_return = 0
        if not old_t_sec == self.t_sec:
            hr_diff = self.t_hr - self.old_t_hr
            min_diff = self.t_min - self.old_t_min
            sec_diff = self.t_sec - self.old_t_sec

            str_to_return = datetime.timedelta(hours=hr_diff, minutes=min_diff, seconds=sec_diff)

        return str_to_return

    def make_two_digit_num(int_to_check):
        str_temp = '{}'.format(int_to_check)
        if int_to_check < 10: str_temp = '0{}'.format(int_to_check)
        return str_temp

