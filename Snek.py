from sense_hat import SenseHat
from time import sleep
import random

s = SenseHat()
s.low_light = True

# Colors used
GREEN = (0, 255, 0)
RED = (255, 0, 0)


min_edge = 0
max_edge = 7


def generateFood():
    # Spawn random food
        retryFlag = True
        while retryFlag:
            foodPositionX = random.randint(0, 7)
            foodPositionY = random.randint(0, 7)
            retryFlag = False
            for x, y in zip(snakePositionX, snakePositionY):
                if x == foodPositionX and y == foodPositionY:
                    retryFlag = True
                    break
        return foodPositionX, foodPositionY
    
    
# Main game loop
while True:

    s.clear()
    s.show_message("SNEK")
    
    gameOverFlag = False
    doGrow = False
    generateNewFood = False
    
    # Increase speed by 10% when food is eaten
    snakeSpeed = 0.5 # used as a time delay
    snakeSpeedBoost = 1.1
    totalScore = 0
    bordersCrossed = False
    
    # initializing the starting position of the snek
    snakePositionX = [3]
    snakePositionY = [4]
    
    # Default moving direction 
    directionX = 1
    directionY = 0

    # initial food position
    foodPositionX, foodPositionY = generateFood()

    while not gameOverFlag:
        # if head of the snake at the same location as food, eat it
        if foodPositionX == snakePositionX[0] and foodPositionY == snakePositionY[0]:
            doGrow = True
            generateNewFood = True
            snakeSpeed /= snakeSpeedBoost # increase the speed by 10%
            totalScore = totalScore + 1

        # Snake dies when crossing over itself
        for i in range(1, len(snakePositionX)):
            if snakePositionX[i] == snakePositionX[0] and snakePositionY[i] == snakePositionY[0]:
                gameOverFlag = True

        
        # Check temperature
        current_temp = s.get_temperature()
        tempFlag = current_temp < -10 or current_temp > 60
        
        # Check game borders, snake dies when crossing boundaries
        if snakePositionX[0] > max_edge or snakePositionX[0] < min_edge or snakePositionY[0] > max_edge or snakePositionY[0] < min_edge:
          bordersCrossed = True
        
        # Check if game is over
        if gameOverFlag or tempFlag or bordersCrossed:
            break

        # Listen for commands
        for button in s.stick.get_events():
            if button.direction == "left" and directionX != 1:
                directionX = -1
                directionY = 0
            elif button.direction == "right" and directionX != -1:
                directionX = 1
                directionY = 0
            elif button.direction == "up" and directionY != 1:
                directionY = -1
                directionX = 0
            elif button.direction == "down" and directionY != -1:
                directionY = 1
                directionX = 0

        # Grow snek
        if doGrow:
            doGrow = False
            snakePositionX.append(0)
            snakePositionY.append(0)

        # Move snek
        if not bordersCrossed:
            for i in range((len(snakePositionX) - 1), 0, -1):
                snakePositionX[i] = snakePositionX[i - 1]
                snakePositionY[i] = snakePositionY[i - 1]

            snakePositionX[0] += directionX
            snakePositionY[0] += directionY

        # Generate food
        if generateNewFood:
            generateNewFood = False
            foodPositionX, foodPositionY = generateFood()

        # Update the screen
        if not bordersCrossed:
          s.clear()
          s.set_pixel(foodPositionX, foodPositionY, RED)
          for x, y in zip(snakePositionX, snakePositionY):
              s.set_pixel(x, y, GREEN)
        else:
          gameOverFlag = True

        # Snake speed 
        sleep(snakeSpeed)


    s.clear()

    # Display final score
    if gameOverFlag or bordersCrossed or tempFlag:
        s.show_message("Game over! Score is: {}".format(totalScore), text_colour=RED)