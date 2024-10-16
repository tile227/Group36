A2a: 
I am confident in coding in Python:  
0 – Strongly disagree (Katharina Gertrud Voll) 
0 – Strongly disagree (Tilemachos Tsontakis) 

Our focus area: Materials and LCA > Analysts 


A2b: Identify Claim
-Building we choose to focus on for our focus area:  
Building #2406 

-the claim we choose is 'The wall to window ratio of the façade is 37 %.'
Source: CES_BLD_24_06_Client: Client Report; p. 19 

-Short description:  
The claim 'The wall to window ratio of the façade is 37%' refers to the proportion of the total surface area of a building's façade that is composed of windows compared to the solid wall: A wall to window ratio of 37% means that 37% of the surface area of the façade is occupied by windows, while the remaining 63% is occupied by walls. 

The wall to window ratio is an important architectural and energy efficiency metric.  

This ratio is often used to assess factors such as natural lighting, ventilation, thermal insulation and the overall aesthetics of the building. 

In terms of design, a higher window ratio often results in more natural light but can increase heat loss or gain, while a higher wall ratio can provide better insulation. 

-Justification:
The claim that the wall-to-window ratio is 37% is worth validating because it plays a pivotal role in multiple performance aspects, including: 

Energy Efficiency: Affects U-values, heat transfer, and compliance with BR18. 
Daylight Availability and Visual Comfort: Contributes to achieving SOC3.2.3 and SOC3.2.5 DGNB points. 

Thermal Comfort and Overheating Risk: Ensures compliance with DS/EN 16798. 

DGNB Certification: Impacts multiple criteria, such as TEC4.4 and TEC5.7. 

Environmental and Economic Impact: Influences LCA and LCC calculations, contributing to the building's overall environmental profile. 

By validating this claim, you ensure that the building’s façade design meets both regulatory requirements and sustainability targets while supporting a comfortable and visually pleasing indoor environment. If discrepancies are found, it could indicate that the current design or construction deviates from the intent, leading to performance issues and certification challenges. 



A2c:
- We will make a script that calculates the total wall area and the total window area of the building’s façade. Calculate the wall to window ratio and compare it to the stated 37 %.  

-It has to be checked during the design part of the façade.  

-Total Exterior Wall Area: Sum of all surface areas of the exterior façade walls (Geometrical Properties).
Window Surface Area: Total Window area that are part of the exterior façade (Geometrical Properties).

-During Design phase

-Analyze: Extracting and calculating specific geometric data from the model (the exterior wall and window areas) to derive a meaningful ratio. This process involves analyzing the building’s design to understand the balance between wall and window surface. 

-The use case example that is closest to ours is 20: Building System Analysis. Our use case could be an early stage on the Building System analysis use case. The calculation of the wall/window ratio of the facade helps us to gather information about the natural lighting, thermal comfort and energy gains/losses of the building.


A2e:
-Tool name: Facade Area Analyzer (FAA)
This tool is designed to streamline the process of calculating the wall/window ratio for our building facade (and possibly generic building facades) in Blender within a Python environment. The tool will automate the extraction and analysis of geometric data from an IFC model, allowing architects and engineers to assess compliance with design guidelines and sustainability standards.
FAA will identify the facade elements (walls and windows) of a building and will calculate the total area of these elements. It will also generate the percentage of the wall to window ratio.

-From a business standpoint FAA will enhance design efficiency by automating the calculation of wall/window ratio and will reduce the time and effort needed to analyze designs. It will also help with minimizing energy consumption for heating and cooling leading to significant cost savings for building owners and tenants in the long run. Additionally companies that utilize innovative tools like this can differentiate themselves in the market, attracting clients looking for cutting-edge solutions in sustainable building design.
From a societal point of view our tool will contribute to the creation of energy-efficient buildings, which are essential for reducing overall energy consumption and greenhouse gas emissions. It can also help with enhancing natural lighting in buildings, leading to better indoor environmental quality, which has been shown to improve occupant health, productivity, and well-being.


A2f:
The information we need is:
-Facade Windows, which we can find in the ARC.ifc file with the name: Ifcate/systempanel:glazed xxxxx
-Outer walls of the facade witch consists of 2 elements: Ifcrtainwall/basicwall:ABC - eXT. Wall - xxxxx and ifcmember/rectangular mullion: ARC - Terracota sunscreen - xxxxx
-Doors with glass panels which consist of 2 elements: ifcDoor/Doors_GEALAN_front door:Doors_GEALAN_frontxxxx and ifcDoor/Doors_GEALAN_Double-vent-Door with fanlight-xxxx


A2G:
-We only used Blender, the panda plugin and python for this so we don't need a software license.

