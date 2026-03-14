#include <cstdint>
#include <emscripten.h>
#include <cmath> 

const int WIDTH = 200;
const int HEIGHT = 200;
const int GRID_SIZE = WIDTH * HEIGHT;

// 0 = empty, 1 = adult, 2 = newborn, 3 = just moved (prevents double-moving)
uint8_t grid[GRID_SIZE];
int newborns_buffer[GRID_SIZE];

uint32_t rng_state = 123456789;

inline uint32_t xorshift32() {
    uint32_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    rng_state = x;
    return x;
}

inline float randomFloat() {
    return (xorshift32() & 0xFFFFFF) / 16777216.0f; 
}

extern "C" {

    EMSCRIPTEN_KEEPALIVE
    uint8_t* getGridPointer() { return grid; }

    EMSCRIPTEN_KEEPALIVE
    void clearGrid() {
        for (int i = 0; i < GRID_SIZE; i++) grid[i] = 0;
    }

    EMSCRIPTEN_KEEPALIVE
    void setSeed(uint32_t seed) {
        rng_state = (seed == 0) ? 1 : seed; 
    }

    // Notice we changed 'float mobility' to 'int distance'
    EMSCRIPTEN_KEEPALIVE
    int stepSimulation(float alpha, int distance, uint32_t optionalSeed) {
        
        if (optionalSeed != 0) rng_state = optionalSeed;

        // 1. Maturation
        for (int i = 0; i < GRID_SIZE; i++) {
            if (grid[i] == 2) grid[i] = 1;
        }

        // 2. Mobility Phase (Distance-based Jump)
        for (int i = 0; i < GRID_SIZE; i++) {
            if (grid[i] == 1) {
                int y = i / WIDTH;
                int x = i % WIDTH;
                
                // distance here acts as 'R'
                float radius = (float)distance;
                
                // Get a random angle between 0 and 2*PI
                float theta = randomFloat() * 2.0f * 3.14159265f;

                // Calculate displacement
                int dx = (int)roundf(radius * cosf(theta));
                int dy = (int)roundf(radius * sinf(theta));

                int nx = x + dx;
                int ny = y + dy;

                // Boundary check and collision check
                if (nx >= 0 && nx < WIDTH && ny >= 0 && nx < HEIGHT) {
                    int target = ny * WIDTH + nx;
                    if (grid[target] == 0) {
                        grid[i] = 0;
                        grid[target] = 3; 
                    }
                }
            }
        }

        // Convert the '3's (recently moved) back to '1's (normal adults)
        for (int i = 0; i < GRID_SIZE; i++) {
            if (grid[i] == 3) grid[i] = 1;
        }

        // 3. Reproduction Phase
        int newborn_count = 0;

        for (int i = 0; i < GRID_SIZE; i++) {
            if (grid[i] == 1) {
                int y = i / WIDTH;
                int x = i % WIDTH;
                
                int empty[4];
                int empty_count = 0;

                // Create and shuffle direction array (0: left, 1: right, 2: up, 3: down)
                int dirs[4] = {0, 1, 2, 3};
                for (int k = 3; k > 0; --k) {
                    int j = xorshift32() % (k + 1);
                    int temp = dirs[k];
                    dirs[k] = dirs[j];
                    dirs[j] = temp;
                }

                // Check neighbors in the randomized order
                for (int k = 0; k < 4; ++k) {
                    if      (dirs[k] == 0 && x > 0 && grid[i - 1] == 0) empty[empty_count++] = i - 1;
                    else if (dirs[k] == 1 && x < WIDTH - 1 && grid[i + 1] == 0) empty[empty_count++] = i + 1;
                    else if (dirs[k] == 2 && y > 0 && grid[i - WIDTH] == 0) empty[empty_count++] = i - WIDTH;
                    else if (dirs[k] == 3 && y < HEIGHT - 1 && grid[i + WIDTH] == 0) empty[empty_count++] = i + WIDTH;
                }

                if (empty_count > 0 && randomFloat() < alpha) {
                    newborns_buffer[newborn_count++] = empty[xorshift32() % empty_count];
                }
            }
        }

        // 4. Apply newborns
        for (int i = 0; i < newborn_count; i++) {
            grid[newborns_buffer[i]] = 2;
        }

        // 5. Count total population
        int count = 0;
        for (int i = 0; i < GRID_SIZE; i++) {
            if (grid[i] == 1 || grid[i] == 2) count++;
        }

        return count;
    }
}