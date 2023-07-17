Feature: Testing the jump

  @basic
  Scenario: Jump over 2 pipes
    Given A game with a player
    And An entity list
    When Mario is at position 7 and 11 with normal pipe height
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipe

  @critic
  Scenario: Jump over 2 pipes
    Given A game with a player
    And An entity List
    When Mario is at position 7 and 11 with second pipe at 120% of is height
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipe