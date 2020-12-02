"""Module for training starting"""

import glob
from typing import List, Tuple

from modules.data.dataset import Dataset
from modules.network.hopfield import HopfieldNetwork
from modules.utils.plots import plot_images_compare

from config import Config


def get_trained_model(image_paths: List[str],
                      image_size: Tuple[int, int] = (256, 256),
                      asynchronous: bool = True) -> HopfieldNetwork:
    dataset = Dataset(list_of_paths=image_paths, image_size=image_size)
    flatten_images = dataset.get_all_flatten_images()

    model = HopfieldNetwork(train_data=flatten_images, asynchronous=asynchronous)
    model.train()

    return model


def evaluation(model: HopfieldNetwork,
               image_paths: List[str],
               image_size: Tuple[int, int] = (256, 256),
               num_iter: int = 20,
               threshold: int = 50):

    dataset_original = Dataset(list_of_paths=image_paths,
                               image_size=image_size,
                               add_noise=False)
    flatten_images_original = dataset_original.get_all_flatten_images()

    predictions = model.predict(data=flatten_images_original,
                                num_iter=num_iter,
                                threshold=threshold)

    data = {
        'original_image': flatten_images_original,
        'prediction_image': predictions
    }

    return data


if __name__ == '__main__':
    image_paths_train = glob.glob(pathname='images_diff/train/*.*', recursive=True)
    image_paths_test = glob.glob(pathname='images_diff/test/*.*', recursive=True)

    model = get_trained_model(image_paths=image_paths_train,
                              image_size=Config.image_size,
                              asynchronous=Config.asynchronous)

    data = evaluation(model=model,
                      image_paths=image_paths_test,
                      image_size=Config.image_size,
                      num_iter=Config.num_iter,
                      threshold=Config.threshold)

    plot_images_compare(data=data)
