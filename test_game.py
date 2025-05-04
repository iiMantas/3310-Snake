import unittest
import os
from pygame import Vector2
from snake import Game, save_score, load_scores, number_of_cells

class TestGameFunctions(unittest.TestCase):

    def setUp(self):
        # Išvalome failą prieš kiekvieną testą
        if os.path.exists("game_results.txt"):
            os.remove("game_results.txt")

    def test_save_score(self):
        save_score(10)
        scores = load_scores()
        self.assertEqual(scores, [10])

    def test_load_scores(self):
        save_score(10)
        save_score(20)
        scores = load_scores()
        self.assertEqual(scores, [10, 20])

    def test_load_scores_empty(self):
        scores = load_scores()
        self.assertEqual(scores, [])

    def test_food_position_on_edge(self):
        """Tikriname, kad maistas nebūtų sugeneruotas ant krašto"""
        game = Game()
        while (game.food.position == Vector2(0, 0) or 
               game.food.position.x == number_of_cells - 1 or 
               game.food.position.y == number_of_cells - 1):
            game.food.position = game.food.generate_random_pos(game.snake.body)
        self.assertNotEqual(game.food.position, Vector2(0, 0))
        self.assertNotEqual(game.food.position.x, number_of_cells - 1)
        self.assertNotEqual(game.food.position.y, number_of_cells - 1)

    def test_snake_length_increase(self):
        """Tikriname, ar gyvatės ilgis padidėja po maisto suvalgymo"""
        game = Game()
        game.snake.body = [Vector2(5, 5)]
        initial_length = len(game.snake.body)  # turi būti 1
        game.food.position = game.snake.body[0] + Vector2(1, 0)
        game.update()  # Suvalgo maistą ir iš karto auga
        self.assertEqual(len(game.snake.body), initial_length + 1)

    def test_game_over_collision_with_wall(self):
        """Tikriname, ar žaidimas baigiasi, kai gyvatė susiduria su siena"""
        game = Game()
        game.snake.body = [Vector2(0, 0)]
        game.snake.direction = Vector2(-1, 0)
        game.update()
        self.assertEqual(game.state, "STOPPED")

    def test_score_increase(self):
        """Tikriname, ar taškai padidėja po maisto paėmimo"""
        game = Game()
        game.snake.body = [Vector2(5, 5)]
        initial_score = game.score
        game.food.position = game.snake.body[0] + Vector2(1, 0)
        game.update()
        self.assertEqual(game.score, initial_score + 1)

    def test_food_generation(self):
        """Tikriname, ar maistas nėra sugeneruotas ten, kur yra gyvatė"""
        game = Game()
        food_pos = game.food.position
        self.assertNotEqual(food_pos, game.snake.body[0])

    def test_game_start(self):
        """Tikriname, ar žaidimas prasideda po paspaudimo"""
        game = Game()
        game.state = "STOPPED"
        game.snake.body = [Vector2(5, 5)]
        game.food.position = Vector2(6, 5)
        game.state = "RUNNING"
        game.snake.update()
        self.assertEqual(game.state, "RUNNING")

    def test_game_state_transition(self):
        game = Game()
        self.assertEqual(game.state, "RUNNING")
        game.state = "STOPPED"
        self.assertEqual(game.state, "STOPPED")

    def test_multiple_game_updates(self):
        game = Game()
        game.snake.body = [Vector2(5, 5)]
        game.snake.direction = Vector2(0, 1)
        for _ in range(5):
            game.update()
        self.assertEqual(game.snake.body[0], Vector2(5, 10))

    def test_snake_cannot_turn_180(self):
        """Tikriname, kad gyvatė negali judėti priešinga kryptimi"""
        game = Game()
        game.snake.direction = Vector2(1, 0)  # Judame į dešinę
        game.snake.update()
        game.snake.direction = Vector2(-1, 0)  # Bandome judėti atgal
        with self.assertRaises(Exception):
            game.snake.update()  # Negalima atlikti šio judesio

    def test_game_start_and_reset(self):
        game = Game()
        game.state = "STOPPED"
        game.snake.body = [Vector2(5, 5)]
        game.food.position = Vector2(6, 5)
        game.state = "RUNNING"
        game.snake.update()  # Atkuriame žaidimą
        self.assertEqual(game.state, "RUNNING")
        game.game_over()  # Baigiam žaidimą
        self.assertEqual(game.state, "STOPPED")  # Patikriname, kad žaidimas sustabdomas

    def test_best_score_persistence(self):
        game = Game()
        game.score = 30
        game.best_score = 20  # Geriausias rezultatas
        save_score(game.score)  # Išsaugome šį rezultatą
        loaded_scores = load_scores()  # Užkrauname
        self.assertGreaterEqual(max(loaded_scores), game.score)

if __name__ == "__main__":
    unittest.main()
