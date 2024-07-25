"""
This the primary class for the Mario Expert agent. It contains the logic for the Mario Expert agent to play the game and choose actions.

Your goal is to implement the functions and methods required to enable choose_action to select the best action for the agent to take.

Original Mario Manual: https://www.thegameisafootarcade.com/wp-content/uploads/2017/04/Super-Mario-Land-Game-Manual.pdf
"""

import json
import logging
import math
import random

import cv2
from mario_environment import MarioEnvironment
from pyboy.utils import WindowEvent


class MarioController(MarioEnvironment):
    """
    The MarioController class represents a controller for the Mario game environment.

    You can build upon this class all you want to implement your Mario Expert agent.

    Args:
        act_freq (int): The frequency at which actions are performed. Defaults to 10.
        emulation_speed (int): The speed of the game emulation. Defaults to 0.
        headless (bool): Whether to run the game in headless mode. Defaults to False.
    """

    def __init__(
        self,
        act_freq: int = 1,
        emulation_speed: int = 2,
        headless: bool = False,
    ) -> None:
        super().__init__(
            act_freq=act_freq,
            emulation_speed=emulation_speed,
            headless=headless,
        )

        self.act_freq = act_freq

        # Example of valid actions based purely on the buttons you can press
        valid_actions: list[WindowEvent] = [
            WindowEvent.PRESS_ARROW_DOWN,
            WindowEvent.PRESS_ARROW_LEFT,
            WindowEvent.PRESS_ARROW_RIGHT,
            WindowEvent.PRESS_ARROW_UP,
            WindowEvent.PRESS_BUTTON_A,
            WindowEvent.PRESS_BUTTON_B,
        ]

        release_button: list[WindowEvent] = [
            WindowEvent.RELEASE_ARROW_DOWN,
            WindowEvent.RELEASE_ARROW_LEFT,
            WindowEvent.RELEASE_ARROW_RIGHT,
            WindowEvent.RELEASE_ARROW_UP,
            WindowEvent.RELEASE_BUTTON_A,
            WindowEvent.RELEASE_BUTTON_B,
        ]

        self.valid_actions = valid_actions
        self.release_button = release_button

    def run_action(self, actions: []) -> None:
        """
        This is a very basic example of how this function could be implemented

        As part of this assignment your job is to modify this function to better suit your needs

        You can change the action type to whatever you want or need just remember the base control of the game is pushing buttons
        """

        tick = 0
        # Simply toggles the buttons being on or off for a duration of act_freq
        for action in actions:
            self.pyboy.send_input(self.valid_actions[action[0]])
            self.pyboy.tick()

        #for _ in range(self.act_freq):

        while len(actions) > 0:
#            input()

            self.pyboy.tick()
            print(tick)
            tick = tick + 1

            for action in actions:
                print("Check Action:", action, tick)
                if action[1] <= tick:
                    print("End Action", action)
                    self.pyboy.send_input(self.release_button[action[0]])
                    actions.remove(action)

