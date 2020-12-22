players = []
current_player = []

def compute_score(hand):
    total = 0
    for i, card in enumerate(reversed(hand)):
        total += (i+1)*card
    return total

with open('challenge_22') as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        if 'Player' in line:
            if current_player:
                players.append(current_player)
            current_player = []
            continue

        current_player.append(int(line))

players.append(current_player)
print(players)
def basic_game(player_one, player_two):
    players = [player_one[::], player_two[::]]

    round_num = 1
    while players[0] and players[1]:
        a, b = (hand.pop(0) for hand in players)
        if a > b:
            players[0].extend([a,b])
        else:
            players[1].extend([b,a])

    print("Player 1's deck:" + ', '.join((f'{n}' for n in players[0])))
    print("Player 2's deck:" + ', '.join((f'{n}' for n in players[1])))

    winner = players[0] if players[0] else players[1]
    winning_score = compute_score(winner)

    return winning_score



num_games = 1

results = {}

def recursive_combat(player_one, player_two):
    global num_games
    game_num = num_games

    round_num = 1
    previous_rounds = set()

    initial_key = (player_one, player_two)
    if initial_key in results:
        return results[initial_key]
    num_games += 1
    player_one = list(player_one)
    player_two = list(player_two)
    while player_one and player_two:
        #print(f'-- Round {round_num} (Game {game_num}) --')
        key = (tuple(player_one),tuple(player_two))
        if key in previous_rounds:
            results[initial_key] = 0
            return 0
        previous_rounds.add(key)
        round_num += 1

        a, b = (hand.pop(0) for hand in (player_one, player_two))
        if a > len(player_one) or b > len(player_two):
            #This is simple mode
            if a > b:
                player_one.extend([a,b])
            else:
                player_two.extend([b,a])
            continue
        #Time for recursive combat!
        winner = recursive_combat(tuple(player_one[:a]), tuple(player_two[:b]))
        if winner == 0:
            player_one.extend([a,b])
        else:
            player_two.extend([b,a])

    if game_num == 1:
        result = compute_score(player_one) if player_one else compute_score(player_two)
    else:
        result = 0 if player_one else 1
    results[initial_key] = result
    return result

part_1 = basic_game(*players)
print(f'Part 1 {part_1}')

part_2 = recursive_combat(tuple(players[0]), tuple(players[1]))
print(f'Part 2 {part_2}')
