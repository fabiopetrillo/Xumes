Feature: Testing the jump

  @basic
  Scenario: Jump over 2 pipes
    Given A game with a player
    When  The first pipe is at 100% and the next pipe is at 100%
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipe

  @basic
  Scenario: Jump over 2 pipes
    Given A game with a player
    And An entity List
    When The first pipe is at 80% and the next pipe is at 120%
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipe

  @basic
  Scenario: Jump over 2 pipes
    Given A game with a player
    And An entity List
    When The first pipe is at 80% and the next pipe is at 100%
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipe

  @critic
  Scenario: Jump over 2 pipes
    Given A game with a player
    And An entity List
    When The first pipe is at 150% and the next pipe is at 100%
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipe

  @critic
  Scenario: Jump over 2 pipes
    Given A game with a player
    And An entity List
    When The first pipe is at 100% and the next pipe is at 150%
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipe