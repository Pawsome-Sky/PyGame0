import pygame
import random
from enemy_data import ENEMY_SPAWN_DATA

HEALTH = 100
MONEY = 650


class World():
    def __init__(self, data, original_map_width, original_map_height, map_width, map_height):
        self.level = 1
        self.game_speed = 1
        self.health = HEALTH
        self.money = MONEY
        self.tile_map = []
        self.waypoints = []
        self.map_data = data
        self.original_map_width = original_map_width
        self.original_map_height = original_map_height
        self.map_width = map_width
        self.map_height = map_height
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def process_data(self):
        # Scaling factors
        scale_x = self.map_width / self.original_map_width  # Use your original map's width
        scale_y = self.map_height / self.original_map_height  # Use your original map's height

        # Look through data to extract relevant info
        for layer in self.map_data["layers"]:
            # Extracting the main tilemap
            if layer["name"] == "Tilemap":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data, scale_x, scale_y)

        # Ensure tile_map exists and is valid
        if not hasattr(self, "tile_map") or not self.tile_map:
            print("Error: Tilemap layer not found or empty!")

    def process_waypoints(self, data, scale_x, scale_y):
        # Iterate through waypoints to extract sets of x and y coordinates
        for point in data:
            temp_x = point.get("x") * scale_x
            temp_y = point.get("y") * scale_y
            self.waypoints.append((temp_x, temp_y))

    def process_enemies(self):
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        # Now randomize the list to shuffle the enemies
        random.shuffle(self.enemy_list)

    def check_level_complete(self):
        if (self.killed_enemies + self.missed_enemies) == len(self.enemy_list):
            return True

    def reset_level(self):
        # Reset enemy variables
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0