class MarioExpert:
    """
    The MarioExpert class represents an expert agent for playing the Mario game.

    Edit this class to implement the logic for the Mario Expert agent to play the game.

    Do NOT edit the input parameters for the __init__ method.

    Args:
        results_path (str): The path to save the results and video of the gameplay.
        headless (bool, optional): Whether to run the game in headless mode. Defaults to False.
    """

    def __init__(self, results_path: str, headless=False):
        self.results_path = results_path

        self.environment = MarioController(headless=headless)

        self.video = None

    def choose_action(self):
        state = self.environment.game_state()
        frame = self.environment.grab_frame()
        game_area = self.environment.game_area()

        print(game_area)

        y_val = len(game_area)
        actions = []
        que = []
        enemies = []
        closest_vec_obj = float('inf')
        closest_vec_enemy = float('inf')
        closest_obj = -1
        closest_enemy = -1
        mario_pos = -1

        for y in game_area:
            y_val = y_val - 1
            x_val = 0
            for x in y:
                x_val = x_val + 1
                if x == 1:

                    mario_pos = [x_val + 1, y_val - 1]

                    if mario_pos[0] == 17 or mario_pos[1] == 17:
                        actions.append([2, 20])
                        return actions

                    y_val = len(game_area)

                    for y in game_area:
                        y_val = y_val - 1
                        x_val = 0
                        for x in y:
                            x_val = x_val + 1
                            distance = math.sqrt((x_val - mario_pos[0]) ** 2 + (y_val - mario_pos[1]) ** 2)
                            value = x

                            if value != 10 and value != 14 and value != 1 and value != 0 and y_val < mario_pos[1] or value != 0 and value != 1 and y_val >= mario_pos[1] or value == 0 and y_val == 0:
                                if value == 15 or value == 16 or value == 18:
                                    if distance < closest_vec_enemy:
                                        closest_vec_enemy = distance
                                        print("Closest enemy vec:", distance)
                                        closest_enemy = len(enemies)

                                    if x_val - mario_pos[0] < 0:
                                        distance = distance * -1

                                    enemies.append([value, x_val, y_val, distance])

                                else:
                                    if x_val - mario_pos[0] < 0:
                                        distance = distance * -1

                                    if 0 < distance < closest_vec_obj:
                                        closest_vec_obj = distance
                                        print("Closest obj vec:", distance)
                                        closest_obj = len(que)
                                        print("Closest Distance:", closest_obj)

                                    que.append([value, x_val, y_val, distance])

                    print("Mario:", mario_pos)
                    if len(que) > 0:
                        print("Que:", que)
                        print("Real Distance:", que[closest_obj][3])
                        print("Closest Value:", que[closest_obj][0])

                    if len(enemies) > 0:
                        print("Enemy Que:", enemies)
                        print("Real Distance:", enemies[closest_enemy][3])
                        print("Closest Value:", enemies[closest_enemy][0])
                    break
            else:
                continue
            break

        if len(enemies) > 0:
            if enemies[closest_enemy][0] == 15:
                if 4 > enemies[closest_enemy][3] > 1 and enemies[closest_enemy][2] == mario_pos[1] and game_area[len(game_area) - mario_pos[1]][mario_pos[0] - 1] == 10 and enemies[closest_enemy][1] > mario_pos[0] or game_area[len(game_area) - mario_pos[1]][mario_pos[0] - 1] == 10 and 6 > enemies[closest_enemy][3] and enemies[closest_enemy][2] < mario_pos[1] and enemies[closest_enemy][1] > mario_pos[0] or game_area[len(game_area) - mario_pos[1]][mario_pos[0]] == 14 and 6 > enemies[closest_enemy][3] and enemies[closest_enemy][2] < mario_pos[1] and enemies[closest_enemy][1] > mario_pos[0]:
                    print("Attack Right")
                    actions.append([2, 6])
                    actions.append([5, 6])
                    actions.append([4, 2])
                if 4 > enemies[closest_enemy][3] > 1 and enemies[closest_enemy][2] == mario_pos[1] and game_area[len(game_area) - mario_pos[1]][mario_pos[0] - 1] == 10 and enemies[closest_enemy][1] < mario_pos[0] or game_area[len(game_area) - mario_pos[1]][mario_pos[0] - 1] == 10 and 6 > enemies[closest_enemy][3] and enemies[closest_enemy][2] < mario_pos[1] and enemies[closest_enemy][1] < mario_pos[0] or game_area[len(game_area) - mario_pos[1]][mario_pos[0]] == 14 and 6 > enemies[closest_enemy][3] and enemies[closest_enemy][2] < mario_pos[1] and enemies[closest_enemy][1] < mario_pos[0]:
                    print("Attack Left")
                    actions.append([2, 6])
                    actions.append([5, 6])
                    actions.append([4, 2])
                elif enemies[closest_enemy][3] <= 3 and enemies[closest_enemy][2] > mario_pos[1] or enemies[closest_enemy][3] < 2 and enemies[closest_enemy][2] == mario_pos[1] or enemies[closest_enemy][3] < 2 and enemies[closest_enemy][1] == mario_pos[0] + 1:
                    print("Run Away")
                    actions.append([1, 10])
                    actions.append([5, 10])
                elif enemies[closest_enemy][1] < mario_pos[0] and enemies[closest_enemy][2] < mario_pos[1] and 1 < enemies[closest_enemy][3] < 4:
                    print("Left On Top")
                    actions.append([1, 2])
                    actions.append([5, 2])

                elif enemies[closest_enemy][1] > mario_pos[0] and enemies[closest_enemy][2] < mario_pos[1] and 1 < enemies[closest_enemy][3] < 4:
                    print("Right On Top")
                    actions.append([2, 2])
                    actions.append([5, 2])

            if enemies[closest_enemy][0] == 16:
                if 4 > enemies[closest_enemy][3] and enemies[closest_enemy][2] == mario_pos[1] and game_area[len(game_area) - mario_pos[1]][mario_pos[0]] == 10 and enemies[closest_enemy][1] > mario_pos[0]:
                    print("Attack Right")
                    actions.append([5, 6])
                    actions.append([2, 6])
                    actions.append([4, 6])
                elif 4 > enemies[closest_enemy][3] and enemies[closest_enemy][2] == mario_pos[1] and game_area[len(game_area) - mario_pos[1]][mario_pos[0]] == 10 and enemies[closest_enemy][1] < mario_pos[0]:
                    print("Attack Left")
                    actions.append([5, 6])
                    actions.append([1, 6])
                    actions.append([4, 6])
                elif enemies[closest_enemy][3] < 3 and enemies[closest_enemy][2] > mario_pos[1] or enemies[closest_enemy][3] < 2 and enemies[closest_enemy][2] == mario_pos[1] or enemies[closest_enemy][3] < 2 and enemies[closest_enemy][1] == mario_pos[0] + 1:
                    print("Run Away")
                    actions.append([1, 10])
                    actions.append([5, 10])
                elif enemies[closest_enemy][1] < mario_pos[0] and enemies[closest_enemy][2] < mario_pos[1] and enemies[closest_enemy][3] < 3:
                    print("Left On Top")
                    actions.append([1, 3])
                    actions.append([5, 3])

                elif enemies[closest_enemy][1] > mario_pos[0] and enemies[closest_enemy][2] < mario_pos[1] and enemies[closest_enemy][3] < 3:
                    print("Right On Top")
                    actions.append([2, 3])
                    actions.append([5, 3])

            if enemies[closest_enemy][0] == 18:
                if 3 > enemies[closest_enemy][3] and enemies[closest_enemy][2] == mario_pos[1] and \
                        game_area[len(game_area) - mario_pos[1]][mario_pos[0]] == 10:
                    print("Attack")
                    actions.append([5, 6])
                    actions.append([2, 6])
                    actions.append([4, 10])
                elif enemies[closest_enemy][3] < 5 and enemies[closest_enemy][2] > mario_pos[1] or \
                        enemies[closest_enemy][3] < 2 and enemies[closest_enemy][2] == mario_pos[1] or \
                        enemies[closest_enemy][3] < 2 and enemies[closest_enemy][1] == mario_pos[0] + 1:
                    print("Run Away")
                    actions.append([1, 10])
                    actions.append([5, 10])
                elif enemies[closest_enemy][1] < mario_pos[0] and enemies[closest_enemy][2] < mario_pos[1] and \
                        enemies[closest_enemy][3] < 3:
                    print("Left On Top")
                    actions.append([1, 3])
                    actions.append([5, 3])

                elif enemies[closest_enemy][1] > mario_pos[0] and enemies[closest_enemy][2] < mario_pos[1] and \
                        enemies[closest_enemy][3] < 3:
                    print("Right On Top")
                    actions.append([2, 3])
                    actions.append([5, 3])

            elif len(actions) == 0:
                for enemy in enemies:
                    print("here", enemy)
                    if enemy[1] < mario_pos[0] and enemy[2] < mario_pos[1] and enemy[3] < 3:
                        print("Left On Top")
                        actions.append([1, 3])
                        actions.append([5, 3])

                    elif enemy[1] > mario_pos[0] and enemy[2] < mario_pos[1] and enemy[3] < 3:
                        print("Right On Top")
                        actions.append([2, 3])
                        actions.append([5, 3])

                    elif enemy[1] == mario_pos[0] and enemy[2] < mario_pos[1] and enemy[3] < 3:
                        print("Drop Down")
                        actions.append([0, 10])
                        actions.append([1, 3])
                        actions.append([2, 3])
                        actions.append([5, 3])

        if len(que) > 0 and len(actions) == 0:
            for obj in que:
                if obj[0] == 0 and 0 < obj[1] - mario_pos[0] < 2:
                    print("Jump")
                    actions.append([5, 6])
                    actions.append([2, 15])
                    actions.append([4, 15])

            if len(actions) == 0:

                if que[closest_obj][0] == 14:
                    if que[closest_obj][3] < 3 and (que[closest_obj][1] - mario_pos[0]) >= 0:
                        actions.append([1, 20])
                    elif que[closest_obj][3] == 3:
                        print("Jump")
                        actions.append([2, 8])
                        actions.append([4, 13])

                elif que[closest_obj][0] == 10:
                    if que[closest_obj][3] < 2 and (que[closest_obj][1] - mario_pos[0]) >= 0 and game_area[mario_pos[0] - 1][mario_pos[1] - 1] != 0 and game_area[mario_pos[0] + 1][mario_pos[1] - 2] == 10:
                        print("Walk Back")
                        actions.append([1, 20])
                    elif que[closest_obj][3] < 3:
                        print("Jump")
                        actions.append([2, 8])
                        actions.append([4, 13])

        if len(actions) == 0:
            actions.append([2, 1])

        # Implement your code here to choose the best action
        # time.sleep(0.1)
        #return random.randint(0, len(self.environment.valid_actions) - 1)
        return actions

    def step(self):
        """
        Modify this function as required to implement the Mario Expert agent's logic.

        This is just a very basic example
        """

        # Choose an action - button press or other...
        action = self.choose_action()

        # Run the action on the environment
        self.environment.run_action(action)

    def play(self):
        """
        Do NOT edit this method.
        """
        self.environment.reset()

        frame = self.environment.grab_frame()
        height, width, _ = frame.shape

        self.start_video(f"{self.results_path}/mario_expert.mp4", width, height)

        while not self.environment.get_game_over():
            frame = self.environment.grab_frame()
            self.video.write(frame)

            self.step()

        final_stats = self.environment.game_state()
        logging.info(f"Final Stats: {final_stats}")

        with open(f"{self.results_path}/results.json", "w", encoding="utf-8") as file:
            json.dump(final_stats, file)

        self.stop_video()

    def start_video(self, video_name, width, height, fps=30):
        """
        Do NOT edit this method.
        """
        self.video = cv2.VideoWriter(
            video_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
        )

    def stop_video(self) -> None:
        """
        Do NOT edit this method.
        """
        self.video.release()
