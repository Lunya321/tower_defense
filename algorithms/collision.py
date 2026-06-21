def aabb_collision(rect1, rect2):
    return (rect1[0] < rect2[0] + rect2[2] and
            rect1[0] + rect1[2] > rect2[0] and
            rect1[1] < rect2[1] + rect2[3] and
            rect1[1] + rect1[3] > rect2[1])

def check_projectile_enemy_collision(projectile, enemy, hit_radius=15):
    proj_rect = (
        projectile.pos.x - hit_radius,
        projectile.pos.y - hit_radius,
        hit_radius * 2,
        hit_radius * 2
    )
    enemy_rect = (
        enemy.pos.x - hit_radius,
        enemy.pos.y - hit_radius,
        hit_radius * 2,
        hit_radius * 2
    )
    return aabb_collision(proj_rect, enemy_rect)

def check_circle_collision(pos1, pos2, radius1, radius2):
    distance = pos1.distance_to(pos2)
    return distance <= (radius1 + radius2)