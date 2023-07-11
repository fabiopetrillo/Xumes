Feature: Testing the jump

  Scenario: Top and bottom
    Given A game with a player
    And A pipe generator
    When The first pipe is at 50 % and the next pipe is at 100 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes

  Scenario: Bottom and top
    Given A game with a player
    And A pipe generator
    When The first pipe is at 100 % and the next pipe is at 50 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes