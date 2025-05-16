 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a//dev/null b/map_game.py
index 0000000..3e68641 100644
--- a//dev/null
+++ b/map_game.py
@@ -0,0 +1,99 @@
+import random
+import os
+
+MAP = [
+    "####################",
+    "#...........#......#",
+    "#..#######..#..##..#",
+    "#..#.....#..#..##..#",
+    "#..#.E...#..#......#",
+    "#..#####.#..########",
+    "#S.......#........##",
+    "####################"
+]
+
+WALL = '#'
+EMPTY = '.'
+EXIT = 'E'
+START = 'S'
+PLAYER = 'P'
+COIN = 'C'
+
+def clear_screen():
+    os.system('clear' if os.name == 'posix' else 'cls')
+
+def find_symbol(symbol):
+    for y, row in enumerate(MAP):
+        x = row.find(symbol)
+        if x != -1:
+            return x, y
+    return None
+
+def place_coins(count=5):
+    global coins
+    coins = {}
+    open_cells = [(x, y) for y, row in enumerate(MAP) for x, c in enumerate(row) if c == EMPTY]
+    for _ in range(count):
+        if not open_cells:
+            break
+        x, y = random.choice(open_cells)
+        open_cells.remove((x, y))
+        coins[(x, y)] = True
+
+
+def draw_map(player_pos):
+    clear_screen()
+    for y, row in enumerate(MAP):
+        row_chars = list(row)
+        for x in range(len(row_chars)):
+            if (x, y) == player_pos:
+                row_chars[x] = PLAYER
+            elif (x, y) in coins:
+                row_chars[x] = COIN
+        print(''.join(row_chars))
+    print(f"Coins remaining: {len(coins)}")
+
+
+def main():
+    player_pos = find_symbol(START)
+    if not player_pos:
+        raise ValueError("No starting position 'S' defined on map")
+    place_coins()
+
+    while True:
+        draw_map(player_pos)
+        move = input("Move (w/a/s/d or q to quit): ").lower()
+        if move == 'q':
+            print("Thanks for playing!")
+            break
+        x, y = player_pos
+        if move == 'w':
+            y -= 1
+        elif move == 's':
+            y += 1
+        elif move == 'a':
+            x -= 1
+        elif move == 'd':
+            x += 1
+        new_pos = (x, y)
+
+        if (0 <= y < len(MAP)) and (0 <= x < len(MAP[y])) and MAP[y][x] != WALL:
+            player_pos = new_pos
+            if new_pos in coins:
+                coins.pop(new_pos)
+                print("You collected a coin!")
+                input("Press Enter to continue...")
+            if MAP[y][x] == EXIT:
+                if coins:
+                    print("Collect all coins before exiting!")
+                    input("Press Enter to continue...")
+                else:
+                    draw_map(player_pos)
+                    print("Congratulations! You reached the exit.")
+                    break
+        else:
+            print("You hit a wall!")
+            input("Press Enter to continue...")
+
+if __name__ == "__main__":
+    main()
 
EOF
)
