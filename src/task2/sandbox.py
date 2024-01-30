import matplotlib.pyplot as plt
import cv2

baboon_path = "/home/ubuntu/thirdeye/src/task2/baboon.jpg"
cat_grey = "/home/ubuntu/thirdeye/src/task2/cat_grey.jfif"

def Plot_Figure(images_with_titles, rows, cols):

    num_images = len(images_with_titles)

    # Create a new figure
    fig = plt.figure(figsize=(4 * cols, 4 * rows))

    for i in range(1, num_images+1):
        fig.add_subplot(rows, cols, i)
        plt.imshow(images_with_titles[i-1][0])
        plt.axis('off')  # Turn off axis labels
        plt.title(images_with_titles[i-1][1])

    plt.show()


def Plot_Histograms(image_array, rows, cols):
    num_images = len(image_array)

    # Create a new figure
    fig = plt.figure(figsize=(4 * cols, 4 * rows))

    for i in range(1, num_images + 1):
        img = image_array[i - 1][0]
        title = image_array[i - 1][1]

        # Convert image to grayscale
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Calculate histogram
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])

        # Plot histogram
        fig.add_subplot(rows, cols, i)
        plt.plot(hist)
        plt.title(f'Histogram - {title}')

    plt.show()

def main():
    image1 = cv2.imread(baboon_path)
    image2 = cv2.imread(cat_grey)
    image_array = [(image1, "Input"), (image2, "Output")]

    # Plotting images
    Plot_Figure(image_array, rows=2, cols=1)

    # Plotting histograms
    Plot_Histograms(image_array, rows=2, cols=1)

if __name__ == '__main__':
    main()
