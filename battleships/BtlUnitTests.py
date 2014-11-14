import unittest
#from BtlBoard import BtlBoard
#from BtlGame import BtlGame
#from BtlPlayer import BtlPlayer
from BtlMove import BtlMove
from BtlShip import BtlShip

class BtlUnitTests( unittest.TestCase ):

  def test_BtlMove_1( self ):
    with self.assertRaises( TypeError ):
      move = BtlMove( 'K', 11 )

  def test_BtlMove_2( self ):
    with self.assertRaises( TypeError ):
      move = BtlMove( '@', 0 )

  def test_BtlMove_3( self ):
    with self.assertRaises( TypeError ):
      move = BtlMove( 1, 1 )

  def test_BtlMove_getX_1( self ):
    move = BtlMove( 'A', 1 )
    self.assertEquals( 0, move.getX() )

  def test_BtlMove_getX_2( self ):
    move = BtlMove( 'J', 10 )
    self.assertEquals( 9, move.getX() )
  
  def test_BtlMove_getY_1( self ):
    move = BtlMove( 'A', 1 )
    self.assertEquals( 0, move.getY() )

  def test_BtlMove_getY_2( self ):
    move = BtlMove( 'J', 10 )
    self.assertEquals( 9, move.getY() )
 
  def test_BtlMove_str_1( self ):
    move = BtlMove( 'A', 1 )
    self.assertEquals( 'A1', str( move ) )

  def test_BtlMove_str_2( self ):
    move = BtlMove( 'J', 10 )
    self.assertEquals( 'J10', str( move ) )

  def test_BtlMove_getMove_1( self ):
    move = BtlMove( 'A', 1 )
    self.assertEqual( ( 0, 0 ), move.getMove() )

  def test_BtlMove_getMove_2( self ):
    move = BtlMove( 'J', 10 )
    self.assertEqual( ( 9, 9 ), move.getMove() )

  def test_BtlShip_isSunk_1( self ):
    ship = BtlShip( 'test', 3 )
    self.assertFalse( ship.isSunk() )

  def test_BtlShip_isSunk_2( self ):
    ship = BtlShip( 'test', 3 )
    ship.setHit( 0 )
    self.assertFalse( ship.isSunk() )

  def test_BtlShip_isSunk_3( self ):
    ship = BtlShip( 'test', 3 )
    ship.setHit( 0 )
    ship.setHit( 1 )
    self.assertFalse( ship.isSunk() )

  def test_BtlShip_isSunk_4( self ):
    ship = BtlShip( 'test', 3 )
    ship.setHit( 0 )
    ship.setHit( 1 )
    ship.setHit( 2 )
    self.assertTrue( ship.isSunk() )

  def test_BtlShip_isSunk_5( self ):
    ship = BtlShip( 'test', 3 )
    ship.setHit( 0 )
    ship.setHit( 2 )
    ship.setHit( 6 )
    self.assertFalse( ship.isSunk() )
  
  def test_BtlShip_isSunk_6( self ):
    ship = BtlShip( 'test', 3 )
    ship.setHit( 4 )
    ship.setHit( 5 )
    ship.setHit( 6 )
    self.assertFalse( ship.isSunk() )

  def test_BtlShip_isHit_1( self ):
    ship = BtlShip( 'test', 3 )
    ship.setPosition( 0, 0, '>' )
    self.assertTrue( ship.isHit( 0, 0, False ) )

  def test_BtlShip_isHit_2( self ):
    ship = BtlShip( 'test', 3 )
    ship.setPosition( 0, 0, '>' )
    self.assertTrue( ship.isHit( 2, 0, False ) )

  def test_BtlShip_isHit_3( self ):
    ship = BtlShip( 'test', 3 )
    ship.setPosition( 0, 0, '>' )
    self.assertFalse( ship.isHit( 3, 0, False ) )

  def test_BtlShip_isHit_4( self ):
    ship = BtlShip( 'test', 3 )
    ship.setPosition( 0, 0, '>' )
    self.assertFalse( ship.isHit( 0, 1, False ) )

  def test_BtlShip_isHit_5( self ):
    ship = BtlShip( 'test', 3 )
    ship.setPosition( 0, 0, '>' )
    self.assertFalse( ship.isHit( 3, 1, False ) )

  def test_BtlShip_isHit_6( self ):
    ship = BtlShip( 'test', 3 )
    ship.setPosition( 3, 3, 'v' )
    self.assertTrue( ship.isHit( 3, 4, False ) )

  def test_BtlShip_isHit_7( self ):
    ship = BtlShip( 'test', 3 )
    ship.setPosition( 3, 3, 'v' )
    self.assertTrue( ship.isHit( 3, 5, False ) )

  def test_BtlShip_isHit_8( self ):
    ship = BtlShip( 'test', 3 )
    ship.setPosition( 3, 3, 'v' )
    self.assertFalse( ship.isHit( 3, 0, False ) )

  def test_BtlShip_isHit_9( self ):
    ship = BtlShip( 'test', 3 )
    ship.setPosition( 3, 3, 'v' )
    self.assertFalse( ship.isHit( 2, 3, False ) )

  def test_BtlShip_isHit_10( self ):
    ship = BtlShip( 'test', 3 )
    ship.setPosition( 3, 3, 'v' )
    self.assertFalse( ship.isHit( 4, 4, False ) )

if __name__ == '__main__':
  unittest.main()
