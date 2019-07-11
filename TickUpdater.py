import threading
import time


NUMBER_UPDATE_PER_SECOND = 100


class TickUpdater(threading.Thread):
    """
    A class which update the UI
    """

    def __init__(self, ui):
        """
        Constructor
        :param ui: the ui to update
        """
        super().__init__()
        self.ui = ui

    def run(self) -> None:
        """
        Run the update
        :return: None
        """
        time_last_second = time.time()
        number_update = 0

        while self.ui.is_alive:
            if time_last_second + 1 < time.time():
                time_last_second = time.time()
                if number_update < NUMBER_UPDATE_PER_SECOND:
                    print("WARNING: {} tick(s) skip !".format(str(NUMBER_UPDATE_PER_SECOND - number_update)))
                number_update = 0

            elif number_update >= NUMBER_UPDATE_PER_SECOND:
                print("Terminate, " + str(time_last_second + 1 - time.time()) + " second(s) remaining")
                time.sleep(time_last_second + 1 - time.time())
                continue

            else:
                time.sleep((time_last_second + 1 - time.time()) / (NUMBER_UPDATE_PER_SECOND - number_update))
                if self.ui.is_alive:
                    self.ui.tick_update()
                number_update += 1