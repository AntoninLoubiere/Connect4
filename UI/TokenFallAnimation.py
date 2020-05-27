import tkinter.tix

NUMBER_UPDATE_PER_SECOND = 100
TIME_ANIMATION = 0.75


class TokenFallAnimation(object):
    """
    The class of animation of the fall of tokens
    """

    def __init__(self, final_x, final_y, player, game_panel):
        """
        Constructor
        :param final_x: the final x coord
        :param final_y: the final y coord
        :param game_panel: link to panel class
        :param player: The player which own this token
        """

        self.final_x = final_x
        self.final_y = final_y
        self.current_height = -game_panel.token_square_size

        self.game_panel = game_panel
        self.player = player

        self.final_coord = self.game_panel.get_square_coord(final_x, final_y)

        self.id = self.game_panel.grid_canvas.create_image(
            self.final_coord[0][0], self.current_height, image=self.game_panel.ui.image_getter.save_token_photos[player]
            [self.game_panel.players[player].token], anchor=tkinter.tix.NW
        )
        self.animation_update()

    def animation_update(self):
        """
        On tick update
        :return: None
        """
        y_speed = self.game_panel.get_square_coord(
            0, self.game_panel.game.grid_height)[0][1] / (NUMBER_UPDATE_PER_SECOND * TIME_ANIMATION)
        # second

        if self.final_coord[0][1] > self.current_height + y_speed:
            self.game_panel.grid_canvas.move(self.id, 0, y_speed)
            self.current_height = self.game_panel.grid_canvas.coords(self.id)[1]

        else:
            self.game_panel.update_image(self.final_x, self.final_y)
            self.game_panel.on_end_animation(self.player)
            self.game_panel.remove_token_animation(self)
            return None

        self.game_panel.after(int(1000 / NUMBER_UPDATE_PER_SECOND * TIME_ANIMATION), self.animation_update)

    def on_remove(self):
        """
        When the animation is remove
        :return: None
        """
        self.game_panel.grid_canvas.delete(self.id)

    def set_current_height(self, current_height):
        """
        set the current height
        :param current_height: the current height
        :return: None
        """
        self.game_panel.grid_canvas.move(self.id, 0, current_height)
        self.current_height = current_height
