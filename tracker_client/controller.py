#!/usr/bin/env python

import track_fish2
from tracker_client.fish_client import FishClient
from tracker_client.fish_tank import Tank
from tools import fishlog
import argparse
import os


# TODO:
# - create seperate log file for each fish
# - insert fish client send and test with feeder
# -


class Controller:
    def __init__(self, name='test'):
        width = track_fish2.init_tracking()

        # init logger
        full_script_path = '{}{}'.format(os.path.dirname(os.path.realpath(__file__)), '/')
        full_root_script_path = full_script_path[:full_script_path.find('tracker_client')]
        log_folder = '{}data/log/'.format(full_root_script_path)
        print('log:{}'.format(log_folder))
        self.logger = fishlog.FishLog(log_folder, name)

        #init tank
        self.tank = []
        id = 0
        for size in width:
            self.tank.append(Tank(id, size))
            id = id + 1

    def do(self,x,y,fish_id):
        self.logger.add_tracked_point(x, y)
        feed_side = self.tank[fish_id].decide(x)
        if feed_side is not None:
            print(feed_side, fish_id)
            #fish_client.send(fish_id, feed_side)
            self.logger.add_feed(feed_side)


# ap = argparse.ArgumentParser()
# ap.add_argument("-log", "--log", required=True, help="path to log folder")
# args = vars(ap.parse_args())
controller = Controller()
track_fish2.track_loop(controller)
