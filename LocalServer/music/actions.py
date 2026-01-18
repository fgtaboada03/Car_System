import json

def music_action(controller, payload):
    data = json.loads(payload)
    action = data["action"]

    match action:
        case 1:
            update = controller.start_song(data)

        case 2:
            update = controller.start_playlist(data)

        case 3:
            update = controller.queue_song(data, up_next=False)

        case 4:
            update = controller.queue_song(data, up_next=True)

        case 5:
            update = controller.queue_playlist(data, up_next=False)

        case 6:
            update = controller.queue_playlist(data, up_next=True)

        case 7:
            update = controller.reorder_songs(data)

        case 8:
            update = controller.delete_song(data)

        case 9:
            update = controller.adjust_cur_time(data)

        case 10:
            update = controller.adjust_volume(data)

        case 11:
            update = controller.toggle_playback()

        case 12:
            update = controller.skip_reverse()

        case 13:
            update = controller.skip_forward()

        case 14:
            update = controller.skip_forward_x(data["x"])

        case 15:
            update = controller.skip_reverse_x(data["x"])

        case _:
            raise ValueError(f"Unknown action: {action}")
    return update
