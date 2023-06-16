import pygame
import random
import queue
import time
import heapq

# Inisialisasi Pygame
pygame.init()

# Inisialisasi modul mixer
pygame.mixer.init()

# Muat musik
music = pygame.mixer.Sound("music.mp3")

# Putar musik
music.play(-1)

# Set ukuran layar
screen_width = 700  # Lebar layar termasuk lebar menu
screen_height = 533
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Athena Teknik")

# Membuat dan mengganti logo/icon screen
icon = pygame.image.load("Logo.jpg")
pygame.display.set_icon(icon)

# Ukuran kotak pada peta
map_width = 37 # Lebar peta sedikit lebih kecil
map_height = 41
tile_size = 13

# Membuat peta dengan semua dinding
game_map = [[1] * map_height for _ in range(map_width)]

droidh_vision = 4  # Nilai awal pandangan DroidH

# Fungsi untuk membuat jalan dengan Recursive Backtracking
def create_maze(x, y):
    game_map[x][y] = 0  # Tandai posisi saat ini sebagai jalan
    
    # Daftar arah yang mungkin
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(directions)
    
    # Coba untuk bergerak ke setiap arah secara acak
    for dx, dy in directions:
        nx, ny = x + dx * 2, y + dy * 2  # Koordinat sel setelah dinding
        
        # Cek apakah sel setelah dinding masih berada dalam peta
        if 0 <= nx < map_width and 0 <= ny < map_height and game_map[nx][ny] == 1:
            game_map[x + dx][y + dy] = 0  # Hapus dinding di antara
            create_maze(nx, ny)  # Lanjutkan rekursi

# Membuat peta acak
create_maze(1, 1)

# Membuat font untuk teks di menu
font = pygame.font.Font(None, 24)

# Menyimpan pilihan menu yang aktif
active_menu = None

# Melacak apakah proses pembuatan peta sedang berlangsung
is_creating_maze = False

droidm_path = []  # Path yang akan diikuti oleh DroidM

additional_droidm_positions = []  # Inisialisasi list posisi DroidM tambahan

# Mencari posisi yang valid untuk DroidM dan DroidH
valid_positions = []
for x in range(map_width):
    for y in range(map_height):
        if game_map[x][y] == 0:
            valid_positions.append((x, y))

# Mengacak posisi DroidM
droidm_position = random.choice(valid_positions)
droidm_x, droidm_y = droidm_position

# Mengacak posisi DroidH
droidh_position = random.choice(valid_positions)
droidh_x, droidh_y = droidh_position

# Membuat fungsi untuk menggambar peta
def draw_map():
    for x in range(map_width):
        for y in range(map_height):
            if game_map[x][y] == 0:
                # Warna putih
                color = (255, 255, 255)
                # Menggeser peta ke kanan
                rect = pygame.Rect(x * tile_size + 210, y * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, color, rect)
            else:
                # Warna hitam
                color = (0, 0, 0)
                rect = pygame.Rect(x * tile_size + 210, y * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, color, rect)
                
    # Menggambar DroidM
    if game_map[droidm_x][droidm_y] == 0:
        droidm_rect = pygame.Rect(droidm_x * tile_size + 210, droidm_y * tile_size, tile_size, tile_size)
        droidm_img = pygame.image.load("DroidM.png")
        screen.blit(droidm_img, droidm_rect)
    
    # Menggambar DroidH
    if game_map[droidh_x][droidh_y] == 0:
        droidh_rect = pygame.Rect(droidh_x * tile_size + 210, droidh_y * tile_size, tile_size, tile_size)
        droidh_img = pygame.image.load("DroidH.png")
        screen.blit(droidh_img, droidh_rect)
    
    # Menggambar DroidM tambahan
    for position in additional_droidm_positions:
        if game_map[position[0]][position[1]] == 0:
            droidm_rect = pygame.Rect(position[0] * tile_size + 210, position[1] * tile_size, tile_size, tile_size)
            droidm_img = pygame.image.load("DroidM.png")
            screen.blit(droidm_img, droidm_rect)
        
