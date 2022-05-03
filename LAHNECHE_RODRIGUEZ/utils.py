import numpy as np
import math


def get_SAD(left_matrix, right_matrix):
    """ 
    Return the dissimilarity between 2 parts (2 matrices) of 2 images.
    The dissimilarity is calculated according to the SAD formula.

    Args:
        left_image(np.ndarray): 2D array representing an image in gray.
        right_image(np.ndarray): 2D array representing an image in gray.
        left_pixel_considered(tuple): coordinates of the left pixel considered as center
            of the first matrix from left image.
        right_pixel_considered(tuple): coordinates of the left pixel considered as center
            of the first matrix from right image.
        neighbourhood(int): number of pixels considered in the neighbourhood for SAD formula.

    Returns:
        dissimilarity(int): dissimilarity calculated between the 2 parts.
    """

    dissimilarity = np.sum(
        np.abs(
            np.subtract(
                left_matrix,
                right_matrix,
                dtype="float"
            )
        )
    )

    return dissimilarity


def get_MSE(left_matrix, right_matrix):
    """ 
    Return the dissimilarity between 2 parts (2 matrices) of 2 images.
    The dissimilarity is calculated according to the SAD formula.

    Args:
        left_image(np.ndarray): 2D array representing an image in gray.
        right_image(np.ndarray): 2D array representing an image in gray.
        left_pixel_considered(tuple): coordinates of the left pixel considered as center
            of the first matrix from left image.
        right_pixel_considered(tuple): coordinates of the left pixel considered as center
            of the first matrix from right image.
        neighbourhood(int): number of pixels considered in the neighbourhood for SAD formula.

    Returns:
        dissimilarity(int): dissimilarity calculated between the 2 parts.
    """

    dissimilarity = np.mean(
        np.square(
            np.subtract(
                left_matrix,
                right_matrix,
                dtype="float"
            )
        )
    )

    return dissimilarity


def get_SSD(left_matrix, right_matrix):
    """ 
    Return the dissimilarity between 2 parts (2 matrices) of 2 images.
    The dissimilarity is calculated according to the SAD formula.

    Args:
        left_image(np.ndarray): 2D array representing an image in gray.
        right_image(np.ndarray): 2D array representing an image in gray.
        left_pixel_considered(tuple): coordinates of the left pixel considered as center
            of the first matrix from left image.
        right_pixel_considered(tuple): coordinates of the left pixel considered as center
            of the first matrix from right image.
        neighbourhood(int): number of pixels considered in the neighbourhood for SAD formula.

    Returns:
        dissimilarity(int): dissimilarity calculated between the 2 parts.
    """

    dissimilarity = np.sum(
        np.square(np.abs(
            np.subtract(
                left_matrix,
                right_matrix,
                dtype="float"
            )
        ))

    )

    return dissimilarity


def get_disparity(left_image, right_image, left_pixel_considered, neighbourhood, maxdisp):
    """
    Get the disparity for one point in the left image to his conjugated in the right image.

    Args:
        left_image(np.ndarray): 2D array representing an image in gray.
        right_image(np.ndarray): 2D array representing an image in gray.
        left_pixel_considered(tuple): coordinates of a point in left_image we want to
            get his disparity with the right image.
        neighbourhood(int): number of pixels considered in the neighbourhood for SAD formula.
        maxdisp(int): max disparity observed between the 2 images.
        order(string): oreder of the movement. Choice between left and right.

    Returns:
        disparity(int): disparity of the left_point_considered with the right image.
    """
    left_matrix = left_image[
        left_pixel_considered[0]-neighbourhood//2:left_pixel_considered[0]+neighbourhood//2+1,
        left_pixel_considered[1]-neighbourhood//2:left_pixel_considered[1]+neighbourhood//2+1
    ]
    right_matrix = right_image[
        left_pixel_considered[0]-neighbourhood//2:left_pixel_considered[0]+neighbourhood//2+1,
        left_pixel_considered[1]-neighbourhood//2:left_pixel_considered[1]+neighbourhood//2+1
    ]
    min_dissimilarity = get_SSD(
        left_matrix,
        right_matrix,
    )

    disparity = 0
    ranges = np.arange(1, maxdisp)
    for i in range(1, maxdisp):
        left_matrix = left_image[
            left_pixel_considered[0]-neighbourhood//2:left_pixel_considered[0]+neighbourhood//2+1,
            left_pixel_considered[1]-neighbourhood//2:left_pixel_considered[1]+neighbourhood//2+1
        ]
        right_matrix = right_image[
            left_pixel_considered[0]-neighbourhood//2:left_pixel_considered[0]+neighbourhood//2+1,
            left_pixel_considered[1]-i-neighbourhood//2:left_pixel_considered[1]-i+neighbourhood//2+1
        ]
        try:
            dissimilarity = get_SSD(
                left_matrix,
                right_matrix,
            )
        except:
            pass

        if dissimilarity < min_dissimilarity:
            min_dissimilarity = dissimilarity
            disparity = i

    return disparity


def filtre_mode(carre):
    vals, counts = np.unique(carre[carre != 0].flatten(), return_counts=True)
    return vals[np.argmax(counts)]


def apply_filtre_mode(disp):
    N = 15
    new_disp = np.zeros(disp.shape)
    for i in range(disp.shape[0]):
        for j in range(disp.shape[1]):
            if disp[i, j] != 0:
                new_disp[i, j] = filtre_mode(disp[max(i-math.floor(N/2), 0):min(i+math.floor(N/2)+1, disp.shape[0]),
                                                  max(j-math.floor(N/2), 0):min(j+math.floor(N/2)+1, disp.shape[1])])
    return new_disp


def get_disparity_map(left_image, right_image, neighbourhood, maxdisp):
    """ Get the disparity map between 2 images

        Args:
            left_image(np.ndarray): 2D array representing an image in gray.
            right_image(np.ndarray): 2D array representing an image in gray.
            neighbourhood(int): number of pixels considered in the neighbourhood for SAD formula.
            maxdisp(int): max disparity observed between the 2 images.
            order(string): oreder of the movement. Choice between left and right.

        Returns:
            disparity_map(np.ndarray): disparity map between the 2 images
    """

    disparity_map = np.zeros(left_image.shape[0:2])
    for row in range(neighbourhood, disparity_map.shape[0]-neighbourhood):
        for col in range(neighbourhood, disparity_map.shape[1]-neighbourhood):
            disparity_map[row, col] = get_disparity(
                left_image,
                right_image,
                (row, col),
                neighbourhood,
                maxdisp,
            )

    disparity_map = apply_filtre_mode(disparity_map)

    return disparity_map
