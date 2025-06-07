using System;
using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Input;
using System.Windows.Threading;
using System.Windows.Controls;
using System.Windows.Media.Imaging;
using System.Windows.Media;

namespace WpfSnake
{
    public partial class MainWindow : Window
    {
        private readonly int cellSize = 32;
        private readonly int gridWidth = 17;   // 畫布寬度 544px / 32
        private readonly int gridHeight = 15;  // 畫布高度 480px / 32

        private List<Point> snake = new List<Point>();
        private List<Point> obstacles = new List<Point>();
        private Point food;
        private Point bomb = new Point(-1, -1);
        private bool bombActive = false;
        private DispatcherTimer gameTimer = new DispatcherTimer();
        private DispatcherTimer obstacleTimer = new DispatcherTimer();
        private DispatcherTimer countdownTimer = new DispatcherTimer();
        private string direction = "Right";
        private bool gameOver = false;
        private bool isPaused = false;
        private int score = 0;
        private int timeleft = 120;
        private Random rand = new Random();
        private readonly int obstacleCount = 5;
        private readonly int maxObstacles = 10;

        public MainWindow()
        {
            InitializeComponent();

            this.Loaded += (s, e) =>
            {
                InitGame();

                gameTimer.Interval = TimeSpan.FromMilliseconds(800); // 速度較慢
                gameTimer.Tick += GameLoop;
                gameTimer.Start();

                obstacleTimer.Interval = TimeSpan.FromSeconds(10);
                obstacleTimer.Tick += AddObstacle;
                obstacleTimer.Start();

                countdownTimer.Interval = TimeSpan.FromSeconds(1);
                countdownTimer.Tick += CountdownTick;
                countdownTimer.Start();

                this.KeyDown += OnKeyDown;
            };
        }

        private void CountdownTick(object sender, EventArgs e)
        {
            if (isPaused || gameOver) return;

            timeleft--;
            CountdownText.Text = $"Time: {timeleft}s";

            if (timeleft <= 0)
            {
                countdownTimer.Stop();
                gameTimer.Stop();
                obstacleTimer.Stop();
                gameOver = true;
                MessageBox.Show("時間到！分數：" + score);
            }
        }

        protected override void OnClosed(EventArgs e)
        {
            base.OnClosed(e);
            Environment.Exit(0);
        }

        private void InitGame()
        {
            snake.Clear();
            obstacles.Clear();
            snake.Add(new Point(7, 5));
            direction = "Right";
            gameOver = false;
            isPaused = false;
            score = 0;
            bombActive = false;
            timeleft = 120;
            CountdownText.Text = $"Time: {timeleft}s";

            GenerateMazeWalls();
            GenerateFood();
            GenerateObstacles();
            UpdateScore();
        }

        private void GameLoop(object sender, EventArgs e)
        {
            if (gameOver)
            {
                gameTimer.Stop();
                obstacleTimer.Stop();
                countdownTimer.Stop();
                MessageBox.Show("Game Over! 分數：" + score);
                return;
            }

            if (isPaused) return;

            MoveSnake();
            Draw();
            UpdateScore();
        }

        private void MoveSnake()
        {
            Point head = snake[0];
            Point newHead = head;

            switch (direction)
            {
                case "Up": newHead.Y -= 1; break;
                case "Down": newHead.Y += 1; break;
                case "Left": newHead.X -= 1; break;
                case "Right": newHead.X += 1; break;
            }

            if (newHead.X < 0 || newHead.Y < 0 ||
                newHead.X >= gridWidth || newHead.Y >= gridHeight ||
                snake.Contains(newHead) ||
                obstacles.Contains(newHead))
            {
                gameOver = true;
                return;
            }

            snake.Insert(0, newHead);

            if (newHead == food)
            {
                GenerateFood();
            }
            else
            {
                snake.RemoveAt(snake.Count - 1);
            }

            if (newHead == bomb && bombActive)
            {
                bombActive = false;
                obstacles.RemoveAll(obs =>
                    Math.Abs(obs.X - newHead.X) <= 1 &&
                    Math.Abs(obs.Y - newHead.Y) <= 1);
            }
        }

