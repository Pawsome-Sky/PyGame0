import pygame


class World():
    def __init__(self, data, original_map_width, original_map_height, map_width, map_height):
        self.waypoints = []
        self.map_data = data
        self.original_map_width = original_map_width
        self.original_map_height = original_map_height
        self.map_width = map_width
        self.map_height = map_height

    def process_data(self):
        # Scaling factors
        scale_x = self.map_width / self.original_map_width  # Use your original map's width
        scale_y = self.map_height / self.original_map_height  # Use your original map's height

        # Look through data to extract relevant info
        for layer in self.map_data["layers"]:
            if layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data, scale_x, scale_y)

    def process_waypoints(self, data, scale_x, scale_y):
        # Iterate through waypoints to extract sets of x and y coordinates
        for point in data:
            temp_x = point.get("x") * scale_x
            temp_y = point.get("y") * scale_y
            self.waypoints.append((temp_x, temp_y))
