# python_first_pygame
My first Python Pygame - a game that challenges players to navigate a colorful landscape filled with obstacles. The gameplay involves controlling a character (player) within a defined play area, avoiding static and bouncing obstacles, and collecting food items for points.

Key Features:
Dynamic Play Area: The player navigates through a play area filled with randomly generated obstacles and bouncing obstacles that move in random directions.

Scoring System: Players earn points by collecting food items and lose points upon collision with obstacles. The score is affected by the game's difficulty level.

Difficulty Levels: The game's difficulty increases with each level, introducing more obstacles and enhancing the bouncing obstacles' size.

Shield Mechanism: Players can earn shields, providing a buffer against collisions. The number of shields decreases with each collision, and the game visualizes the shield status.

Control Options: Players can choose between keyboard and mouse controls for the movement of their character.

Game Over Condition: The game ends if the score falls to zero, and the game displays the final score and level achieved.

Stylish UI: With a beautiful menu bar and color-coded objects, the game provides an attractive and intuitive interface.

--------------------------------------------------------------------------------------------------------------
# Description of Technologies and Principles Applied (For Potential Employers)
"First Pygame" showcases a strong grasp of Python programming and the following specific skills and principles:

Pygame Framework: The game leverages the Pygame library for rendering graphics, handling user input, and managing game timing.

Object-Oriented Programming (OOP): The game utilizes classes and objects, such as the BounceObstacle class, to encapsulate the behavior and attributes of game entities.

Collision Detection: Implemented using Pygame's collision methods, the game can detect collisions between the player, obstacles, and food items, affecting the game state accordingly.

Randomized Elements: The use of Python's random module to generate random obstacle positions, angles, and bouncing directions adds unpredictability to the gameplay.

Game State Management: The code exhibits well-structured game state management, utilizing variables and functions to control aspects like levels, scores, difficulty, and shields.

Timed Events: With Pygame's timing functions, the game can trigger specific events and responses at controlled intervals, such as flash messages for shields.

Modular Design: The code is organized into specific functions, each handling distinct aspects of the game like drawing elements, handling collisions, player control, and game logic. This modular approach promotes readability and maintainability.

User Interaction Handling: The game supports different control mechanisms (keyboard and mouse) and listens for specific key events to toggle options, demonstrating a thorough understanding of event handling.

Responsive Design: The player's character and obstacles are kept within the play area, and the game responds to collisions with visually distinct feedback, creating an engaging and responsive gaming experience.

Overall, "First Pygame" illustrates a robust understanding of Python programming, game development principles, and the ability to build an interactive and visually appealing application. It demonstrates a strong foundation in coding, problem-solving, and software design.

-------------------------------------------------------------------------------
# How to run
Make sure to install pygame in your venv

The application can be launched from the main.py file

------------------------------------------------------------------------------
# My Thoughts
This was an interesting project. I have always had an interest in games and have dabbled in game development over the years with looks like RPG Maker and Unity, but at those times I lacked a foundational knowledge of programming. This gave me a chance to reapproach game develoment, but with a solid understanding of what all of the code does, and why it does it.

Admittedly, I could greatly improve this project with further investment of time. 

Things that I know it needs for sure:
1. A massive refactoring. All of the code was written as it was being developed and as I watched tutorials on how to implement basic processes within the Pygame framework. Some of the legacy code was left in place because it worked, and I wanted to focus more on adding to the game, improving the experience for users, and also implementing other game design elements. This accounts for the use of both Object Oriented and non OOP for instantiating objects.
2. There are a few quirky bugs that I spotted and have a general idea of how to fix, but are not massive hindrances in the game experience.
3. UI Improvements - I dont love the UI, but it was great to learn some of what goes into designing a UI programmatically without any artwork for elements or screens.

With all of that being said, the primary purpose of this project was for me to experiment with the Pygame framework, and midway through I decided I might as well finish the project to showcase what I was learning.

As you view the application, please keep in mind that I spent a total of roughly 10 hours on the project, including watching tutorials and troubleshooting the application.
