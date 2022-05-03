import time
from skimage import io
import sys
from utils import get_disparity_map


def main(left_image, right_image, returned_disparity):

    Ig = io.imread(left_image)
    Id = io.imread(right_image)

    start_time = time.time()
    disparity_map = get_disparity_map(Ig, Id, 7, 70)
    disparity_map = disparity_map.astype("uint8") * 4
    end_time = time.time() - start_time

    if returned_disparity != "sans-sortie":
        print(
            "----------- La carte des dispartiés est en cours d'enregistrement -----------")
        io.imsave(fname=returned_disparity, arr=disparity_map)
        print(
            f"----------- La carte des disparités nommée {returned_disparity} est bien enregistrée -----------")

    else:
        print(f"L'algorithme de Block Matching s'est effectué en {end_time} s")


if __name__ == '__main__':
    assert len(sys.argv) == 4, "Il faut 3 arguments : evaldisp.py img_gche.png img_dte.png disparite_estimee.png (ou sans-sortie)"

    main(sys.argv[1], sys.argv[2], sys.argv[3])
