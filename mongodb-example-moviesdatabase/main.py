import WebUI

import os
import configparser
from flask import Flask, render_template, request, redirect, url_for, session
from Database import Database
from User import User
from UserState import UserState




if __name__ == "__main__":
    WebUI.run()
    # user = Database.read_user("Marc")
    # user_state = UserState(user)
    # print(user_state)
