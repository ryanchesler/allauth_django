# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from operator import itemgetter

# @login_required
def home(request):

    cursor = connection.cursor()
    friend_info = []
    if request.user.username :
        user_name = request.user.username
    else:
        user_name = "user30"

    cursor.execute("SELECT * FROM socialaccount_socialaccount ss, auth_user user "
                   "WHERE ss.user_id=user.id AND user.username='"+user_name+"' ")

    try:

        row = cursor.fetchone()
        uid = row[2]
        steam_url = uid.split("id/")
        steam_id = steam_url[2]


        url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=575D6F2C240C96CB1ADB5122D6675BF2&steamid="+steam_id+"&relationship=friend"
        friends = requests.get(url)
        friends =  friends.json()

        if bool(friends):
            for friend in friends.get('friendslist').get('friends'):
                gamers = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=575D6F2C240C96CB1ADB5122D6675BF2&steamids='"+friend.get('steamid')+"'")
                gamers = gamers.json()
                for gamer in gamers.get("response").get('players'):
                    friend_info.append({
                        'friend_name': gamer.get('personaname'),
                        'avatar': gamer.get('avatar'),
                        'steam_id': friend.get('steamid')
                    })

    except Exception, error:
        print error

    friend_info = sorted(friend_info, key=itemgetter('friend_name'))

    return render(request, 'home.html', {'friend_info': friend_info, 'steam_id': steam_id})

def games(request):


    if request.method == 'POST':
        game_list = []

        steam_id_list = request.POST.getlist('steam_id_list')
        user_steam_id = request.POST.get('steam_id')
        steam_id_list.append(user_steam_id)

        i=0
        for steamid in steam_id_list:

            games = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=575D6F2C240C96CB1ADB5122D6675BF2&include_appinfo=1&steamid="+steamid+"&format=json")
            games = games.json()



            if bool(games):

                for game in games.get('response').get('games'):

                    if any(d['name'] == game.get('name') for d in game_list):
                        for gl in game_list:
                            if gl.get('name') == game.get('name'):

                                sid_list = gl.get('steam_id')
                                sid_list.append(steamid)
                                gl.update({'count': gl.get('count')+1, 'steam_id': sid_list})


                    else:
                        img_logo_url = "http://media.steampowered.com/steamcommunity/public/images/apps/"+str(game.get('appid'))+"/"+str(game.get('img_logo_url'))+".jpg"
                        img_icon_url = "http://media.steampowered.com/steamcommunity/public/images/apps/"+str(game.get('appid'))+"/"+str(game.get('img_icon_url'))+".jpg"


                        game_list.append({
                            'name': game.get('name'),
                            'count': 1,
                            'img_logo_url': img_logo_url,
                            'img_icon_url': img_icon_url,
                            'appid': game.get('appid'),
                            'steam_id': [steamid]
                        })



            i += 1

        newlist = sorted(game_list, key=itemgetter('count'), reverse=True)

        alist = []
        games = []
        i = 0
        store_steam_info = []

        for nlist in newlist:

            friend_info = []


            if any(d['steam_id'] == nlist.get('steam_id') for d in store_steam_info):
                for ssi in store_steam_info:
                    if ssi['steam_id'] == nlist.get('steam_id'):
                        # import pdb;pdb.set_trace()
                        friend_info = ssi.get('friend_info')
            else:
                gamers = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=575D6F2C240C96CB1ADB5122D6675BF2&steamids='"+str(nlist.get('steam_id'))+"'")
                gamers = gamers.json()
                for gamer in gamers.get("response").get('players'):
                    friend_info.append({
                        'friend_name': gamer.get('personaname'),
                        'avatar': gamer.get('avatar')
                    })
                store_steam_info.append({
                    'steam_id': nlist.get('steam_id'),
                    'friend_info': friend_info
                })


            if ((newlist[i].get('count') == newlist[i - 1].get('count')) and i!=0):

                nlist['friend_info'] = friend_info
                games.append(nlist)

                for a in alist:
                    if a.get('count') == nlist.get('count'):
                        a.update({'games': games})
            else:
                games = []
                nlist['friend_info'] = friend_info
                games.append(nlist)
                alist.append({
                    'count': nlist.get('count'),
                    'games': games
                })

            i += 1



        return render(request, 'games.html', {'game_list': alist})

def friends(request):
    return render(request, 'friends.html')
