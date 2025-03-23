    if event.key == pygame.K_SPACE:
        for sprite in group:
            sprite.acceleration()
    if event.key == pygame.K_ESCAPE:
        config.DONE = True