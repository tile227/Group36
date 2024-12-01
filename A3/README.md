# **About the Tool**

-The claim we choose is 'The wall to window ratio of the façade is 37 %.' 

-The claim is in: CES_BLD_24_06_Client: Client Report; p. 19

## **Description:**
The Tool (named Facade Area Analyzer (FAA)) is designed to streamline the process of calculating the wall/window ratio for our building facade (and possibly generic building facades) in Blender within a Python environment. The tool creates a bounding box of the building and checks all objects materials for glass in their name. Then with raycasting (checking and stopping at the first object hit) it determines witch materials are part of the facade and calculates the total area of the facade. Then with simple calculations it prints the total surface of glass materials of the facade and finally the window-to-wall ratio of the facade of the building.

## **Instructions:** 

Install Blender-> Load the building model into Blender.
Ensure that: The building is correctly positioned with the ground level at Z = 0.
Run the script


## **Advanced Building Design**

-The tool would be most useful in Stage B (Design phase).

-Subjects: Architectural Design, Energy Engineering, sustainable Design



## **The information needed for the model to work is to:**

*Properly defined materials:* Glass materials must have "glass" in their name for the script to identify them.

*Vertical facade geometry:* All facade elements should be modeled as vertical surfaces.

*Correct positioning:* The building should be placed with ground level at Z = 0 to exclude subgrade elements.

*Polygon data:* Objects should contain polygonal geometry (mesh data) with face normals and areas correctly defined.

This setup ensures accurate calculations of facade areas and Window-to-Wall Ratio.