# Membuat fungsi untuk menggambar menu
def draw_menu():
    # Menggambar latar belakang menu
    # Mengubah lebar menu menjadi 210
    menu_bg = pygame.Rect(0, 0, 205, screen_height)
    pygame.draw.rect(screen, (41, 41, 41), menu_bg)

    # Menggambar pilihan menu
    menu_options = ["Acak Peta", "Mulai", "Tambah DroidM", "Hapus DroidM", "Acak Posisi DroidM", "Acak Posisi DroidH", "Berhenti", "Pandangan DroidM", "Pandangan DroidH", "Keluar"]
    option_y = 50
    for option in menu_options:
        text = font.render(option, True, (57, 255, 20))
        text_rect = text.get_rect()
        text_rect.center = (100, option_y + text_rect.height / 2)

        # Menggambar tampilan button bar jika menu aktif
        if active_menu == option:
            button_rect = pygame.Rect(text_rect.left - 5, text_rect.top, text_rect.width + 10, text_rect.height)

            # Mengubah warna tombol saat diklik
            if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (0, 0, 0), button_rect)
                
            else:
                pygame.draw.rect(screen, (0, 0, 0), button_rect)

        pygame.draw.rect(screen, (168, 169, 169), text_rect.inflate(10, 10), width=2)
        screen.blit(text, text_rect)
        option_y += text_rect.height + 25

    # Menambahkan judul pada menu
    title = font.render("Menu Game", True, (255, 255, 255))
    title_rect = title.get_rect()
    title_rect.center = (100, 20)
    screen.blit(title, title_rect)
    
    # Menggambar slider pandangan DroidH
    if active_menu == "Pandangan DroidH":
        slider_label = "Atur Pandangan: "
        min_value = 0  # Nilai minimum pandangan DroidH
        max_value = 11  # Nilai maksimum pandangan DroidH
        global droidh_vision
        droidh_vision = draw_slider(slider_label, min_value, max_value, droidh_vision, 25, 470)
    
# Membuat fungsi untuk menggambar pandangan DroidM
def draw_droidm_vision():
    vision_radius = 0  # Radius pandangan DroidM

    for ny in range(map_height):
        for nx in range(map_width):
            rect = pygame.Rect((nx * tile_size) + 210, ny * tile_size, tile_size, tile_size)
            if abs(nx - droidm_x) + abs(ny - droidm_y) <= vision_radius:
                # Gambar area dalam radius pandangan dengan efek blur biru
                surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                alpha = 128  # Nilai transparansi, 0 (transparan) hingga 255 (solid)
            else:
                # Gambar area di luar radius pandangan dengan efek blur biru
                surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                alpha = 64  # Nilai transparansi, 0 (transparan) hingga 255 (solid)
                surface.fill((0, 0, 0, alpha))
                screen.blit(surface, rect)
                
    # Tidak menampilkan posisi droid hijau
    droidh_rect = pygame.Rect((droidh_x * tile_size) + 210, droidh_y * tile_size, tile_size, tile_size)
    pygame.draw.rect(screen, (0, 0, 0), droidh_rect)

