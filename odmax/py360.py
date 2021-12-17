# original code py360convert from https://github.com/sunset1995/py360convert
import numpy as np
from . import utils

def c2e(cubemap, h, w, mode='bilinear', cube_format='dice'):
    """
    Convert cubemap to equirectangular spherical array

    :param cubemap: ND-array or list of ND-arrays, cubemap to project
    :param h: height
    :param w: width
    :param mode: str, interpolation method (default: "bilinear")
    :param cube_format: str, way the cubemap is organised (default: "dice")
    :return: ND-array [M, N, 3] with equirectangular image
    """
    if mode == 'bilinear':
        order = 1
    elif mode == 'nearest':
        order = 0
    else:
        raise NotImplementedError('unknown mode')

    if cube_format == 'horizon':
        pass
    elif cube_format == 'list':
        cubemap = utils.cube_list2h(cubemap)
    elif cube_format == 'dict':
        cubemap = utils.cube_dict2h(cubemap)
    elif cube_format == 'dice':
        cubemap = utils.cube_dice2h(cubemap)
    else:
        raise NotImplementedError('unknown cube_format')
    assert len(cubemap.shape) == 3
    assert cubemap.shape[0] * 6 == cubemap.shape[1]
    assert w % 8 == 0
    face_w = cubemap.shape[0]

    uv = utils.equirect_uvgrid(h, w)
    u, v = np.split(uv, 2, axis=-1)
    u = u[..., 0]
    v = v[..., 0]
    cube_faces = np.stack(np.split(cubemap, 6, 1), 0)

    # Get face id to each pixel: 0F 1R 2B 3L 4U 5D
    tp = utils.equirect_facetype(h, w)
    coor_x = np.zeros((h, w))
    coor_y = np.zeros((h, w))

    for i in range(4):
        mask = (tp == i)
        coor_x[mask] = 0.5 * np.tan(u[mask] - np.pi * i / 2)
        coor_y[mask] = -0.5 * np.tan(v[mask]) / np.cos(u[mask] - np.pi * i / 2)

    mask = (tp == 4)
    c = 0.5 * np.tan(np.pi / 2 - v[mask])
    coor_x[mask] = c * np.sin(u[mask])
    coor_y[mask] = c * np.cos(u[mask])

    mask = (tp == 5)
    c = 0.5 * np.tan(np.pi / 2 - np.abs(v[mask]))
    coor_x[mask] = c * np.sin(u[mask])
    coor_y[mask] = -c * np.cos(u[mask])

    # Final renormalize
    coor_x = (np.clip(coor_x, -0.5, 0.5) + 0.5) * face_w
    coor_y = (np.clip(coor_y, -0.5, 0.5) + 0.5) * face_w

    equirec = np.stack([
        utils.sample_cubefaces(cube_faces[..., i], tp, coor_y, coor_x, order=order)
        for i in range(cube_faces.shape[3])
    ], axis=-1)

    return equirec

def e2c(e_img, face_w=256, mode='bilinear', cube_format='dice', overlap=0.):
    """
    Convert equirectangular spherical array to cubemap

    :param e_img: ND-array [M, N, 3], equirectangular image to project
    :param face_w: int, amount of pixels per face (default: 256)
    :param mode: str, interpolation method (default: "bilinear")
    :param cube_format: str, way the cubemap is organised (default: "dice")
    :param overlap: fractional overlap allowed between each face. Useful to generate overlap in photogrammetry applications
    :return: ND-array [M, N, 3] with equirectangular image
    """
    assert len(e_img.shape) == 3
    h, w = e_img.shape[:2]
    if mode == 'bilinear':
        order = 1
    elif mode == 'nearest':
        order = 0
    else:
        raise NotImplementedError('unknown mode')

    xyz = utils.xyzcube(face_w, overlap=overlap)
    uv = utils.xyz2uv(xyz)
    coor_xy = utils.uv2coor(uv, h, w)

    cubemap = np.stack([
        utils.sample_equirec(e_img[..., i], coor_xy, order=order)
        for i in range(e_img.shape[2])
    ], axis=-1)

    if cube_format == 'horizon':
        pass
    elif cube_format == 'list':
        cubemap = utils.cube_h2list(cubemap)
    elif cube_format == 'dict':
        cubemap = utils.cube_h2dict(cubemap)
    elif cube_format == 'dice':
        cubemap = utils.cube_h2dice(cubemap)
    else:
        raise NotImplementedError()

    return cubemap

def e2p(e_img, fov_deg, u_deg, v_deg, out_hw, in_rot_deg=0, mode='bilinear'):
    """
    retrieve perspective image from provided equirectangular image

    :param e_img: ND-array [H, W, 3], equirectangular image
    :param fov_deg: float or (float, float) field of view in degree
    :param u_deg: float, horizon viewing angle in range [-180, 180]
    :param v_deg: float, vertical viewing angle in range [-90, 90]
    :param out_hw: tuple of ints (height, width) in pixels
    :param in_rot_deg: in plane rotation
    :param mode: str, interpolation method (default: "bilinear")
    :return:
    """
    assert len(e_img.shape) == 3
    h, w = e_img.shape[:2]

    try:
        h_fov, v_fov = fov_deg[0] * np.pi / 180, fov_deg[1] * np.pi / 180
    except:
        h_fov, v_fov = fov, fov
    in_rot = in_rot_deg * np.pi / 180

    if mode == 'bilinear':
        order = 1
    elif mode == 'nearest':
        order = 0
    else:
        raise NotImplementedError('unknown mode')

    u = -u_deg * np.pi / 180
    v = v_deg * np.pi / 180
    xyz = utils.xyzpers(h_fov, v_fov, u, v, out_hw, in_rot)
    uv = utils.xyz2uv(xyz)
    coor_xy = utils.uv2coor(uv, h, w)

    pers_img = np.stack([
        utils.sample_equirec(e_img[..., i], coor_xy, order=order)
        for i in range(e_img.shape[2])
    ], axis=-1)

    return pers_img


