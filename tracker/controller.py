#!/usr/bin/env python

import track_fish
from tracker.tcp_client import FishClient
from tracker.fish_tank import Tank
from tools import fishlog

import argparse
import os


# TODO:
# - create seperate log file for each fish
# - insert fish client send and test with feeder
# -


class Controller:
    def __init__(self, cb_obj=None, name=['test']):
        global total_feed
        global time_counter
        total_feed = 0
        time_counter = 0

        self.cb_obj = cb_obj

        width = track_fish.init_tracking()

        # init logger
        full_script_path = '{}{}'.format(os.path.dirname(os.path.realpath(__file__)), '/')
        full_root_script_path = full_script_path[:full_script_path.find('tracker')]
        log_folder = '{}data/log/'.format(full_root_script_path)
        #print('log:{}'.format(log_folder))
        #print_and_update_main_log('log:{}'.format(log_folder))
        self.logger = []

        #init tank
        self.tank = []
        id = 0
        for size in width:
            self.tank.append(Tank(id, size))
            self.logger.append(fishlog.FishLog(log_folder, "{}.({})".format(name[id], str(id))))
            id = id + 1

    def do(self, x, y, fish_id):
        global total_feed

        self.logger[fish_id].add_tracked_point(x, y)
        feed_side = self.tank[fish_id].decide(x)

        #self.time_count()

        if feed_side is not None:
            total_feed += 1
            str_to_print = '{}\t,{}\t - \tTotal:{}'.format(fish_id, feed_side, total_feed)

            if self.cb_obj is not None:
                self.cb_obj.print_and_update_main_log(str_to_print)
            fish_client = FishClient()
            fish_client.send(fish_id + 1, feed_side)
            fish_client.kill()

            #fish_client.send(fish_id, feed_side)
            self.logger[fish_id].add_feed(feed_side)

    def time_count(self):
        global time_counter
        print(time_counter)


# ap = argparse.ArgumentParser()
# ap.add_argument("-log", "--log", required=True, help="path to log folder")
# args = vars(ap.parse_args())
if __name__ == '__main__':
    controller = Controller()
    track_fish.track_loop(controller)

