# Game
@given("player against {nb_enemies} enemies")
def step_impl(game_context, nb_enemies):
    """
    Setup of the game and binding of the observables
    """
    game_context.game = Game()
    game_context.game.nb_enemies = nb_enemies
    game_context.bind(game_context.player, "player", [State("x"), State("y"), State("dead")])
    game_context.bind(game_context.enemies, "enemies", [State("enemies_list", [State("x"), State("y"), State("dead")])])


@when("player and enemies fight")
def step_impl(game_context):
    """
    Game loop execution
    """
    game_context.game.enemies.move()
    game_context.game.player.move()
    game_context.game.enemies.attack()
    game_context.game.player.attack()
    if game_context.game.enemies.die():
        game_context.nb_enemies_killed += 1
    if game_context.game.player.die():
        game_context.player_dead = True


@then("player has kill {nb_enemies} enemies")
def step_impl(game_context, nb_enemies):
    """
    When game is over.
    """
    assert game_context.nb_enemies_killed == nb_enemies
    assert not game_context.player_dead


@reset
def reset(game_context):
    """
    Reset the game for the next test
    """
    game_context.game.player.reset_trainer()
    game_context.game.enemies.reset_trainer()


# Training

@terminated
def terminated(training_context):
    """
    Like convert_terminated, but with the training context
    """
    enemies_dead = True
    for enemy in training_context.enemies:
        if not enemy.dead:
            enemies_dead = False
    return training_context.player.dead or enemies_dead


@action
def action(training_context):
    """
    Like convert_action, but with the training context
    """
    if training_context.raw_actions == 0:
        return ["left"]
    elif training_context.raw_actions == 1:
        return ["right"]
    else:
        return ["attack"]


@observation
def observation(training_context):
    """
    Like convert_observation, but with the training context
    """
    return {"player": np.array([training_context.player.x, training_context.player.dead]),
            "enemies": np.array([[enemy.x, enemy.y] for enemy in training_context.enemies])}

@reward
def reward(training_context):
    """
    Like convert_reward, but with the training context
    """
    if not training_context.nb_enemies_killed_prev:
        training_context.nb_enemies_killed_prev = 0
    for enemy in training_context.enemies:
        if enemy.dead:
            training_context.nb_enemies_killed += 1
    d_enemies_killed = training_context.nb_enemies_killed - training_context.nb_enemies_killed_prev
    training_context.nb_enemies_killed_prev = training_context.nb_enemies_killed

    if d_enemies_killed > 0:
        return 1
    if training_context.player.dead:
        return -1
    else:
        return 0