        private void Draw()
        {
            GameCanvas.Children.Clear();
            DrawImage("Photo/apple.png", food);

            if (bombActive)
            {
                DrawImage("Photo/bomb.png", bomb);
            }

            foreach (var obs in obstacles)
            {
                DrawImage("Photo/obstacle.png", obs);
            }

            for (int i = 0; i < snake.Count; i++)
            {
                if (i == 0)
                    DrawImage("Photo/snake_head.png", snake[i]);
                else if (i == snake.Count - 1)
                    DrawImage("Photo/snake_tail.png", snake[i]);
                else
                {
                    string bodyImage = (i % 2 == 0) ? "Photo/snake_body_1.png" : "Photo/snake_body_2.png";
                    DrawImage(bodyImage, snake[i]);
                }
            }
        }

        private void DrawImage(string imagePath, Point position)
        {
            Image img = new Image
            {
                Width = cellSize,
                Height = cellSize,
                Source = new BitmapImage(new Uri($"pack://application:,,,/{imagePath}"))
            };

            Canvas.SetLeft(img, position.X * cellSize);
            Canvas.SetTop(img, position.Y * cellSize);
            GameCanvas.Children.Add(img);
        }

        private void GenerateFood()
        {
            Point GreatFood;
            int tries = 0;
            do
            {
                GreatFood = new Point(rand.Next(0, gridWidth), rand.Next(0, gridHeight));
                tries++;
                if (tries > 100) return;
            }
            while (snake.Contains(GreatFood) || obstacles.Contains(GreatFood));

            food = GreatFood;

            if (!bombActive && rand.NextDouble() < 0.3)
            {
                Point b;
                do
                {
                    b = new Point(rand.Next(0, gridWidth), rand.Next(0, gridHeight));
                }
                while (snake.Contains(b) || obstacles.Contains(b) || b == food);

                bomb = b;
                bombActive = true;
            }
        }

        private void GenerateObstacles()
        {
            while (obstacles.Count < obstacleCount)
            {
                Point p = new Point(rand.Next(0, gridWidth), rand.Next(0, gridHeight));
                if (!snake.Contains(p) && !obstacles.Contains(p) && p != food)
                {
                    obstacles.Add(p);
                }
            }
        }

        private void AddObstacle(object sender, EventArgs e)
        {
            if (obstacles.Count >= maxObstacles) return;

            Point p = new Point(rand.Next(0, gridWidth), rand.Next(0, gridHeight));
            if (!snake.Contains(p) && !obstacles.Contains(p) && p != food)
            {
                obstacles.Add(p);
            }
        }

        private void GenerateMazeWalls()
        {
            int centerX = gridWidth / 2;
            int centerY = gridHeight / 2;

            for (int i = -2; i <= 2; i++)
            {
                obstacles.Add(new Point(centerX + i, centerY));
                obstacles.Add(new Point(centerX, centerY + i));
            }

            for (int x = 2; x < 6; x++)
                obstacles.Add(new Point(x, 2));

            for (int y = gridHeight - 5; y < gridHeight - 1; y++)
                obstacles.Add(new Point(gridWidth - 3, y));
        }

        private void UpdateScore()
        {
            score = snake.Count - 1;
            ScoreText.Text = $"Score: {score}";
        }

        private void OnKeyDown(object sender, KeyEventArgs e)
        {
            switch (e.Key)
            {
                case Key.Up: if (direction != "Down") direction = "Up"; break;
                case Key.Down: if (direction != "Up") direction = "Down"; break;
                case Key.Left: if (direction != "Right") direction = "Left"; break;
                case Key.Right: if (direction != "Left") direction = "Right"; break;
                case Key.P: isPaused = !isPaused; break;
            }
        }

        private void RestartButton_Click(object sender, RoutedEventArgs e)
        {
            GameCanvas.Children.Clear();
            InitGame();
            gameTimer.Stop();
            gameTimer.Start();
            countdownTimer.Stop();
            countdownTimer.Start();
        }
    }
}
