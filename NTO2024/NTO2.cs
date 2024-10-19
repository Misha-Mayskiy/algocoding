using System;
using System.Collections.Generic;
using System.Linq;

namespace NTO
{
    public partial class NTO
    {
        Hero hero;
        Field field;

        public static void Main(string[] args)
        {
            List<string> inputLines = new List<string>();
            string line;
            while ((line = Console.ReadLine()) != "Stop")
            {
                inputLines.Add(line);
            }
            string heroLine = inputLines[0].Replace("Hero is ", "").Replace("(", "").Replace(")", "");
            var heroDimensions = heroLine.Split(',').Select(int.Parse).ToArray();
            Hero hero = new Hero(heroDimensions[0], heroDimensions[1]);
            string fieldLine = inputLines[1].Replace("Field is ", "").Replace("(", "").Replace(")", "");
            var fieldDimensions = fieldLine.Split(',').Select(int.Parse).ToArray();
            Field field = new Field(fieldDimensions[0], fieldDimensions[1], hero);
            hero.x_position = field.width / 2;
            hero.y_position = field.height / 2;
            int index = 2;
            while (!inputLines[index].StartsWith("Moves:"))
            {
                string obstacleLine = inputLines[index]
                    .Replace("Obstacle is ", "")
                    .Replace("position is ", "")
                    .Replace("(", "")
                    .Replace(")", "");
                var parts = obstacleLine.Split(',');
                int obstacleWidth = int.Parse(parts[0]);
                int obstacleHeight = int.Parse(parts[1]);
                int obstacleX = int.Parse(parts[2]);
                int obstacleY = int.Parse(parts[3]);
                field.obstacles.Add(new Obstacle(obstacleWidth, obstacleHeight, obstacleX, obstacleY));
                index++;
            }
            hero.OnUpdate();
            for (int i = index + 1; i < inputLines.Count; i++)
            {
                string moveLine = inputLines[i].Replace("(", "").Replace(")", "");
                var moveParts = moveLine.Split(',').Select(int.Parse).ToArray();
                DirectionVector moveVector = (moveParts[0], moveParts[1]);
                field.MoveHero(moveVector);
                hero.OnUpdate();
            }
        }
    }

    public class Field
    {
        public int width;
        public int height;
        public Hero hero;
        public List<Obstacle> obstacles = new List<Obstacle> { };

        public Field(int _width, int _height, Hero _hero)
        {
            width = _width;
            height = _height;
            hero = _hero;
        }

        public void MoveHero(DirectionVector vector)
        {
            // Calculate new potential positions
            int newX = hero.x_position + vector.x_dir;
            int newY = hero.y_position + vector.y_dir;

            bool teleportedX = false, teleportedY = false;

            // Check for teleportation on X axis
            if (newX >= width)
            {
                newX = 0;
                teleportedX = true;
            }
            else if (newX < 0)
            {
                newX = width - 1;
                teleportedX = true;
            }

            // Check for teleportation on Y axis
            if (newY >= height)
            {
                newY = 0;
                teleportedY = true;
            }
            else if (newY < 0)
            {
                newY = height - 1;
                teleportedY = true;
            }

            // Notify about teleportation
            if (teleportedX || teleportedY)
                Console.WriteLine("Teleported");

            // Check for collisions
            bool collisionX = false, collisionY = false;

            foreach (var obstacle in obstacles)
            {
                // Check collision with the new X position
                if (IsColliding(newX, hero.y_position, obstacle))
                    collisionX = true;

                // Check collision with the new Y position
                if (IsColliding(hero.x_position, newY, obstacle))
                    collisionY = true;

                // If both axes collide with the same obstacle
                if (collisionX && collisionY)
                    break;
            }

            // Handle collisions and update position accordingly
            if (collisionX && collisionY)
                Console.WriteLine("We got collision by X and Y");
            
            else if (collisionX)
                Console.WriteLine("We got collision by X");
            
            else if (collisionY)
                Console.WriteLine("We got collision by Y");
            
            else
            {
                // Move the hero only if there are no collisions
                hero.x_position = newX;
                hero.y_position = newY;
                
                // Ensure the movement is reflected correctly after checking collisions
                if (!collisionX && !collisionY)
                    Console.WriteLine($"Moved to ({hero.x_position}, {hero.y_position})");
                
             }
        }

        private bool IsColliding(int x, int y, Obstacle obstacle)
        {
           return x >= obstacle.x_position - obstacle.width / 2 &&
                  x <= obstacle.x_position + obstacle.width / 2 &&
                  y >= obstacle.y_position - obstacle.height / 2 &&
                  y <= obstacle.y_position + obstacle.height / 2;
        }
    }

    public class Obstacle
    {
        public int width;
        public int height;
        public int x_position;
        public int y_position;

        public Obstacle(int _width, int _height, int _x, int _y)
        {
           width = _width;
           height = _height;
           x_position = _x;
           y_position = _y;
       }
   }

   public class Hero
   {
       public int width;
       public int height;
       public int x_position;
       public int y_position;

       public Hero(int _width, int _height)
       {
           width = _width;
           height = _height;
       }

       public void OnUpdate()
       {
           Console.WriteLine($"{x_position}, {y_position}");
       }
   }

   public class DirectionVector
   {
       public enum HorizontalDirection { left=-1, stay=0, right=1 }
       public enum VerticalDirection { down=-1, stay=0, up=1 }

       public HorizontalDirection x_dir { get; set; }
       public VerticalDirection y_dir { get; set; }

       public DirectionVector() 
       { 
           x_dir= HorizontalDirection.stay; 
           y_dir= VerticalDirection.stay; 
       }
       
       public DirectionVector((int,int) directions) 
       { 
           x_dir= (HorizontalDirection)directions.Item1; 
           y_dir= (VerticalDirection)directions.Item2; 
       }

       public static implicit operator DirectionVector((int,int) directions) => new DirectionVector(directions);
       
       public static implicit operator (int,int)(DirectionVector vector) => ((int)vector.x_dir,(int)vector.y_dir);
       
       public override string ToString() => $"({(int)x_dir}, {(int)y_dir})";
   }
}