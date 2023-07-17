import argparse
import os
import numpy as np

def polar_to_cartesian(ranges, azimuths, elevations):
    # 将角度转换为弧度
    azimuths_rad = np.radians(azimuths)
    elevations_rad = np.radians(elevations)

    # 计算XYZ坐标
    x = ranges * np.cos(elevations_rad) * np.cos(azimuths_rad)
    y = ranges * np.cos(elevations_rad) * np.sin(azimuths_rad)
    z = ranges * np.sin(elevations_rad)

    # 组合X、Y和Z坐标成矩阵
    coords = np.column_stack((x, y, z))

    return coords.astype(np.float32)

# def get_radar_xyzv(radar_file):
#     points = np.fromfile(radar_file, dtype=np.float64).reshape(-1, 8)
#     ranges = points[:, 2]
#     azimuths = points[:, 5]
#     elevations = points[:, 6]
#     coords_xyz = polar_to_cartesian(ranges, azimuths, elevations)
#     doppler_velocity_raw = points[:,3]
#     xyzv = np.column_stack((coords_xyz, doppler_velocity_raw))
#     return xyzv
def get_radar_xyz(radar_file):
    points = np.fromfile(radar_file, dtype=np.float64).reshape(-1, 8)
    ranges = points[:, 2]
    azimuths = points[:, 5]
    elevations = points[:, 6]
    coords_xyz = polar_to_cartesian(ranges, azimuths, elevations)
    return coords_xyz

def xyz_loader(radar_file):
    data = np.fromfile(radar_file, dtype=np.float32).reshape(-1, 8)
    return data[:, :3]