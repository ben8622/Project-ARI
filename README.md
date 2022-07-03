# Project A.R.I (Autonomous Recording of Inventory)
An open sourced web application built on Flask that uses computer vision to take inventory of a fictional business. This project was built at HackDFW 21 and their sponsor McKesson's challenge of "using technology to tackle supply-chain issues". Winning first place! [Here's a demonstration.](https://www.youtube.com/watch?v=fIP6DAwMeYs)

## Idea
Both Oscar (the other creator) and I have worked grueling manual labor jobs where inventory checking was main task. This takes hours, prone to human error, and is mind-numbingly boring. A.R.I. is here to accomplish this task that no one really wants to do.

## Flow
1. Grab video feed input frame by frame
2. Inspect the frame for any Aruco Tags
    - There are two types of Aruco tags inventory and bay markers. Inventory is the actual products we are counting and bay markers are localize the position of a bay in the warehouse
3. Check to see if the Aruco Tag's ID matches that of an inventory item
4. When an inventory item is found, we use [this function](https://github.com/ben8622/Project-ARI/blob/main/aruco_detection/aruco_detect.py#L47) to calculate it's distance from the camera
    - Since _most_ bays in a warehouse are a standard size as is boxes, we can calculate the amount of boxes _behind_ the first one
5. Paint the border of the Aruco Tag onto the webstream and its distance from the camera
6. Display a livestream of the inventory on screen (future plans would be to store in a database periodically)
