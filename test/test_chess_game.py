#!/usr/bin/env python3
"""
Comprehensive Chess Game Test Script
Tests various scenarios including moves, checks, checkmate, castling, and invalid castling situations.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import pygame
from game import Game
from board import Board
from square import Square
from move import Move
from piece import King, Queen, Rook, Bishop, Knight, Pawn

class ChessGameTester:
    def __init__(self):
        pygame.init()
        self.test_results = []
        
    def log_test(self, test_name, passed, details=""):
        """Log test results"""
        status = "PASS" if passed else "FAIL"
        result = f"[{status}] {test_name}"
        if details:
            result += f" - {details}"
        print(result)
        self.test_results.append((test_name, passed, details))
    
    def test_basic_pawn_moves(self):
        """Test basic pawn movements"""
        print("\n=== Testing Basic Pawn Moves ===")
        
        game = Game()
        
        # Test white pawn double move (white's turn)
        piece = game.board.squares[6][0].piece
        game.board.calc_moves(piece, 6, 0)
        move = Move(Square(6, 0), Square(4, 0))
        is_valid = move in piece.moves
        self.log_test("White Pawn Double Move", is_valid, f"Valid: {is_valid}")
        
        # Test black pawn double move (need to switch to black's turn)
        game.next_player = 'black'
        piece = game.board.squares[1][0].piece
        game.board.calc_moves(piece, 1, 0)
        move = Move(Square(1, 0), Square(3, 0))
        is_valid = move in piece.moves
        self.log_test("Black Pawn Double Move", is_valid, f"Valid: {is_valid}")
        
        # Test invalid pawn move (blocked by piece)
        game = Game()  # Reset for clean test
        game.board.squares[5][1].piece = Pawn('black')  # Block the path
        piece = game.board.squares[6][1].piece
        game.board.calc_moves(piece, 6, 1)
        move = Move(Square(6, 1), Square(4, 1))
        is_valid = move in piece.moves
        self.log_test("Pawn Move Through Blocked Path", not is_valid, f"Should be invalid: {is_valid}")
    
    def test_knight_moves(self):
        """Test knight movements"""
        print("\n=== Testing Knight Moves ===")
        
        game = Game()
        
        # Test valid knight move
        piece = game.board.squares[7][1].piece
        game.board.calc_moves(piece, 7, 1)
        move = Move(Square(7, 1), Square(5, 2))
        is_valid = move in piece.moves
        self.log_test("Valid Knight Move", is_valid, f"Valid: {is_valid}")
        
        # Test invalid knight move (to occupied square)
        piece = game.board.squares[7][1].piece
        game.board.calc_moves(piece, 7, 1)
        move = Move(Square(7, 1), Square(6, 0))
        is_valid = move in piece.moves
        self.log_test("Knight Move to Occupied Square", not is_valid, f"Should be invalid: {is_valid}")
    
    def test_bishop_moves(self):
        """Test bishop movements"""
        print("\n=== Testing Bishop Moves ===")
        
        game = Game()
        
        # Test invalid bishop move (blocked by pawn)
        piece = game.board.squares[7][2].piece
        game.board.calc_moves(piece, 7, 2)
        move = Move(Square(7, 2), Square(5, 0))
        is_valid = move in piece.moves
        self.log_test("Bishop Move Through Piece", not is_valid, f"Should be invalid: {is_valid}")
        
        # Clear path and test valid move
        game.board.squares[6][1].piece = None
        piece = game.board.squares[7][2].piece
        game.board.calc_moves(piece, 7, 2)
        move = Move(Square(7, 2), Square(5, 0))
        is_valid = move in piece.moves
        self.log_test("Valid Bishop Move", is_valid, f"Valid: {is_valid}")
    
    def test_check_detection(self):
        """Test check detection"""
        print("\n=== Testing Check Detection ===")
        
        game = Game()
        
        # Set up a check scenario
        # Clear some pieces to create check
        game.board.squares[6][4].piece = None  # Remove white pawn
        game.board.squares[6][5].piece = None  # Remove white pawn
        game.board.squares[6][6].piece = None  # Remove white pawn
        
        # Move black queen to create check
        game.board.squares[0][3].piece = None  # Remove black queen from original position
        game.board.squares[4][7].piece = Queen('black')  # Place black queen at h4
        
        # Check if white king is in check
        in_check = game.board.in_check('white')
        self.log_test("Check Detection", in_check, f"White king should be in check: {in_check}")
        
        # Check if black king is not in check
        in_check = game.board.in_check('black')
        self.log_test("No Check Detection", not in_check, f"Black king should not be in check: {in_check}")
    
    def test_checkmate_detection(self):
        """Test checkmate detection"""
        print("\n=== Testing Checkmate Detection ===")
        
        game = Game()
        
        # Set up Fool's Mate scenario
        # Clear pieces for Fool's Mate
        game.board.squares[6][5].piece = None  # Remove white pawn
        game.board.squares[6][6].piece = None  # Remove white pawn
        game.board.squares[1][4].piece = None  # Remove black pawn
        
        # Move pieces to create Fool's Mate
        game.board.squares[5][5].piece = Pawn('white')  # White pawn at f3
        game.board.squares[3][4].piece = Pawn('black')  # Black pawn at e5
        game.board.squares[4][6].piece = Pawn('white')  # White pawn at g4
        game.board.squares[4][7].piece = Queen('black')  # Black queen at h4
        
        # Check if white is in checkmate
        is_checkmate = game.board.is_checkmate('white')
        self.log_test("Checkmate Detection", is_checkmate, f"White should be in checkmate: {is_checkmate}")
        
        # Check if black is not in checkmate
        is_checkmate = game.board.is_checkmate('black')
        self.log_test("No Checkmate Detection", not is_checkmate, f"Black should not be in checkmate: {is_checkmate}")
    
    def test_castling(self):
        """Test castling moves"""
        print("\n=== Testing Castling ===")
        
        game = Game()
        
        # Clear path for king-side castling
        game.board.squares[7][1].piece = None  # Remove white knight
        game.board.squares[7][2].piece = None  # Remove white bishop
        game.board.squares[7][5].piece = None  # Remove white bishop
        game.board.squares[7][6].piece = None  # Remove white knight
        
        # Test king-side castling
        piece = game.board.squares[7][4].piece  # White king
        game.board.calc_moves(piece, 7, 4)
        move = Move(Square(7, 4), Square(7, 6))  # King-side castling
        is_valid = move in piece.moves
        self.log_test("King-side Castling", is_valid, f"Valid: {is_valid}")
        
        # Test queen-side castling
        game.board.squares[7][3].piece = None  # Remove white queen
        piece = game.board.squares[7][4].piece  # White king
        game.board.calc_moves(piece, 7, 4)
        move = Move(Square(7, 4), Square(7, 2))  # Queen-side castling
        is_valid = move in piece.moves
        self.log_test("Queen-side Castling", is_valid, f"Valid: {is_valid}")
    
    def test_castling_restrictions(self):
        """Test castling restrictions"""
        print("\n=== Testing Castling Restrictions ===")
        
        game = Game()
        
        # Clear path for castling
        game.board.squares[7][1].piece = None
        game.board.squares[7][2].piece = None
        game.board.squares[7][5].piece = None
        game.board.squares[7][6].piece = None
        
        # Test 1: King has moved
        king = game.board.squares[7][4].piece
        king.moved = True
        piece = game.board.squares[7][4].piece
        game.board.calc_moves(piece, 7, 4)
        move = Move(Square(7, 4), Square(7, 6))
        is_valid = move in piece.moves
        self.log_test("Castling After King Moved", not is_valid, f"Should be invalid: {is_valid}")
        
        # Reset for next test
        game = Game()
        game.board.squares[7][1].piece = None
        game.board.squares[7][2].piece = None
        game.board.squares[7][5].piece = None
        game.board.squares[7][6].piece = None
        
        # Test 2: Rook has moved
        rook = game.board.squares[7][7].piece
        rook.moved = True
        piece = game.board.squares[7][4].piece
        game.board.calc_moves(piece, 7, 4)
        move = Move(Square(7, 4), Square(7, 6))
        is_valid = move in piece.moves
        self.log_test("Castling After Rook Moved", not is_valid, f"Should be invalid: {is_valid}")
        
        # Reset for next test
        game = Game()
        game.board.squares[7][1].piece = None
        game.board.squares[7][2].piece = None
        game.board.squares[7][6].piece = None
        
        # Test 3: Path is blocked
        piece = game.board.squares[7][4].piece
        game.board.calc_moves(piece, 7, 4)
        move = Move(Square(7, 4), Square(7, 6))
        is_valid = move in piece.moves
        self.log_test("Castling With Blocked Path", not is_valid, f"Should be invalid: {is_valid}")
    
    def test_en_passant(self):
        """Test en passant capture"""
        print("\n=== Testing En Passant ===")
        
        game = Game()
        
        # Set up en passant scenario
        game.board.squares[6][0].piece = None  # Remove white pawn
        game.board.squares[4][0].piece = Pawn('white')  # White pawn at a4
        game.board.squares[1][1].piece = None  # Remove black pawn
        game.board.squares[4][1].piece = Pawn('black')  # Black pawn at b4
        
        # Set en passant target (the square the pawn jumped over)
        game.board.en_passant_target = Square(3, 1)  # The square the black pawn jumped over
        
        # Test en passant capture
        piece = game.board.squares[4][0].piece  # White pawn
        game.board.calc_moves(piece, 4, 0)
        move = Move(Square(4, 0), Square(3, 1))  # Capture en passant
        is_valid = move in piece.moves
        self.log_test("En Passant Capture", is_valid, f"Valid: {is_valid}")
    

    
    def test_move_validation(self):
        """Test move validation rules"""
        print("\n=== Testing Move Validation ===")
        
        game = Game()
        
        # Test moving through pieces
        piece = game.board.squares[7][0].piece  # White rook
        game.board.calc_moves(piece, 7, 0)
        move = Move(Square(7, 0), Square(5, 0))
        is_valid = move in piece.moves
        self.log_test("Moving Through Pieces", not is_valid, f"Should be invalid: {is_valid}")
        
        # Test moving to occupied square (same color)
        piece = game.board.squares[7][1].piece  # White knight
        game.board.calc_moves(piece, 7, 1)
        move = Move(Square(7, 1), Square(6, 0))
        is_valid = move in piece.moves
        self.log_test("Moving to Occupied Square", not is_valid, f"Should be invalid: {is_valid}")
        

    
    def test_game_over_detection(self):
        """Test game over detection"""
        print("\n=== Testing Game Over Detection ===")
        
        game = Game()
        
        # Set up checkmate position
        game.board.squares[6][5].piece = None
        game.board.squares[6][6].piece = None
        game.board.squares[1][4].piece = None
        game.board.squares[5][5].piece = Pawn('white')
        game.board.squares[3][4].piece = Pawn('black')
        game.board.squares[4][6].piece = Pawn('white')
        game.board.squares[4][7].piece = Queen('black')
        
        # Check game over
        game.check_game_over()
        is_game_over = game.game_over
        winner = game.winner
        show_popup = game.show_popup
        
        self.log_test("Game Over Detection", is_game_over, f"Game should be over: {is_game_over}")
        self.log_test("Winner Detection", winner == 'black', f"Winner should be black: {winner}")
        self.log_test("Popup Display", show_popup, f"Popup should be shown: {show_popup}")
    
    def run_all_tests(self):
        """Run all test scenarios"""
        print("Starting Comprehensive Chess Game Tests")
        print("=" * 50)
        
        self.test_basic_pawn_moves()
        self.test_knight_moves()
        self.test_bishop_moves()
        self.test_check_detection()
        self.test_checkmate_detection()
        self.test_castling()
        self.test_castling_restrictions()
        self.test_en_passant()
        self.test_move_validation()
        self.test_game_over_detection()
        
        # Summary
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for _, passed, _ in self.test_results if passed)
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\nFailed Tests:")
            for test_name, passed, details in self.test_results:
                if not passed:
                    print(f"  - {test_name}: {details}")
        
        return failed_tests == 0

def main():
    """Main test runner"""
    tester = ChessGameTester()
    success = tester.run_all_tests()
    
    if success:
        print("\nAll tests passed! Chess game is working correctly.")
        return 0
    else:
        print("\nSome tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    exit(main())
