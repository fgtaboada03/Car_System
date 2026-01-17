import json

def music_action(controller, payload):
    data = json.loads(payload)
    action = data["action"]

    match action:
        case 1:
            controller.start_song(data)

        case 2:
            controller.start_playlist(data)

        case 3:
            controller.queue_song(data, up_next=False)

        case 4:
            controller.queue_song(data, up_next=True)

        case 5:
            controller.queue_playlist(data, up_next=False)

        case 6:
            controller.queue_playlist(data, up_next=True)

        case 7:
            controller.reorder_songs(data)

        case 8:
            controller.delete_song(data)

        case 9:
            controller.adjust_cur_time(data)

        case 10:
            controller.adjust_volume(data)

        case 11:
            controller.toggle_playback()

        case 12:
            controller.skip_reverse()

        case 13:
            controller.skip_forward()

        case 14:
            controller.skip_forward_x(data["x"])

        case 15:
            controller.skip_reverse_x(data["x"])

        case _:
            raise ValueError(f"Unknown action: {action}")
