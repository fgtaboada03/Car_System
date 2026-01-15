from player import Player

player = Player()

cases = {
    1: player.start_song,
    2: player.start_playlist,
    3: (player.queue_song, False),
    4: (player.queue_song, True),
    5: (player.queue_playlist, False),
    6: (player.queue_song, True),
    7: player.reorder_songs,
    8: player.delete_song,
    9: player.adjust_cur_time,
    10: player.adjust_volume,
    11: player.toggle_playback,
    12: player.skip_reverse,
    13: player.skip_forward
}

def action(msg):
    data = msg.properties.json()
    action = data["action"]
    func = cases[action]

    if (len(func) == 2):
        func[0](msg, func[1])

    n_parameter_funcs = 10

    if (action > n_parameter_funcs):
        func()
    else:
        func(data) 