def draw_slider(label, min_value, max_value, current_value, x, y):
    # Menggambar label
    label_text = font.render(label, True, (57, 255, 20))
    label_rect = label_text.get_rect()
    label_rect.topleft = (x, y)
    screen.blit(label_text, label_rect)

    # Menggambar bar
    bar_width = 100
    bar_height = 10
    bar_rect = pygame.Rect(x, y + 20, bar_width, bar_height)
    pygame.draw.rect(screen, (0, 0, 0), bar_rect)

    # Menggambar handle slider
    handle_radius = 5
    handle_x = x + int((current_value - min_value) / (max_value - min_value) * bar_width)
    handle_y = y + 20 + bar_height // 2
    handle_rect = pygame.Rect(handle_x - handle_radius, handle_y - handle_radius, handle_radius * 2, handle_radius * 2)
    pygame.draw.circle(screen, (57, 255, 20), (handle_x, handle_y), handle_radius)

    # Menampilkan nilai saat ini
    value_text = font.render(str(current_value), True, (255, 255, 255))
    value_rect = value_text.get_rect()
    value_rect.midtop = (x + bar_width // 2, y + 40)
    screen.blit(value_text, value_rect)

    # Menangani interaksi slider
    if pygame.mouse.get_pressed()[0] and bar_rect.collidepoint(pygame.mouse.get_pos()):
        # Mendapatkan posisi klik mouse pada slider
        mouse_x = pygame.mouse.get_pos()[0]
        # Menghitung nilai berdasarkan posisi klik mouse
        current_value = min_value + (mouse_x - x) / bar_width * (max_value - min_value)
        # Memastikan nilai tetap dalam rentang yang valid
        current_value = max(min_value, min(max_value, current_value))

    return int(current_value)
            
# Membuat fungsi untuk menggambar pandangan DroidH
def draw_droidh_vision():
    # Radius pandangan DroidH (horizontal)
    vision_radius = 4 
    vision_radius = droidh_vision  # Gunakan nilai pandangan DroidH yang baru

    for ny in range(map_height):
        for nx in range(map_width):
            rect = pygame.Rect((nx * tile_size) + 210, ny * tile_size, tile_size, tile_size)

            # Menentukan batas koordinat kotak pandangan DroidH
            left = droidh_x - vision_radius
            right = droidh_x + vision_radius
            top = droidh_y - vision_radius
            bottom = droidh_y + vision_radius

            # Mengecek apakah posisi saat ini berada dalam kotak pandangan DroidH
            if left <= nx <= right and top <= ny <= bottom:
                # Gambar area dalam kotak pandangan dengan warna biru solid
                surface = pygame.Surface((tile_size, tile_size))
            else:
                # Tutupi area di luar kotak pandangan dengan warna hitam
                surface = pygame.Surface((tile_size, tile_size))
                surface.fill((0, 0, 0))
                screen.blit(surface, rect)

            droidm_radius = tile_size // 2 
            droidm_center_x = (droidm_x * tile_size) + 210 + droidm_radius
            droidm_center_y = droidm_y * tile_size + droidm_radius
            droidm_center = (droidm_center_x, droidm_center_y)
            pygame.draw.circle(screen, (255, 0, 0), droidm_center, droidm_radius)

# Algoritma BFS Untuk Droid Merah
def bfs_search(start_x, start_y, target_x, target_y):
    # Inisialisasi antrian untuk menyimpan posisi yang akan dikunjungi
    q = queue.Queue()

    # Inisialisasi array visited untuk melacak posisi yang sudah dikunjungi
    visited = [[False] * map_height for _ in range(map_width)]

    # Inisialisasi array parent untuk melacak jalur yang dilewati
    parent = [[None] * map_height for _ in range(map_width)]

    # Tambahkan posisi awal ke antrian
    q.put((start_x, start_y))
    visited[start_x][start_y] = True

    # Loop sampai antrian kosong atau target ditemukan
    while not q.empty():
        current_x, current_y = q.get()

        # Jika target ditemukan, keluar dari loop
        if current_x == target_x and current_y == target_y:
            break

        # Cek semua tetangga yang mungkin
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_x, next_y = current_x + dx, current_y + dy

            # Periksa apakah tetangga valid dan belum dikunjungi
            if 0 <= next_x < map_width and 0 <= next_y < map_height and not visited[next_x][next_y] and game_map[next_x][next_y] == 0:
                q.put((next_x, next_y))
                visited[next_x][next_y] = True
                parent[next_x][next_y] = (current_x, current_y)

    # Rekonstruksi jalur yang dilewati
    path = []
    x, y = target_x, target_y
    while (x, y) != (start_x, start_y):
        path.append((x, y))
        x, y = parent[x][y]

    # Balikkan jalur secara terbalik agar dari start ke target
    return path[::-1]

# Algoritma BFS Untuk Droid Merah Tambahan
def bfs_search_additional(start_x, start_y, target_x, target_y):
    # Inisialisasi antrian untuk menyimpan posisi yang akan dikunjungi
    q = queue.Queue()

    # Inisialisasi array visited untuk melacak posisi yang sudah dikunjungi
    visited = [[False] * map_height for _ in range(map_width)]

    # Inisialisasi array parent untuk melacak jalur yang dilewati
    parent = [[None] * map_height for _ in range(map_width)]

    # Tambahkan posisi awal ke antrian
    q.put((start_x, start_y))
    visited[start_x][start_y] = True

    # Loop sampai antrian kosong atau target ditemukan
    while not q.empty():
        current_x, current_y = q.get()

        # Jika target ditemukan, keluar dari loop
        if current_x == target_x and current_y == target_y:
            break

        # Cek semua tetangga yang mungkin
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_x, next_y = current_x + dx, current_y + dy

            # Periksa apakah tetangga valid dan belum dikunjungi
            if 0 <= next_x < map_width and 0 <= next_y < map_height and not visited[next_x][next_y] and game_map[next_x][next_y] == 0:
                q.put((next_x, next_y))
                visited[next_x][next_y] = True
                parent[next_x][next_y] = (current_x, current_y)

    # Rekonstruksi jalur yang dilewati
    path = []
    x, y = target_x, target_y
    while (x, y) != (start_x, start_y):
        path.append((x, y))
        x, y = parent[x][y]

    # Balikkan jalur secara terbalik agar dari start ke target
    return path[::-1]

# Fungsi heuristik untuk algoritma A*
def heuristic(x1, y1, x2, y2):
    # Menghitung jarak Manhattan antara dua titik
    return abs(x1 - x2) + abs(y1 - y2)

# Algoritma A* untuk Droid Hijau
def a_star_search(start_x, start_y, target_x, target_y):
    # Inisialisasi heap untuk menyimpan posisi yang akan dikunjungi
    heap = []

    # Inisialisasi dictionary untuk melacak cost sejauh ini dari posisi awal ke setiap posisi
    cost_so_far = {}

    # Inisialisasi array parent untuk melacak jalur yang dilewati
    parent = {}

    # Menambahkan posisi awal ke heap dengan cost 0
    heapq.heappush(heap, (0, start_x, start_y))
    cost_so_far[(start_x, start_y)] = 0
    parent[(start_x, start_y)] = None

    # Loop sampai heap kosong atau target ditemukan
    while heap:
        current_cost, current_x, current_y = heapq.heappop(heap)

        # Jika target ditemukan, keluar dari loop
        if current_x == target_x and current_y == target_y:
            break

        # Cek semua tetangga yang mungkin
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_x, next_y = current_x + dx, current_y + dy

            # Periksa apakah tetangga valid
            if 0 <= next_x < map_width and 0 <= next_y < map_height and game_map[next_x][next_y] == 0:
                new_cost = cost_so_far[(current_x, current_y)] + 1

                # Periksa apakah tetangga sudah dikunjungi atau memiliki cost yang lebih rendah
                if (next_x, next_y) not in cost_so_far or new_cost < cost_so_far[(next_x, next_y)]:
                    cost_so_far[(next_x, next_y)] = new_cost

                    # Jika jarak antara Droid Merah dan Droid Hijau kurang dari atau sama dengan 5, pilih tetangga dengan jarak terjauh
                    if heuristic(next_x, next_y, droidm_x, droidm_y) <= 5:
                        priority = -heuristic(next_x, next_y, droidm_x, droidm_y)  # Menggunakan negatif heuristic untuk memaksimalkan jarak
                    else:
                        priority = new_cost + heuristic(next_x, next_y, target_x, target_y)

                    heapq.heappush(heap, (priority, next_x, next_y))
                    parent[(next_x, next_y)] = (current_x, current_y)

    # Rekonstruksi jalur yang dilewati
    path = []
    x, y = target_x, target_y
    while (x, y) != (start_x, start_y):
        path.append((x, y))
        x, y = parent[(x, y)]

    # Balikkan jalur secara terbalik agar dari start ke target
    return path[::-1]

# Fungsi untuk menggambar peta dan objek-objek di dalamnya
def draw_game():
    screen.fill((0, 0, 0))  # Warna latar belakang hitam
    
    # Menggambar peta
    for x in range(map_width):
        for y in range(map_height):
            rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            if game_map[x][y] == 1:
                pygame.draw.rect(screen, (0, 0, 255), rect)
            else:
                pygame.draw.rect(screen, (255, 255, 255), rect)
    
    # Menggambar DroidM
    pygame.draw.circle(screen, (255, 0, 0), (droidm_x * tile_size + tile_size // 2, droidm_y * tile_size + tile_size // 2), tile_size // 2)
    
    # Menggambar DroidH
    pygame.draw.circle(screen, (0, 255, 0), (droidh_x * tile_size + tile_size // 2, droidh_y * tile_size + tile_size // 2), tile_size // 2)
    
#Hendle Menu Bar                
def handle_menu_choice(choice):
    global active_menu, is_creating_maze, droidm_x, droidm_y, droidm_position, droidh_x, droidh_y, droidh_position, game_map, droidm_count

    active_menu = choice
    print(f"Pilihan menu: {choice}")

    if choice == "Acak Peta":
          # Membuat peta acak ulang
        create_maze(1, 1)
        is_creating_maze = True
        game_map = [[1] * map_height for _ in range(map_width)]  # Mengatur ulang peta dengan semua dinding
        droidm_position = random.choice(valid_positions)
        droidm_x, droidm_y = droidm_position
    
    elif choice == "Tambah DroidM":
        # Menambah DroidM pada posisi acak
        new_position = random.choice(valid_positions)
        additional_droidm_positions.append(new_position)

    elif choice == "Acak Posisi DroidM":
        # Mengacak posisi DroidM
        droidm_position = random.choice(valid_positions)
        droidm_x, droidm_y = droidm_position
        
    elif choice == "Acak Posisi DroidH":
        # Mengacak posisi DroidH
        droidh_position = random.choice(valid_positions)
        droidh_x, droidh_y = droidh_position
    
    elif choice == "Hapus DroidM":
        # Menghapus DroidM yang ditambahkan sebelumnya
        if additional_droidm_positions:
            additional_droidm_positions.pop()

# Membuat game loop
running = True
last_move_time_droidm = time.time()  # Waktu terakhir DroidM bergerak
last_move_time_droidh = time.time()  # Waktu terakhir DroidH berger
last_move_time_additional = time.time() # Waktu terakhir DroidM tambahan bergerak
while running:
    current_time = time.time()
    # Menghandle event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Mendapatkan posisi klik mouse
            pos = pygame.mouse.get_pos()

            # Mengecek apakah posisi klik mouse berada pada salah satu opsi menu
            menu_options = ["Acak Peta", "Mulai", "Tambah DroidM", "Hapus DroidM", "Acak Posisi DroidM", "Acak Posisi DroidH", "Berhenti", "Pandangan DroidM", "Pandangan DroidH", "Keluar"]
            option_y = 50
            for option in menu_options:
                text = font.render(option, True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = (100, option_y + text_rect.height / 2)
                if text_rect.collidepoint(pos):
                    handle_menu_choice(option)
                    if option == "Keluar":
                        running = False
                option_y += text_rect.height + 25
        
    # Jika sedang dalam proses pembuatan peta, lakukan pembuatan peta acak
    if is_creating_maze:
        create_maze(1, 1)
        is_creating_maze = False
        droidm_step = 0  # Atur langkah DroidM kembali ke 0 setelah peta diacak ulang
        
    # Menggambar peta
    draw_map()
    
    # Memperbarui posisi DroidM jika ada jalur yang ditemukan
    if active_menu == "Mulai" and current_time - last_move_time_droidm >= 0.2:
        path_droidm = bfs_search(droidm_x, droidm_y, droidh_x, droidh_y)
        if path_droidm:
            droidm_x, droidm_y = path_droidm[0]
            last_move_time_droidm = current_time  # Mengupdate waktu terakhir DroidM bergerak
            
            # Cek apakah DroidM telah menemukan posisi DroidH
            if (droidm_x, droidm_y) == (droidh_x, droidh_y):
                print("Droid Merah Telah Menemukan Posisi Droid Hijau!")
                break
                  
    # Memperbarui posisi Droid Merah Tambahan jika ada jalur yang ditemukan
    if active_menu == "Mulai" and current_time - last_move_time_additional >= 0.2:
        for i in range(len(additional_droidm_positions)):
            path_additional = bfs_search_additional(additional_droidm_positions[i][0], additional_droidm_positions[i][1], droidh_x, droidh_y)
            if path_additional:
                additional_droidm_positions[i] = path_additional[0]
            
                # Cek apakah DroidM Tambahan menempel pada DroidH
                if additional_droidm_positions[i][0] == droidh_x and additional_droidm_positions[i][1] == droidh_y:
                    print("Droid Merah Tambahan Telah Menemukan Posisi Droid Hijau!")
                    break
        
        last_move_time_additional = current_time  # Mengupdate waktu terakhir DroidM Tambahan bergerak
    
    jarak_tertentu = 5

    # Memperbarui posisi DroidH jika ada jalur yang ditemukan
    if active_menu == "Mulai" and current_time - last_move_time_droidh >= 0.2:
        # Periksa apakah Droid Merah berada dalam jarak tertentu
        if heuristic(droidh_x, droidh_y, droidm_x, droidm_y) <= jarak_tertentu:
            # Mencari tetangga terjauh yang dapat dijangkau
            farthest_neighbor = None
            farthest_distance = 0
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_x, next_y = droidh_x + dx, droidh_y + dy
                if 0 <= next_x < map_width and 0 <= next_y < map_height and game_map[next_x][next_y] == 0:
                    distance = heuristic(next_x, next_y, droidm_x, droidm_y)
                    if distance > farthest_distance:
                        farthest_neighbor = (next_x, next_y)
                        farthest_distance = distance

            if farthest_neighbor:
                droidh_x, droidh_y = farthest_neighbor
        else:
            path_droidh = a_star_search(droidh_x, droidh_y, droidm_x, droidm_y)
            if path_droidh:
                droidh_x, droidh_y = path_droidh[0]
                last_move_time_droidh = current_time  # Mengupdate waktu terakhir DroidH bergerak
            else:
                break  # Menghentikan program setelah DroidH tidak dapat menemukan jalur

    # Menggambar menu
    draw_menu()

    # Menggambar pandangan DroidM
    if active_menu == "Pandangan DroidM":
        draw_droidm_vision()
    # Menggambar pandangan DroidH
    if active_menu == "Pandangan DroidH":
        draw_droidh_vision()
        
    # Update layar
    pygame.display.update()

# Keluar dari Pygame
pygame.mixer.quit()
pygame.quit()