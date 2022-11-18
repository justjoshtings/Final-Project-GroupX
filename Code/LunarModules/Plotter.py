"""
Plotter.py
Object to handle all processing of images/data.

author: @saharae, @justjoshtings
created: 11/12/2022
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from LunarModules.ImageProcessor import ImageProcessor
import seaborn as sns
import os
import random
import cv2
import copy

# WILL NEED TO CLEAN THIS WHOLE MESS UP LATER!!!

class Plotter:
    '''
    Object to handle plotting of images.
    '''
    def __init__(self, log_file=None):
        '''
        Params:
            self: instance of object
            log_file (str): default is None to not have logging, otherwise, specify logging path ../filepath/log.log

        '''
    
    #Sanity check, view few mages
    def peek_images(self, sample_images, sample_masks=None, encode=None, color_scale=None, file_name=None, mask_name=None, predict=None, model=None, sample_images2=None, model_alt=None):
        """
        Function to plot a randomly selected training set (or validation set if given validation filepaths)

        Parameters:
            sample_images: image in np array
            sample_masks: mask in np array
            encode: Boolean to set encoding type 'uint8' or not
            color_scale: set to 'gray' to set grayscale
            file_name: filename to display in image plot tile
            mask_name: filename to display in mask plot tile
            predict: Boolean, set to True if want to show prediction plots
            model: instance of model object to use .predict() on

        Return:
            None
        """
        image_number = random.randint(0, sample_images.shape[0]-1)

        plt.figure(figsize=(12, 6))
        
        # Original Image
        if predict is not None and model is not None and model_alt is not None:
            plt.subplot(141)
        elif predict is not None and model is not None and model_alt is None:
            plt.subplot(131)
        else:
            plt.subplot(121)

        if encode == 'uint8':
            plt.imshow(sample_images.astype(('uint8')))
        else:
            plt.imshow(sample_images)
        plt.title('Original:\n{}'.format(file_name), fontdict = {'fontsize' : 8})
        plt.axis('off')
        
        # Mask
        if predict is not None and model is not None and model_alt is not None:
            plt.subplot(142)
        elif predict is not None and model is not None and model_alt is None:
            plt.subplot(132)
        else:
            plt.subplot(122)

        if encode == 'uint8':
            if color_scale == 'gray':
                plt.imshow(sample_masks.astype(('uint8')), cmap='gray')
            else:
                plt.imshow(sample_masks.astype(('uint8')))
        else:
            if color_scale == 'gray':
                plt.imshow(sample_masks, cmap='gray')
            else:
                plt.imshow(sample_masks)
        plt.title('Ground Truth Mask:\n{}'.format(mask_name), fontdict = {'fontsize' : 8})
        plt.axis('off')

        if predict is not None and model is not None and model_alt is not None:
            plt.subplot(143)
        if predict is not None and model is not None and model_alt is None:
            plt.subplot(133)
            # Prediction

        if predict is not None:
            # Turn (612, 612, 3) to (1, 612, 612, 3)
            if len(sample_images.shape) == 3:
                sample_images = np.expand_dims(sample_images, axis=0)

            # Predict image
            predicted_image = model.predict(sample_images)
            predicted_image = predicted_image[0,::,::,::]
            # Reverse one hot encode predicted mask
            predicted_image_decoded = ImageProcessor.reverse_one_hot_encode(predicted_image)

            
            if encode == 'uint8':
                if color_scale == 'gray':
                    plt.imshow(predicted_image_decoded.astype(('uint8')), cmap='gray')
                else:
                    plt.imshow(predicted_image_decoded.astype(('uint8')))
            else:
                if color_scale == 'gray':
                    plt.imshow(predicted_image_decoded, cmap='gray')
                else:
                    plt.imshow(predicted_image_decoded)
            plt.title('Predicted Mask {}:'.format(model.name), fontdict = {'fontsize' : 8})
            plt.axis('off')

        if predict is not None and model is not None and model_alt is not None:
            # Prediction #2

            # Turn (612, 612, 3) to (1, 612, 612, 3)
            if len(sample_images2.shape) == 3:
                sample_images2 = np.expand_dims(sample_images2, axis=0)

            # Predict image
            predicted_image = model_alt.predict(sample_images2)
            predicted_image = predicted_image[0,::,::,::]
            # Reverse one hot encode predicted mask
            predicted_image_decoded = ImageProcessor.reverse_one_hot_encode(predicted_image)

            plt.subplot(144)
            if encode == 'uint8':
                if color_scale == 'gray':
                    plt.imshow(predicted_image_decoded.astype(('uint8')), cmap='gray')
                else:
                    plt.imshow(predicted_image_decoded.astype(('uint8')))
            else:
                if color_scale == 'gray':
                    plt.imshow(predicted_image_decoded, cmap='gray')
                else:
                    plt.imshow(predicted_image_decoded)
            plt.title('Predicted Mask {}:'.format(model_alt.name), fontdict = {'fontsize' : 8})
            plt.axis('off')

        plt.show()

    def peek_masks_breakdown(self, sample_images, sample_masks=None, encode=None, color_scale=None, file_name=None, mask_name=None, predict=None, model=None):
        """
        Function to plot a randomly selected prediction mask and breakdown channels
        
        Parameters:
            sample_images: image in np array
            sample_masks: mask in np array
            encode: Boolean to set encoding type 'uint8' or not
            color_scale: set to 'gray' to set grayscale
            file_name: filename to display in image plot tile
            mask_name: filename to display in mask plot tile
            predict: Boolean, set to True if want to show prediction plots
            model: instance of model object to use .predict() on

        Return:
            None
        """
        image_number = random.randint(0, sample_images.shape[0]-1)

        plt.figure(figsize=(12, 6))

        # Turn (612, 612, 3) to (1, 612, 612, 3)
        if len(sample_images.shape) == 3:
            sample_images = np.expand_dims(sample_images, axis=0)

        # Predict image
        predicted_image = model.predict(sample_images)
        predicted_image = predicted_image[0,::,::,::]
        predicted_image = ImageProcessor.rescale(predicted_image)

        # Reverse one hot encode predicted mask
        predicted_image_decoded = ImageProcessor.reverse_one_hot_encode(predicted_image)
        predicted_image_decoded = ImageProcessor.rescale(predicted_image_decoded)

        # Predicted
        plt.subplot(4,2,1)

        if encode == 'uint8':
            if color_scale == 'gray':
                plt.imshow(predicted_image_decoded.astype(('uint8')), cmap='gray')
            else:
                plt.imshow(predicted_image_decoded.astype(('uint8')))
        else:
            if color_scale == 'gray':
                plt.imshow(predicted_image_decoded, cmap='gray')
            else:
                plt.imshow(predicted_image_decoded)
        plt.title('Predicted Mask {}:'.format(model.name), fontdict = {'fontsize' : 8})
        plt.axis('off')

        labels = ['Sky, Red:', 
                    'Big Rocks, Blue:',
                    'Small Rocks, Green:',
                    'Unlabeled, Grey:',
                    ]

        all_colored_channel_activations = 0

        for i in range(predicted_image.shape[-1]-1):
            # Channels
            plt.subplot(4,2,i+2)
            plt.imshow(predicted_image[::,::,i])

            pixels_activated = np.count_nonzero(predicted_image[::,::,i] >= 1)
            percent_pixels_activated = round(pixels_activated / np.size(predicted_image[::,::,i]) * 100, 5)

            all_colored_channel_activations+=percent_pixels_activated

            plt.title(labels[i] + '{}% Pixels Activated'.format(percent_pixels_activated), fontdict = {'fontsize' : 8})
            plt.axis('off')
        
        # Unknown Channel
        plt.subplot(4,2,8)
        plt.imshow(predicted_image[::,::,6])

        plt.title(labels[-1] + '{}% Pixels Activated'.format(round(100 - all_colored_channel_activations, 5)), fontdict = {'fontsize' : 8})
        plt.axis('off')
            
        plt.show()

    #Sanity check, view few mages
    def peek_images_test(self, sample_images, sample_masks=None, encode=None, color_scale=None, file_name=None, mask_name=None, predict=None, model=None):
        """
        Function to plot a randomly selected testing set

        Parameters:
            sample_images: image in np array
            sample_masks: mask in np array
            encode: Boolean to set encoding type 'uint8' or not
            color_scale: set to 'gray' to set grayscale
            file_name: filename to display in image plot tile
            mask_name: filename to display in mask plot tile
            predict: Boolean, set to True if want to show prediction plots
            model: instance of model object to use .predict() on

        Return:
            None
        """
        image_number = random.randint(0, sample_images.shape[0]-1)

        plt.figure(figsize=(12, 6))
        
        # Original Image
        plt.subplot(121)

        if encode == 'uint8':
            plt.imshow(sample_images.astype(('uint8')))
        else:
            plt.imshow(sample_images)
        plt.title('Original:\n{}'.format(file_name), fontdict = {'fontsize' : 8})
        plt.axis('off')
        
        # Prediction
        plt.subplot(122)

        # Turn (X, Y, 3) to (1, X, Y, 3)
        if len(sample_images.shape) == 3:
            sample_images = np.expand_dims(sample_images, axis=0)

        # Predict image
        predicted_image = model.predict(sample_images)
        predicted_image = predicted_image[0,::,::,::]
        # Reverse one hot encode predicted mask
        predicted_image_decoded = ImageProcessor.reverse_one_hot_encode(predicted_image)

        if encode == 'uint8':
            if color_scale == 'gray':
                plt.imshow(predicted_image_decoded.astype(('uint8')), cmap='gray')
            else:
                plt.imshow(predicted_image_decoded.astype(('uint8')))
        else:
            if color_scale == 'gray':
                plt.imshow(predicted_image_decoded, cmap='gray')
            else:
                plt.imshow(predicted_image_decoded)
        plt.title('Predicted Mask {}:'.format(model.name), fontdict = {'fontsize' : 8})
        plt.axis('off')

        plt.show()

    def sanity_check(self, sample_images, sample_masks=None, encode=None, color_scale=None, predict=None, model=None, model_alt=None, predicted_breakdown=None, imsize=None, imsize_alt=None):
        """
        Function to get a training set (or validation set if given validation filepaths) and calls plotting functions
        
        Parameters:
            sample_images: image in np array
            sample_masks: mask in np array
            encode: Boolean to set encoding type 'uint8' or not
            color_scale: set to 'gray' to set grayscale
            file_name: filename to display in image plot tile
            mask_name: filename to display in mask plot tile
            predict: Boolean, set to True if want to show prediction plots
            model: instance of model object to use .predict() on

        Return:
            None
        """
        image_number = random.randint(0, len(os.listdir(sample_images))-1)

        file_name = sorted(os.listdir(sample_images))[image_number]
        image_file = sorted(os.listdir(sample_images))[image_number]
        image = np.array(plt.imread(sample_images + image_file))
        
        if sample_masks is not None:
            mask_name = sorted(os.listdir(sample_masks))[image_number]
            mask_file = sorted(os.listdir(sample_masks))[image_number]
            mask = np.array(plt.imread(sample_masks + mask_file))

        if imsize is not None and sample_masks is not None:
            image =  cv2.resize(image, (imsize, imsize))
            mask =  cv2.resize(mask, (imsize, imsize))
        elif imsize is not None and sample_masks is None:
            image =  cv2.resize(image, (imsize, imsize))

        image1 = copy.deepcopy(image)

        if model_alt:
            image2 = copy.deepcopy(image)
            if imsize_alt is not None and sample_masks is not None:
                image2 =  cv2.resize(image, (imsize_alt, imsize_alt))
                mask =  cv2.resize(mask, (imsize_alt, imsize_alt))
            elif imsize_alt is not None and sample_masks is None:
                image2 =  cv2.resize(image, (imsize_alt, imsize_alt))
        else:
            image2 = None

        # Compare image and mask only
        if predicted_breakdown is None and sample_masks is not None:
            self.peek_images(sample_images=image1, sample_masks=mask, encode=encode, color_scale=color_scale, file_name=file_name, mask_name=mask_name, predict=predict, model=model)
        # Compare original image and mask with predicted mask for model 1 or with model 1 and model 2
        elif predicted_breakdown is not None and sample_masks is not None:
            image1 = ImageProcessor.preprocessor_images(image1)
            mask = ImageProcessor.preprocessor_images(mask)
            if image2 is not None:
                image2 = ImageProcessor.preprocessor_images(image2)
            self.peek_images(sample_images=image1, sample_masks=mask, encode=encode, color_scale=color_scale, file_name=file_name, mask_name=mask_name, predict=predict, model=model, sample_images2=image2, model_alt=model_alt)
            self.peek_masks_breakdown(sample_images=image1, sample_masks=mask, encode=encode, color_scale=color_scale, file_name=file_name, mask_name=mask_name, predict=predict, model=model)
        # Test data, no masks
        elif sample_masks is None:
            image1 = ImageProcessor.preprocessor_images(image1)
            self.peek_images_test(sample_images=image1, encode=encode, color_scale=color_scale, file_name=file_name, predict=predict, model=model)
            # peek_masks_breakdown(sample_images=image, encode=encode, color_scale=color_scale, file_name=file_name, predict=predict, model=model)

