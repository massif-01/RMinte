# RM logo 灯板
## 坐标 (Y,X)
(8,11),(8,22),(8,23),(8,24),(9,9),(9,10),(9,11),(9,12),(9,13),(9,20),(9,21),(9,22),(9,23),(9,24),(9,25),(10,8),(10,9),(10,10),(10,11),(10,12),(10,13),(10,14),(10,15),(10,18),(10,19),(10,20),(10,21),(10,22),(10,23),(11,8),(11,9),(11,10),(11,11),(11,12),(11,13),(11,14),(11,15),(11,16),(11,17),(11,18),(11,19),(11,20),(11,21),(11,22),(12,8),(12,9),(12,10),(12,14),(12,15),(12,16),(12,17),(12,18),(12,19),(12,23),(13,8),(13,9),(13,10),(13,15),(13,16),(13,17),(13,18),(13,23),(13,24),(14,8)(14,9)(14,10),(14,15),(14,16),(14,17),(14,18),(14,23),(14,24),(14,25),(15,8),(15,9),(15,10),(15,15),(15,16),(15,17),(15,18),(15,23),(15,24),(15,25),(16,8),(16,9),(16,10),(16,15),(16,16),(16,17),(16,18),(16,23),(16,24),(16,25),(17,8),(17,9),(17,10),(17,15),(17,16),(17,17),(17,18),(17,23),(17,24),(17,25),(18,9),(18,10),(18,15),(18,16),(18,17),(18,18),(18,23),(18,24),(18,25),(19,10),(19,13),(19,14),(19,15),(19,16),(19,17),(19,18),(19,19),(19,20),(19,23),(19,24),(19,25),(20,11),(20,12),(20,13),(20,14),(20,15),(20,16),(20,17),(20,18),(20,19),(20,20),(20,21),(20,22),(20,23),(20,24),(20,25),(21,10),(21,11),(21,12),(21,13),(21,14),(21,15),(21,18),(21,19),(21,20),(21,21),(21,22),(21,23),(21,24),(21,25),(22,8),(22,9),(22,10),(22,11),(22,12),(22,13),(22,20),(22,21),(22,22),(22,23),(22,24),(23,9),(23,10),(23,11),(23,22)

## 静止代码

```
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "led_strip.h"

// LED matrix parameters
#define LED_PIN GPIO_NUM_16  // ESP32 control pin
#define WIDTH 32             // Matrix width
#define HEIGHT 32            // Matrix height
#define NUM_LEDS (WIDTH * HEIGHT) // Total LEDs: 1024

// RGB structure
typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} RGB;

// Color correction function
RGB color_correct(uint8_t input_r, uint8_t input_g, uint8_t input_b) {
    RGB result;
    const RGB black = {0, 0, 0};
    const RGB min_white = {5, 4, 3};
    const RGB max_white = {168, 112, 76};
    const float input_min = 5.0f;
    const float input_max = 255.0f;

    const float r_slope = (float)(max_white.r - min_white.r) / (input_max - input_min);
    const float g_slope = (float)(max_white.g - min_white.g) / (input_max - input_min);
    const float b_slope = (float)(max_white.b - min_white.b) / (input_max - input_min);

    const float r_intercept = min_white.r - r_slope * input_min;
    const float g_intercept = min_white.g - g_slope * input_min;
    const float b_intercept = min_white.b - b_slope * input_min;

    float temp_r, temp_g, temp_b;
    if (input_r <= 5 && input_g <= 5 && input_b <= 5) {
        temp_r = (float)input_r * (min_white.r / input_min);
        temp_g = (float)input_g * (min_white.g / input_min);
        temp_b = (float)input_b * (min_white.b / input_min);
    } else {
        temp_r = (float)input_r * r_slope + r_intercept;
        temp_g = (float)input_g * g_slope + g_intercept;
        temp_b = (float)input_b * b_slope + b_intercept;
    }

    temp_r = (temp_r < black.r) ? black.r : (temp_r > max_white.r) ? max_white.r : temp_r;
    temp_g = (temp_g < black.g) ? black.g : (temp_g > max_white.g) ? max_white.g : temp_g;
    temp_b = (temp_b < black.b) ? black.b : (temp_b > max_white.b) ? max_white.b : temp_b;

    result.r = (uint8_t)(temp_r + 0.5f);
    result.g = (uint8_t)(temp_g + 0.5f);
    result.b = (uint8_t)(temp_b + 0.5f);
    
    return result;
}

// Global variables
static led_strip_handle_t led_strip;
static uint8_t grid[HEIGHT][WIDTH][3]; // RGB grid

// Initialize LED and matrix
void matrix_init() {
    led_strip_config_t strip_config = {
        .strip_gpio_num = LED_PIN,
        .max_leds = NUM_LEDS,
    };
    led_strip_rmt_config_t rmt_config = {
        .clk_src = RMT_CLK_SRC_DEFAULT,
        .resolution_hz = 10 * 1000 * 1000, // 10MHz
        .flags.with_dma = false,
    };
    ESP_ERROR_CHECK(led_strip_new_rmt_device(&strip_config, &rmt_config, &led_strip));
    
    led_strip_clear(led_strip);
    memset(grid, 0, sizeof(grid));
}

// Define a function to set a specific point with a color
void set_point(int y, int x, uint8_t r, uint8_t g, uint8_t b) {
    if (y >= 0 && y < HEIGHT && x >= 0 && x < WIDTH) {
        grid[y][x][0] = r;
        grid[y][x][1] = g;
        grid[y][x][2] = b;
    }
}

// Update matrix with specified points
void update_matrix() {
    // Clear grid (set all to dark background)
    memset(grid, 0, sizeof(grid));
    
    // Set all specified points with a bright color
    // Using white (255, 255, 255) for visibility
    
    // Points list (y,x)
    set_point(8, 11, 255, 255, 255);
    set_point(8, 22, 255, 255, 255);
    set_point(8, 23, 255, 255, 255);
    set_point(8, 24, 255, 255, 255);
    set_point(9, 9, 255, 255, 255);
    set_point(9, 10, 255, 255, 255);
    set_point(9, 11, 255, 255, 255);
    set_point(9, 12, 255, 255, 255);
    set_point(9, 13, 255, 255, 255);
    set_point(9, 20, 255, 255, 255);
    set_point(9, 21, 255, 255, 255);
    set_point(9, 22, 255, 255, 255);
    set_point(9, 23, 255, 255, 255);
    set_point(9, 24, 255, 255, 255);
    set_point(9, 25, 255, 255, 255);
    set_point(10, 8, 255, 255, 255);
    set_point(10, 9, 255, 255, 255);
    set_point(10, 10, 255, 255, 255);
    set_point(10, 11, 255, 255, 255);
    set_point(10, 12, 255, 255, 255);
    set_point(10, 13, 255, 255, 255);
    set_point(10, 14, 255, 255, 255);
    set_point(10, 15, 255, 255, 255);
    set_point(10, 18, 255, 255, 255);
    set_point(10, 19, 255, 255, 255);
    set_point(10, 20, 255, 255, 255);
    set_point(10, 21, 255, 255, 255);
    set_point(10, 22, 255, 255, 255);
    set_point(10, 23, 255, 255, 255);
    set_point(11, 8, 255, 255, 255);
    set_point(11, 9, 255, 255, 255);
    set_point(11, 10, 255, 255, 255);
    set_point(11, 11, 255, 255, 255);
    set_point(11, 12, 255, 255, 255);
    set_point(11, 13, 255, 255, 255);
    set_point(11, 14, 255, 255, 255);
    set_point(11, 15, 255, 255, 255);
    set_point(11, 16, 255, 255, 255);
    set_point(11, 17, 255, 255, 255);
    set_point(11, 18, 255, 255, 255);
    set_point(11, 19, 255, 255, 255);
    set_point(11, 20, 255, 255, 255);
    set_point(11, 21, 255, 255, 255);
    set_point(11, 22, 255, 255, 255);
    set_point(12, 8, 255, 255, 255);
    set_point(12, 9, 255, 255, 255);
    set_point(12, 10, 255, 255, 255);
    set_point(12, 14, 255, 255, 255);
    set_point(12, 15, 255, 255, 255);
    set_point(12, 16, 255, 255, 255);
    set_point(12, 17, 255, 255, 255);
    set_point(12, 18, 255, 255, 255);
    set_point(12, 19, 255, 255, 255);
    set_point(12, 23, 255, 255, 255);
    set_point(13, 8, 255, 255, 255);
    set_point(13, 9, 255, 255, 255);
    set_point(13, 10, 255, 255, 255);
    set_point(13, 15, 255, 255, 255);
    set_point(13, 16, 255, 255, 255);
    set_point(13, 17, 255, 255, 255);
    set_point(13, 18, 255, 255, 255);
    set_point(13, 23, 255, 255, 255);
    set_point(13, 24, 255, 255, 255);
    set_point(14, 8, 255, 255, 255);
    set_point(14, 9, 255, 255, 255);
    set_point(14, 10, 255, 255, 255);
    set_point(14, 15, 255, 255, 255);
    set_point(14, 16, 255, 255, 255);
    set_point(14, 17, 255, 255, 255);
    set_point(14, 18, 255, 255, 255);
    set_point(14, 23, 255, 255, 255);
    set_point(14, 24, 255, 255, 255);
    set_point(14, 25, 255, 255, 255);
    set_point(15, 8, 255, 255, 255);
    set_point(15, 9, 255, 255, 255);
    set_point(15, 10, 255, 255, 255);
    set_point(15, 15, 255, 255, 255);
    set_point(15, 16, 255, 255, 255);
    set_point(15, 17, 255, 255, 255);
    set_point(15, 18, 255, 255, 255);
    set_point(15, 23, 255, 255, 255);
    set_point(15, 24, 255, 255, 255);
    set_point(15, 25, 255, 255, 255);
    set_point(16, 8, 255, 255, 255);
    set_point(16, 9, 255, 255, 255);
    set_point(16, 10, 255, 255, 255);
    set_point(16, 15, 255, 255, 255);
    set_point(16, 16, 255, 255, 255);
    set_point(16, 17, 255, 255, 255);
    set_point(16, 18, 255, 255, 255);
    set_point(16, 23, 255, 255, 255);
    set_point(16, 24, 255, 255, 255);
    set_point(16, 25, 255, 255, 255);
    set_point(17, 8, 255, 255, 255);
    set_point(17, 9, 255, 255, 255);
    set_point(17, 10, 255, 255, 255);
    set_point(17, 15, 255, 255, 255);
    set_point(17, 16, 255, 255, 255);
    set_point(17, 17, 255, 255, 255);
    set_point(17, 18, 255, 255, 255);
    set_point(17, 23, 255, 255, 255);
    set_point(17, 24, 255, 255, 255);
    set_point(17, 25, 255, 255, 255);
    set_point(18, 9, 255, 255, 255);
    set_point(18, 10, 255, 255, 255);
    set_point(18, 15, 255, 255, 255);
    set_point(18, 16, 255, 255, 255);
    set_point(18, 17, 255, 255, 255);
    set_point(18, 18, 255, 255, 255);
    set_point(18, 23, 255, 255, 255);
    set_point(18, 24, 255, 255, 255);
    set_point(18, 25, 255, 255, 255);
    set_point(19, 10, 255, 255, 255);
    set_point(19, 13, 255, 255, 255);
    set_point(19, 14, 255, 255, 255);
    set_point(19, 15, 255, 255, 255);
    set_point(19, 16, 255, 255, 255);
    set_point(19, 17, 255, 255, 255);
    set_point(19, 18, 255, 255, 255);
    set_point(19, 19, 255, 255, 255);
    set_point(19, 20, 255, 255, 255);
    set_point(19, 23, 255, 255, 255);
    set_point(19, 24, 255, 255, 255);
    set_point(19, 25, 255, 255, 255);
    set_point(20, 11, 255, 255, 255);
    set_point(20, 12, 255, 255, 255);
    set_point(20, 13, 255, 255, 255);
    set_point(20, 14, 255, 255, 255);
    set_point(20, 15, 255, 255, 255);
    set_point(20, 16, 255, 255, 255);
    set_point(20, 17, 255, 255, 255);
    set_point(20, 18, 255, 255, 255);
    set_point(20, 19, 255, 255, 255);
    set_point(20, 20, 255, 255, 255);
    set_point(20, 21, 255, 255, 255);
    set_point(20, 22, 255, 255, 255);
    set_point(20, 23, 255, 255, 255);
    set_point(20, 24, 255, 255, 255);
    set_point(20, 25, 255, 255, 255);
    set_point(21, 10, 255, 255, 255);
    set_point(21, 11, 255, 255, 255);
    set_point(21, 12, 255, 255, 255);
    set_point(21, 13, 255, 255, 255);
    set_point(21, 14, 255, 255, 255);
    set_point(21, 15, 255, 255, 255);
    set_point(21, 18, 255, 255, 255);
    set_point(21, 19, 255, 255, 255);
    set_point(21, 20, 255, 255, 255);
    set_point(21, 21, 255, 255, 255);
    set_point(21, 22, 255, 255, 255);
    set_point(21, 23, 255, 255, 255);
    set_point(21, 24, 255, 255, 255);
    set_point(21, 25, 255, 255, 255);
    set_point(22, 8, 255, 255, 255);
    set_point(22, 9, 255, 255, 255);
    set_point(22, 10, 255, 255, 255);
    set_point(22, 11, 255, 255, 255);
    set_point(22, 12, 255, 255, 255);
    set_point(22, 13, 255, 255, 255);
    set_point(22, 20, 255, 255, 255);
    set_point(22, 21, 255, 255, 255);
    set_point(22, 22, 255, 255, 255);
    set_point(22, 23, 255, 255, 255);
    set_point(22, 24, 255, 255, 255);
    set_point(23, 9, 255, 255, 255);
    set_point(23, 10, 255, 255, 255);
    set_point(23, 11, 255, 255, 255);
    set_point(23, 22, 255, 255, 255);
    
    // Render to LED matrix (simple row-major layout)
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            int led_index = y * WIDTH + x; // Simple row-major layout
            RGB color = color_correct(grid[y][x][0], grid[y][x][1], grid[y][x][2]);
            led_strip_set_pixel(led_strip, led_index, color.r, color.g, color.b);
        }
    }
    led_strip_refresh(led_strip);
}

// Main task
void app_main(void) {
    matrix_init();
    while (1) {
        update_matrix();
        vTaskDelay(pdMS_TO_TICKS(100)); // 100ms refresh, approx 10FPS
    }
}
```

## 彩色logo

```
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "led_strip.h"

// LED matrix parameters
#define LED_PIN GPIO_NUM_9   // ESP32 control pin
#define WIDTH 32             // Matrix width
#define HEIGHT 32            // Matrix height
#define NUM_LEDS (WIDTH * HEIGHT) // Total LEDs: 1024

// RGB structure
typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} RGB;

// HSL structure
typedef struct {
    float h; // Hue (0-360)
    float s; // Saturation (0-1)
    float l; // Lightness (0-1)
} HSL;

// Color correction function
RGB color_correct(uint8_t input_r, uint8_t input_g, uint8_t input_b) {
    RGB result;
    const RGB black = {0, 0, 0};
    const RGB min_white = {5, 4, 3};
    const RGB max_white = {168, 112, 76};
    const float input_min = 5.0f;
    const float input_max = 255.0f;

    const float r_slope = (float)(max_white.r - min_white.r) / (input_max - input_min);
    const float g_slope = (float)(max_white.g - min_white.g) / (input_max - input_min);
    const float b_slope = (float)(max_white.b - min_white.b) / (input_max - input_min);

    const float r_intercept = min_white.r - r_slope * input_min;
    const float g_intercept = min_white.g - g_slope * input_min;
    const float b_intercept = min_white.b - b_slope * input_min;

    float temp_r, temp_g, temp_b;
    if (input_r <= 5 && input_g <= 5 && input_b <= 5) {
        temp_r = (float)input_r * (min_white.r / input_min);
        temp_g = (float)input_g * (min_white.g / input_min);
        temp_b = (float)input_b * (min_white.b / input_min);
    } else {
        temp_r = (float)input_r * r_slope + r_intercept;
        temp_g = (float)input_g * g_slope + g_intercept;
        temp_b = (float)input_b * b_slope + b_intercept;
    }

    temp_r = (temp_r < black.r) ? black.r : (temp_r > max_white.r) ? max_white.r : temp_r;
    temp_g = (temp_g < black.g) ? black.g : (temp_g > max_white.g) ? max_white.g : temp_g;
    temp_b = (temp_b < black.b) ? black.b : (temp_b > max_white.b) ? max_white.b : temp_b;

    result.r = (uint8_t)(temp_r + 0.5f);
    result.g = (uint8_t)(temp_g + 0.5f);
    result.b = (uint8_t)(temp_b + 0.5f);
    
    return result;
}

// RGB to HSL conversion
HSL rgb_to_hsl(uint8_t r, uint8_t g, uint8_t b) {
    HSL hsl;
    float r_norm = r / 255.0f;
    float g_norm = g / 255.0f;
    float b_norm = b / 255.0f;

    float max = fmaxf(fmaxf(r_norm, g_norm), b_norm);
    float min = fminf(fminf(r_norm, g_norm), b_norm);
    float delta = max - min;

    // Lightness
    hsl.l = (max + min) / 2.0f;

    // Saturation
    if (delta == 0.0f) {
        hsl.s = 0.0f;
        hsl.h = 0.0f; // Undefined, but set to 0
    } else {
        hsl.s = (hsl.l > 0.5f) ? (delta / (2.0f - max - min)) : (delta / (max + min));

        // Hue
        if (max == r_norm) {
            hsl.h = (g_norm - b_norm) / delta + (g_norm < b_norm ? 6.0f : 0.0f);
        } else if (max == g_norm) {
            hsl.h = (b_norm - r_norm) / delta + 2.0f;
        } else {
            hsl.h = (r_norm - g_norm) / delta + 4.0f;
        }
        hsl.h *= 60.0f;
    }

    return hsl;
}

// HSL to RGB conversion
RGB hsl_to_rgb(float h, float s, float l) {
    RGB rgb;
    float c = (1.0f - fabsf(2.0f * l - 1.0f)) * s;
    float x = c * (1.0f - fabsf(fmodf(h / 60.0f, 2.0f) - 1.0f));
    float m = l - c / 2.0f;

    float r, g, b;
    if (h >= 0.0f && h < 60.0f) {
        r = c; g = x; b = 0.0f;
    } else if (h >= 60.0f && h < 120.0f) {
        r = x; g = c; b = 0.0f;
    } else if (h >= 120.0f && h < 180.0f) {
        r = 0.0f; g = c; b = x;
    } else if (h >= 180.0f && h < 240.0f) {
        r = 0.0f; g = x; b = c;
    } else if (h >= 240.0f && h < 300.0f) {
        r = x; g = 0.0f; b = c;
    } else {
        r = c; g = 0.0f; b = x;
    }

    rgb.r = (uint8_t)((r + m) * 255.0f + 0.5f);
    rgb.g = (uint8_t)((g + m) * 255.0f + 0.5f);
    rgb.b = (uint8_t)((b + m) * 255.0f + 0.5f);

    return rgb;
}

// Adjust brightness and saturation
RGB adjust_brightness_saturation(uint8_t r, uint8_t g, uint8_t b) {
    // Step 1: Reduce brightness by 52.4% (0.595 * 0.8)
    float brightness_factor = 0.476f; // Total brightness reduction: 1 - 0.524
    float adjusted_r = r * brightness_factor;
    float adjusted_g = g * brightness_factor;
    float adjusted_b = b * brightness_factor;

    // Clamp to valid range
    adjusted_r = (adjusted_r < 0) ? 0 : (adjusted_r > 255) ? 255 : adjusted_r;
    adjusted_g = (adjusted_g < 0) ? 0 : (adjusted_g > 255) ? 255 : adjusted_g;
    adjusted_b = (adjusted_b < 0) ? 0 : (adjusted_b > 255) ? 255 : adjusted_b;

    // Step 2: Convert to HSL and increase saturation by 52.0875% (1.3225 * 1.15)
    HSL hsl = rgb_to_hsl((uint8_t)adjusted_r, (uint8_t)adjusted_g, (uint8_t)adjusted_b);
    hsl.s *= 1.520875f; // Total saturation increase: 1 + 0.520875
    hsl.s = (hsl.s > 1.0f) ? 1.0f : hsl.s; // Clamp saturation to 1.0

    // Step 3: Convert back to RGB
    return hsl_to_rgb(hsl.h, hsl.s, hsl.l);
}

// Global variables
static led_strip_handle_t led_strip;
static uint8_t grid[HEIGHT][WIDTH][3]; // RGB grid

// Initialize LED and matrix
void matrix_init() {
    led_strip_config_t strip_config = {
        .strip_gpio_num = LED_PIN,
        .max_leds = NUM_LEDS,
    };
    led_strip_rmt_config_t rmt_config = {
        .clk_src = RMT_CLK_SRC_DEFAULT,
        .resolution_hz = 10 * 1000 * 1000, // 10MHz
        .flags.with_dma = false,
    };
    ESP_ERROR_CHECK(led_strip_new_rmt_device(&strip_config, &rmt_config, &led_strip));
    
    led_strip_clear(led_strip);
    memset(grid, 0, sizeof(grid));
}

// Define a function to set a specific point with a color
void set_point(int y, int x, uint8_t r, uint8_t g, uint8_t b) {
    if (y >= 0 && y < HEIGHT && x >= 0 && x < WIDTH) {
        // Adjust brightness and saturation
        RGB adjusted = adjust_brightness_saturation(r, g, b);
        grid[y][x][0] = adjusted.r;
        grid[y][x][1] = adjusted.g;
        grid[y][x][2] = adjusted.b;
    }
}

// Update matrix with specified points
void update_matrix() {
    // Clear grid (set all to dark background)
    memset(grid, 0, sizeof(grid));
    
    // Set all specified points with adjusted colors
    set_point(8, 10, 149, 192, 246);
    set_point(8, 11, 151, 189, 246);
    set_point(8, 12, 159, 172, 246);
    set_point(8, 22, 220, 156, 208);
    set_point(8, 23, 223, 157, 205);
    set_point(8, 24, 232, 160, 199);
    set_point(9, 9, 146, 202, 247);
    set_point(9, 10, 149, 192, 246);
    set_point(9, 11, 153, 184, 246);
    set_point(9, 12, 159, 172, 246);
    set_point(9, 13, 166, 161, 245);
    set_point(9, 20, 204, 150, 220);
    set_point(9, 21, 211, 153, 215);
    set_point(9, 22, 220, 157, 208);
    set_point(9, 23, 228, 159, 201);
    set_point(9, 24, 236, 162, 200);
    set_point(9, 25, 240, 162, 195);
    set_point(10, 8, 145, 210, 247);
    set_point(10, 9, 147, 203, 248);
    set_point(10, 10, 148, 198, 247);
    set_point(10, 11, 154, 184, 246);
    set_point(10, 12, 159, 172, 246);
    set_point(10, 13, 166, 162, 245);
    set_point(10, 14, 172, 154, 243);
    set_point(10, 15, 178, 147, 243);
    set_point(10, 18, 191, 144, 235);
    set_point(10, 19, 196, 148, 229);
    set_point(10, 20, 203, 150, 222);
    set_point(10, 21, 212, 153, 214);
    set_point(10, 22, 219, 156, 208);
    set_point(10, 23, 226, 158, 202);
    set_point(11, 8, 145, 209, 247);
    set_point(11, 9, 146, 203, 247);
    set_point(11, 10, 148, 194, 246);
    set_point(11, 11, 153, 184, 246);
    set_point(11, 12, 159, 172, 245);
    set_point(11, 13, 165, 162, 245);
    set_point(11, 14, 172, 154, 243);
    set_point(11, 15, 179, 147, 243);
    set_point(11, 16, 182, 142, 242);
    set_point(11, 17, 186, 141, 239);
    set_point(11, 18, 191, 144, 235);
    set_point(11, 19, 196, 147, 228);
    set_point(11, 20, 203, 149, 220);
    set_point(11, 21, 212, 153, 215);
    set_point(11, 22, 220, 157, 208);
    set_point(12, 8, 145, 209, 247);
    set_point(12, 9, 146, 202, 247);
    set_point(12, 10, 149, 194, 246);
    set_point(12, 14, 172, 153, 243);
    set_point(12, 15, 178, 147, 242);
    set_point(12, 16, 183, 142, 243);
    set_point(12, 17, 185, 142, 240);
    set_point(12, 18, 191, 144, 234);
    set_point(12, 19, 197, 147, 229);
    set_point(12, 23, 226, 158, 203);
    set_point(13, 8, 146, 211, 247);
    set_point(13, 9, 146, 204, 247);
    set_point(13, 10, 149, 195, 247);
    set_point(13, 15, 178, 148, 242);
    set_point(13, 16, 184, 142, 242);
    set_point(13, 17, 185, 142, 240);
    set_point(13, 18, 190, 144, 235);
    set_point(13, 23, 228, 158, 204);
    set_point(13, 24, 235, 161, 198);
    set_point(14, 8, 145, 209, 247);
    set_point(14, 9, 147, 203, 247);
    set_point(14, 10, 149, 194, 246);
    set_point(14, 15, 178, 147, 243);
    set_point(14, 16, 183, 142, 242);
    set_point(14, 17, 186, 142, 241);
    set_point(14, 18, 190, 144, 235);
    set_point(14, 23, 227, 159, 203);
    set_point(14, 24, 234, 161, 197);
    set_point(14, 25, 241, 163, 195);
    set_point(15, 8, 145, 209, 247);
    set_point(15, 9, 147, 203, 247);
    set_point(15, 10, 149, 194, 246);
    set_point(15, 15, 178, 147, 243);
    set_point(15, 16, 183, 142, 242);
    set_point(15, 17, 186, 142, 241);
    set_point(15, 18, 190, 144, 235);
    set_point(15, 23, 227, 159, 203);
    set_point(15, 24, 234, 161, 197);
    set_point(15, 25, 241, 163, 195);
    set_point(16, 8, 145, 209, 247);
    set_point(16, 9, 147, 203, 247);
    set_point(16, 10, 149, 194, 246);
    set_point(16, 15, 178, 147, 243);
    set_point(16, 16, 183, 142, 242);
    set_point(16, 17, 186, 142, 241);
    set_point(16, 18, 190, 144, 235);
    set_point(16, 23, 227, 159, 203);
    set_point(16, 24, 234, 161, 197);
    set_point(16, 25, 241, 163, 195);
    set_point(17, 8, 145, 209, 247);
    set_point(17, 9, 147, 203, 247);
    set_point(17, 10, 149, 194, 246);
    set_point(17, 15, 178, 147, 243);
    set_point(17, 16, 183, 142, 242);
    set_point(17, 17, 186, 142, 241);
    set_point(17, 18, 190, 144, 235);
    set_point(17, 23, 227, 159, 203);
    set_point(17, 24, 234, 161, 197);
    set_point(17, 25, 241, 163, 195);
    set_point(18, 9, 146, 202, 247);
    set_point(18, 10, 149, 194, 245);
    set_point(18, 15, 178, 147, 242);
    set_point(18, 16, 183, 142, 242);
    set_point(18, 17, 185, 142, 240);
    set_point(18, 18, 191, 144, 235);
    set_point(18, 23, 227, 159, 203);
    set_point(18, 24, 234, 161, 197);
    set_point(18, 25, 241, 163, 195);
    set_point(19, 10, 150, 193, 247);
    set_point(19, 13, 165, 162, 245);
    set_point(19, 14, 172, 154, 243);
    set_point(19, 15, 179, 147, 243);
    set_point(19, 16, 182, 142, 242);
    set_point(19, 17, 186, 141, 239);
    set_point(19, 18, 191, 144, 235);
    set_point(19, 19, 196, 147, 228);
    set_point(19, 20, 203, 149, 220);
    set_point(19, 23, 227, 159, 203);
    set_point(19, 24, 234, 161, 197);
    set_point(19, 25, 241, 163, 195);
    set_point(20, 11, 153, 184, 246);
    set_point(20, 12, 159, 172, 245);
    set_point(20, 13, 165, 162, 245);
    set_point(20, 14, 172, 154, 243);
    set_point(20, 15, 179, 147, 243);
    set_point(20, 16, 182, 142, 242);
    set_point(20, 17, 186, 141, 239);
    set_point(20, 18, 191, 144, 235);
    set_point(20, 19, 196, 147, 228);
    set_point(20, 20, 203, 149, 220);
    set_point(20, 21, 212, 153, 215);
    set_point(20, 22, 220, 157, 208);
    set_point(20, 23, 227, 159, 203);
    set_point(20, 24, 234, 161, 197);
    set_point(20, 25, 241, 163, 195);
    set_point(21, 10, 149, 194, 246);
    set_point(21, 11, 153, 183, 246);
    set_point(21, 12, 158, 172, 245);
    set_point(21, 13, 165, 163, 245);
    set_point(21, 14, 173, 155, 244);
    set_point(21, 15, 178, 147, 242);
    set_point(21, 18, 191, 144, 235);
    set_point(21, 19, 196, 147, 228);
    set_point(21, 20, 203, 149, 220);
    set_point(21, 21, 212, 153, 215);
    set_point(21, 22, 220, 157, 208);
    set_point(21, 23, 227, 159, 203);
    set_point(21, 24, 234, 161, 197);
    set_point(21, 25, 241, 163, 195);
    set_point(22, 8, 145, 209, 247);
    set_point(22, 9, 146, 202, 247);
    set_point(22, 10, 149, 194, 246);
    set_point(22, 11, 153, 183, 246);
    set_point(22, 12, 158, 172, 245);
    set_point(22, 13, 165, 163, 245);
    set_point(22, 20, 203, 149, 220);
    set_point(22, 21, 212, 153, 215);
    set_point(22, 22, 220, 157, 208);
    set_point(22, 23, 227, 159, 203);
    set_point(22, 24, 234, 161, 197);
    set_point(23, 9, 147, 202, 247);
    set_point(23, 10, 149, 193, 245);
    set_point(23, 11, 153, 183, 245);
    set_point(23, 21, 212, 153, 215);
    set_point(23, 22, 218, 156, 209);
    set_point(23, 23, 227, 159, 203);
    
    // Render to LED matrix (simple row-major layout)
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            int led_index = y * WIDTH + x; // Simple row-major layout
            RGB color = color_correct(grid[y][x][0], grid[y][x][1], grid[y][x][2]);
            led_strip_set_pixel(led_strip, led_index, color.r, color.g, color.b);
        }
    }
    led_strip_refresh(led_strip);
}

// Main task
void app_main(void) {
    matrix_init();
    while (1) {
        update_matrix();
        vTaskDelay(pdMS_TO_TICKS(100)); // 100ms refresh, approx 10FPS
    }
}
```

## 闪动

```
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "led_strip.h"

// LED matrix parameters
#define LED_PIN GPIO_NUM_9   // ESP32 control pin
#define WIDTH 32             // Matrix width
#define HEIGHT 32            // Matrix height
#define NUM_LEDS (WIDTH * HEIGHT) // Total LEDs: 1024

// Animation parameters
#define FRAME_DELAY_MS 100         // 100ms per frame (10FPS)
#define NUM_SPARKLES 5             // Number of sparkles per frame

// RGB structure
typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} RGB;

// HSL structure
typedef struct {
    float h; // Hue (0-360)
    float s; // Saturation (0-1)
    float l; // Lightness (0-1)
} HSL;

// Color correction function
RGB color_correct(uint8_t input_r, uint8_t input_g, uint8_t input_b) {
    RGB result;
    const RGB black = {0, 0, 0};
    const RGB min_white = {5, 4, 3};
    const RGB max_white = {168, 112, 76};
    const float input_min = 5.0f;
    const float input_max = 255.0f;

    const float r_slope = (float)(max_white.r - min_white.r) / (input_max - input_min);
    const float g_slope = (float)(max_white.g - min_white.g) / (input_max - input_min);
    const float b_slope = (float)(max_white.b - min_white.b) / (input_max - input_min);

    const float r_intercept = min_white.r - r_slope * input_min;
    const float g_intercept = min_white.g - g_slope * input_min;
    const float b_intercept = min_white.b - b_slope * input_min;

    float temp_r, temp_g, temp_b;
    if (input_r <= 5 && input_g <= 5 && input_b <= 5) {
        temp_r = (float)input_r * (min_white.r / input_min);
        temp_g = (float)input_g * (min_white.g / input_min);
        temp_b = (float)input_b * (min_white.b / input_min);
    } else {
        temp_r = (float)input_r * r_slope + r_intercept;
        temp_g = (float)input_g * g_slope + g_intercept;
        temp_b = (float)input_b * b_slope + b_intercept;
    }

    temp_r = (temp_r < black.r) ? black.r : (temp_r > max_white.r) ? max_white.r : temp_r;
    temp_g = (temp_g < black.g) ? black.g : (temp_g > max_white.g) ? max_white.g : temp_g;
    temp_b = (temp_b < black.b) ? black.b : (temp_b > max_white.b) ? max_white.b : temp_b;

    result.r = (uint8_t)(temp_r + 0.5f);
    result.g = (uint8_t)(temp_g + 0.5f);
    result.b = (uint8_t)(temp_b + 0.5f);
    
    return result;
}

// RGB to HSL conversion
HSL rgb_to_hsl(uint8_t r, uint8_t g, uint8_t b) {
    HSL hsl;
    float r_norm = r / 255.0f;
    float g_norm = g / 255.0f;
    float b_norm = b / 255.0f;

    float max = fmaxf(fmaxf(r_norm, g_norm), b_norm);
    float min = fminf(fminf(r_norm, g_norm), b_norm);
    float delta = max - min;

    // Lightness
    hsl.l = (max + min) / 2.0f;

    // Saturation
    if (delta == 0.0f) {
        hsl.s = 0.0f;
        hsl.h = 0.0f; // Undefined, but set to 0
    } else {
        hsl.s = (hsl.l > 0.5f) ? (delta / (2.0f - max - min)) : (delta / (max + min));

        // Hue
        if (max == r_norm) {
            hsl.h = (g_norm - b_norm) / delta + (g_norm < b_norm ? 6.0f : 0.0f);
        } else if (max == g_norm) {
            hsl.h = (b_norm - r_norm) / delta + 2.0f;
        } else {
            hsl.h = (r_norm - g_norm) / delta + 4.0f;
        }
        hsl.h *= 60.0f;
    }

    return hsl;
}

// HSL to RGB conversion
RGB hsl_to_rgb(float h, float s, float l) {
    RGB rgb;
    float c = (1.0f - fabsf(2.0f * l - 1.0f)) * s;
    float x = c * (1.0f - fabsf(fmodf(h / 60.0f, 2.0f) - 1.0f));
    float m = l - c / 2.0f;

    float r, g, b;
    if (h >= 0.0f && h < 60.0f) {
        r = c; g = x; b = 0.0f;
    } else if (h >= 60.0f && h < 120.0f) {
        r = x; g = c; b = 0.0f;
    } else if (h >= 120.0f && h < 180.0f) {
        r = 0.0f; g = c; b = x;
    } else if (h >= 180.0f && h < 240.0f) {
        r = 0.0f; g = x; b = c;
    } else if (h >= 240.0f && h < 300.0f) {
        r = x; g = 0.0f; b = c;
    } else {
        r = c; g = 0.0f; b = x;
    }

    rgb.r = (uint8_t)((r + m) * 255.0f + 0.5f);
    rgb.g = (uint8_t)((g + m) * 255.0f + 0.5f);
    rgb.b = (uint8_t)((b + m) * 255.0f + 0.5f);

    return rgb;
}

// Adjust brightness and saturation
RGB adjust_brightness_saturation(uint8_t r, uint8_t g, uint8_t b) {
    // Step 1: Reduce brightness by 52.4% (0.595 * 0.8)
    float brightness_factor = 0.476f; // Total brightness reduction: 1 - 0.524
    float adjusted_r = r * brightness_factor;
    float adjusted_g = g * brightness_factor;
    float adjusted_b = b * brightness_factor;

    // Clamp to valid range
    adjusted_r = (adjusted_r < 0) ? 0 : (adjusted_r > 255) ? 255 : adjusted_r;
    adjusted_g = (adjusted_g < 0) ? 0 : (adjusted_g > 255) ? 255 : adjusted_g;
    adjusted_b = (adjusted_b < 0) ? 0 : (adjusted_b > 255) ? 255 : adjusted_b;

    // Step 2: Convert to HSL and increase saturation by 52.0875% (1.3225 * 1.15)
    HSL hsl = rgb_to_hsl((uint8_t)adjusted_r, (uint8_t)adjusted_g, (uint8_t)adjusted_b);
    hsl.s *= 1.520875f; // Total saturation increase: 1 + 0.520875
    hsl.s = (hsl.s > 1.0f) ? 1.0f : hsl.s; // Clamp saturation to 1.0

    // Step 3: Convert back to RGB
    return hsl_to_rgb(hsl.h, hsl.s, hsl.l);
}

// Global variables
static led_strip_handle_t led_strip;
static uint8_t grid[HEIGHT][WIDTH][3]; // RGB grid for rendering
static uint8_t background_grid[HEIGHT][WIDTH][3]; // Background grid for static pattern

// Initialize LED and matrix
void matrix_init() {
    led_strip_config_t strip_config = {
        .strip_gpio_num = LED_PIN,
        .max_leds = NUM_LEDS,
    };
    led_strip_rmt_config_t rmt_config = {
        .clk_src = RMT_CLK_SRC_DEFAULT,
        .resolution_hz = 10 * 1000 * 1000, // 10MHz
        .flags.with_dma = false,
    };
    ESP_ERROR_CHECK(led_strip_new_rmt_device(&strip_config, &rmt_config, &led_strip));
    
    led_strip_clear(led_strip);
    memset(grid, 0, sizeof(grid));
    memset(background_grid, 0, sizeof(background_grid));

    // Seed the random number generator
    srand(time(NULL));
}

// Define a function to set a specific point with a color
void set_point(int y, int x, uint8_t r, uint8_t g, uint8_t b) {
    if (y >= 0 && y < HEIGHT && x >= 0 && x < WIDTH) {
        // Adjust brightness and saturation
        RGB adjusted = adjust_brightness_saturation(r, g, b);
        background_grid[y][x][0] = adjusted.r;
        background_grid[y][x][1] = adjusted.g;
        background_grid[y][x][2] = adjusted.b;
    }
}

// Draw the static pattern into the background grid
void draw_static_pattern() {
    // Clear background grid
    memset(background_grid, 0, sizeof(background_grid));
    
    // Set all specified points with adjusted colors
    set_point(8, 10, 149, 192, 246);
    set_point(8, 11, 151, 189, 246);
    set_point(8, 12, 159, 172, 246);
    set_point(8, 22, 220, 156, 208);
    set_point(8, 23, 223, 157, 205);
    set_point(8, 24, 232, 160, 199);
    set_point(9, 9, 146, 202, 247);
    set_point(9, 10, 149, 192, 246);
    set_point(9, 11, 153, 184, 246);
    set_point(9, 12, 159, 172, 246);
    set_point(9, 13, 166, 161, 245);
    set_point(9, 20, 204, 150, 220);
    set_point(9, 21, 211, 153, 215);
    set_point(9, 22, 220, 157, 208);
    set_point(9, 23, 228, 159, 201);
    set_point(9, 24, 236, 162, 200);
    set_point(9, 25, 240, 162, 195);
    set_point(10, 8, 145, 210, 247);
    set_point(10, 9, 147, 203, 248);
    set_point(10, 10, 148, 198, 247);
    set_point(10, 11, 154, 184, 246);
    set_point(10, 12, 159, 172, 246);
    set_point(10, 13, 166, 162, 245);
    set_point(10, 14, 172, 154, 243);
    set_point(10, 15, 178, 147, 243);
    set_point(10, 18, 191, 144, 235);
    set_point(10, 19, 196, 148, 229);
    set_point(10, 20, 203, 150, 222);
    set_point(10, 21, 212, 153, 214);
    set_point(10, 22, 219, 156, 208);
    set_point(10, 23, 226, 158, 202);
    set_point(11, 8, 145, 209, 247);
    set_point(11, 9, 146, 203, 247);
    set_point(11, 10, 148, 194, 246);
    set_point(11, 11, 153, 184, 246);
    set_point(11, 12, 159, 172, 245);
    set_point(11, 13, 165, 162, 245);
    set_point(11, 14, 172, 154, 243);
    set_point(11, 15, 179, 147, 243);
    set_point(11, 16, 182, 142, 242);
    set_point(11, 17, 186, 141, 239);
    set_point(11, 18, 191, 144, 235);
    set_point(11, 19, 196, 147, 228);
    set_point(11, 20, 203, 149, 220);
    set_point(11, 21, 212, 153, 215);
    set_point(11, 22, 220, 157, 208);
    set_point(12, 8, 145, 209, 247);
    set_point(12, 9, 146, 202, 247);
    set_point(12, 10, 149, 194, 246);
    set_point(12, 14, 172, 153, 243);
    set_point(12, 15, 178, 147, 242);
    set_point(12, 16, 183, 142, 243);
    set_point(12, 17, 185, 142, 240);
    set_point(12, 18, 191, 144, 234);
    set_point(12, 19, 197, 147, 229);
    set_point(12, 23, 226, 158, 203);
    set_point(13, 8, 146, 211, 247);
    set_point(13, 9, 146, 204, 247);
    set_point(13, 10, 149, 195, 247);
    set_point(13, 15, 178, 148, 242);
    set_point(13, 16, 184, 142, 242);
    set_point(13, 17, 185, 142, 240);
    set_point(13, 18, 190, 144, 235);
    set_point(13, 23, 228, 158, 204);
    set_point(13, 24, 235, 161, 198);
    set_point(14, 8, 145, 209, 247);
    set_point(14, 9, 147, 203, 247);
    set_point(14, 10, 149, 194, 246);
    set_point(14, 15, 178, 147, 243);
    set_point(14, 16, 183, 142, 242);
    set_point(14, 17, 186, 142, 241);
    set_point(14, 18, 190, 144, 235);
    set_point(14, 23, 227, 159, 203);
    set_point(14, 24, 234, 161, 197);
    set_point(14, 25, 241, 163, 195);
    set_point(15, 8, 145, 209, 247);
    set_point(15, 9, 147, 203, 247);
    set_point(15, 10, 149, 194, 246);
    set_point(15, 15, 178, 147, 243);
    set_point(15, 16, 183, 142, 242);
    set_point(15, 17, 186, 142, 241);
    set_point(15, 18, 190, 144, 235);
    set_point(15, 23, 227, 159, 203);
    set_point(15, 24, 234, 161, 197);
    set_point(15, 25, 241, 163, 195);
    set_point(16, 8, 145, 209, 247);
    set_point(16, 9, 147, 203, 247);
    set_point(16, 10, 149, 194, 246);
    set_point(16, 15, 178, 147, 243);
    set_point(16, 16, 183, 142, 242);
    set_point(16, 17, 186, 142, 241);
    set_point(16, 18, 190, 144, 235);
    set_point(16, 23, 227, 159, 203);
    set_point(16, 24, 234, 161, 197);
    set_point(16, 25, 241, 163, 195);
    set_point(17, 8, 145, 209, 247);
    set_point(17, 9, 147, 203, 247);
    set_point(17, 10, 149, 194, 246);
    set_point(17, 15, 178, 147, 243);
    set_point(17, 16, 183, 142, 242);
    set_point(17, 17, 186, 142, 241);
    set_point(17, 18, 190, 144, 235);
    set_point(17, 23, 227, 159, 203);
    set_point(17, 24, 234, 161, 197);
    set_point(17, 25, 241, 163, 195);
    set_point(18, 9, 146, 202, 247);
    set_point(18, 10, 149, 194, 245);
    set_point(18, 15, 178, 147, 242);
    set_point(18, 16, 183, 142, 242);
    set_point(18, 17, 185, 142, 240);
    set_point(18, 18, 191, 144, 235);
    set_point(18, 23, 227, 159, 203);
    set_point(18, 24, 234, 161, 197);
    set_point(18, 25, 241, 163, 195);
    set_point(19, 10, 150, 193, 247);
    set_point(19, 13, 165, 162, 245);
    set_point(19, 14, 172, 154, 243);
    set_point(19, 15, 179, 147, 243);
    set_point(19, 16, 182, 142, 242);
    set_point(19, 17, 186, 141, 239);
    set_point(19, 18, 191, 144, 235);
    set_point(19, 19, 196, 147, 228);
    set_point(19, 20, 203, 149, 220);
    set_point(19, 23, 227, 159, 203);
    set_point(19, 24, 234, 161, 197);
    set_point(19, 25, 241, 163, 195);
    set_point(20, 11, 153, 184, 246);
    set_point(20, 12, 159, 172, 245);
    set_point(20, 13, 165, 162, 245);
    set_point(20, 14, 172, 154, 243);
    set_point(20, 15, 179, 147, 243);
    set_point(20, 16, 182, 142, 242);
    set_point(20, 17, 186, 141, 239);
    set_point(20, 18, 191, 144, 235);
    set_point(20, 19, 196, 147, 228);
    set_point(20, 20, 203, 149, 220);
    set_point(20, 21, 212, 153, 215);
    set_point(20, 22, 220, 157, 208);
    set_point(20, 23, 227, 159, 203);
    set_point(20, 24, 234, 161, 197);
    set_point(20, 25, 241, 163, 195);
    set_point(21, 10, 149, 194, 246);
    set_point(21, 11, 153, 183, 246);
    set_point(21, 12, 158, 172, 245);
    set_point(21, 13, 165, 163, 245);
    set_point(21, 14, 173, 155, 244);
    set_point(21, 15, 178, 147, 242);
    set_point(21, 18, 191, 144, 235);
    set_point(21, 19, 196, 147, 228);
    set_point(21, 20, 203, 149, 220);
    set_point(21, 21, 212, 153, 215);
    set_point(21, 22, 220, 157, 208);
    set_point(21, 23, 227, 159, 203);
    set_point(21, 24, 234, 161, 197);
    set_point(21, 25, 241, 163, 195);
    set_point(22, 8, 145, 209, 247);
    set_point(22, 9, 146, 202, 247);
    set_point(22, 10, 149, 194, 246);
    set_point(22, 11, 153, 183, 246);
    set_point(22, 12, 158, 172, 245);
    set_point(22, 13, 165, 163, 245);
    set_point(22, 20, 203, 149, 220);
    set_point(22, 21, 212, 153, 215);
    set_point(22, 22, 220, 157, 208);
    set_point(22, 23, 227, 159, 203);
    set_point(22, 24, 234, 161, 197);
    set_point(23, 9, 147, 202, 247);
    set_point(23, 10, 149, 193, 245);
    set_point(23, 11, 153, 183, 245);
    set_point(23, 21, 212, 153, 215);
    set_point(23, 22, 218, 156, 209);
    set_point(23, 23, 227, 159, 203);
}

// Update matrix with sparkling effect
void update_matrix() {
    // Copy the background grid to the rendering grid
    memcpy(grid, background_grid, sizeof(grid));

    // Randomly select points in the pattern to sparkle
    for (int i = 0; i < NUM_SPARKLES; i++) {
        int x, y;
        int attempts = 0;
        const int max_attempts = 100; // Prevent infinite loop

        // Keep trying to find a non-black pixel
        do {
            x = rand() % WIDTH;
            y = rand() % HEIGHT;
            attempts++;
            if (attempts >= max_attempts) break; // Avoid infinite loop
        } while (background_grid[y][x][0] == 0 && background_grid[y][x][1] == 0 && background_grid[y][x][2] == 0);

        // If a valid pixel is found, set it to white (sparkle)
        if (attempts < max_attempts) {
            grid[y][x][0] = 255; // White sparkle
            grid[y][x][1] = 255;
            grid[y][x][2] = 255;
        }
    }

    // Render to LED matrix (simple row-major layout)
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            int led_index = y * WIDTH + x; // Simple row-major layout
            RGB color = color_correct(grid[y][x][0], grid[y][x][1], grid[y][x][2]);
            led_strip_set_pixel(led_strip, led_index, color.r, color.g, color.b);
        }
    }
    led_strip_refresh(led_strip);
}

// Main task
void app_main(void) {
    matrix_init();
    draw_static_pattern(); // Draw the static pattern once
    while (1) {
        update_matrix();
        vTaskDelay(pdMS_TO_TICKS(FRAME_DELAY_MS)); // 100ms refresh, 10FPS
    }
}
```

## 扫光

```

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "led_strip.h"

// LED matrix parameters
#define LED_PIN GPIO_NUM_9   // ESP32 control pin
#define WIDTH 32             // Matrix width
#define HEIGHT 32            // Matrix height
#define NUM_LEDS (WIDTH * HEIGHT) // Total LEDs: 1024

// Flash animation parameters
#define FLASH_WIDTH 2        // Width of the flash (2 pixels)
#define ANIMATION_SPEED 1    // Speed of the diagonal flash movement

// RGB structure
typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} RGB;

// HSL structure
typedef struct {
    float h; // Hue (0-360)
    float s; // Saturation (0-1)
    float l; // Lightness (0-1)
} HSL;

// Color correction function
RGB color_correct(uint8_t input_r, uint8_t input_g, uint8_t input_b) {
    RGB result;
    const RGB black = {0, 0, 0};
    const RGB min_white = {5, 4, 3};
    const RGB max_white = {168, 112, 76};
    const float input_min = 5.0f;
    const float input_max = 255.0f;

    const float r_slope = (float)(max_white.r - min_white.r) / (input_max - input_min);
    const float g_slope = (float)(max_white.g - min_white.g) / (input_max - input_min);
    const float b_slope = (float)(max_white.b - min_white.b) / (input_max - input_min);

    const float r_intercept = min_white.r - r_slope * input_min;
    const float g_intercept = min_white.g - g_slope * input_min;
    const float b_intercept = min_white.b - b_slope * input_min;

    float temp_r, temp_g, temp_b;
    if (input_r <= 5 && input_g <= 5 && input_b <= 5) {
        temp_r = (float)input_r * (min_white.r / input_min);
        temp_g = (float)input_g * (min_white.g / input_min);
        temp_b = (float)input_b * (min_white.b / input_min);
    } else {
        temp_r = (float)input_r * r_slope + r_intercept;
        temp_g = (float)input_g * g_slope + g_intercept;
        temp_b = (float)input_b * b_slope + b_intercept;
    }

    temp_r = (temp_r < black.r) ? black.r : (temp_r > max_white.r) ? max_white.r : temp_r;
    temp_g = (temp_g < black.g) ? black.g : (temp_g > max_white.g) ? max_white.g : temp_g;
    temp_b = (temp_b < black.b) ? black.b : (temp_b > max_white.b) ? max_white.b : temp_b;

    result.r = (uint8_t)(temp_r + 0.5f);
    result.g = (uint8_t)(temp_g + 0.5f);
    result.b = (uint8_t)(temp_b + 0.5f);
    
    return result;
}

// RGB to HSL conversion
HSL rgb_to_hsl(uint8_t r, uint8_t g, uint8_t b) {
    HSL hsl;
    float r_norm = r / 255.0f;
    float g_norm = g / 255.0f;
    float b_norm = b / 255.0f;

    float max = fmaxf(fmaxf(r_norm, g_norm), b_norm);
    float min = fminf(fminf(r_norm, g_norm), b_norm);
    float delta = max - min;

    // Lightness
    hsl.l = (max + min) / 2.0f;

    // Saturation
    if (delta == 0.0f) {
        hsl.s = 0.0f;
        hsl.h = 0.0f; // Undefined, but set to 0
    } else {
        hsl.s = (hsl.l > 0.5f) ? (delta / (2.0f - max - min)) : (delta / (max + min));

        // Hue
        if (max == r_norm) {
            hsl.h = (g_norm - b_norm) / delta + (g_norm < b_norm ? 6.0f : 0.0f);
        } else if (max == g_norm) {
            hsl.h = (b_norm - r_norm) / delta + 2.0f;
        } else {
            hsl.h = (r_norm - g_norm) / delta + 4.0f;
        }
        hsl.h *= 60.0f;
    }

    return hsl;
}

// HSL to RGB conversion
RGB hsl_to_rgb(float h, float s, float l) {
    RGB rgb;
    float c = (1.0f - fabsf(2.0f * l - 1.0f)) * s;
    float x = c * (1.0f - fabsf(fmodf(h / 60.0f, 2.0f) - 1.0f));
    float m = l - c / 2.0f;

    float r, g, b;
    if (h >= 0.0f && h < 60.0f) {
        r = c; g = x; b = 0.0f;
    } else if (h >= 60.0f && h < 120.0f) {
        r = x; g = c; b = 0.0f;
    } else if (h >= 120.0f && h < 180.0f) {
        r = 0.0f; g = c; b = x;
    } else if (h >= 180.0f && h < 240.0f) {
        r = 0.0f; g = x; b = c;
    } else if (h >= 240.0f && h < 300.0f) {
        r = x; g = 0.0f; b = c;
    } else {
        r = c; g = 0.0f; b = x;
    }

    rgb.r = (uint8_t)((r + m) * 255.0f + 0.5f);
    rgb.g = (uint8_t)((g + m) * 255.0f + 0.5f);
    rgb.b = (uint8_t)((b + m) * 255.0f + 0.5f);

    return rgb;
}

// Adjust brightness and saturation
RGB adjust_brightness_saturation(uint8_t r, uint8_t g, uint8_t b) {
    // Step 1: Reduce brightness by 52.4% (0.595 * 0.8)
    float brightness_factor = 0.476f; // Total brightness reduction: 1 - 0.524
    float adjusted_r = r * brightness_factor;
    float adjusted_g = g * brightness_factor;
    float adjusted_b = b * brightness_factor;

    // Clamp to valid range
    adjusted_r = (adjusted_r < 0) ? 0 : (adjusted_r > 255) ? 255 : adjusted_r;
    adjusted_g = (adjusted_g < 0) ? 0 : (adjusted_g > 255) ? 255 : adjusted_g;
    adjusted_b = (adjusted_b < 0) ? 0 : (adjusted_b > 255) ? 255 : adjusted_b;

    // Step 2: Convert to HSL and increase saturation by 52.0875% (1.3225 * 1.15)
    HSL hsl = rgb_to_hsl((uint8_t)adjusted_r, (uint8_t)adjusted_g, (uint8_t)adjusted_b);
    hsl.s *= 1.520875f; // Total saturation increase: 1 + 0.520875
    hsl.s = (hsl.s > 1.0f) ? 1.0f : hsl.s; // Clamp saturation to 1.0

    // Step 3: Convert back to RGB
    return hsl_to_rgb(hsl.h, hsl.s, hsl.l);
}

// Global variables
static led_strip_handle_t led_strip;
static uint8_t grid[HEIGHT][WIDTH][3]; // RGB grid
static int flash_position = 0; // Initial position of flash (starting at 0,0)
static uint8_t mask[HEIGHT][WIDTH]; // Mask for which pixels should be illuminated
static uint8_t original_colors[HEIGHT][WIDTH][3]; // Original colors for each pixel

// Initialize LED and matrix
void matrix_init() {
    led_strip_config_t strip_config = {
        .strip_gpio_num = LED_PIN,
        .max_leds = NUM_LEDS,
    };
    led_strip_rmt_config_t rmt_config = {
        .clk_src = RMT_CLK_SRC_DEFAULT,
        .resolution_hz = 10 * 1000 * 1000, // 10MHz
        .flags.with_dma = false,
    };
    ESP_ERROR_CHECK(led_strip_new_rmt_device(&strip_config, &rmt_config, &led_strip));
    
    led_strip_clear(led_strip);
    memset(grid, 0, sizeof(grid));
    memset(mask, 0, sizeof(mask));
    memset(original_colors, 0, sizeof(original_colors));
    
    // Initialize mask and original colors with given points
    // Points list with original colors

    // Store only the points in the mask (1 means it's a point)
    mask[8][11] = 1;
    mask[8][22] = 1;
    mask[8][23] = 1;
    mask[8][24] = 1;
    mask[9][9] = 1;
    mask[9][10] = 1;
    mask[9][11] = 1;
    mask[9][12] = 1;
    mask[9][13] = 1;
    mask[9][20] = 1;
    mask[9][21] = 1;
    mask[9][22] = 1;
    mask[9][23] = 1;
    mask[9][24] = 1;
    mask[9][25] = 1;
    mask[10][8] = 1;
    mask[10][9] = 1;
    mask[10][10] = 1;
    mask[10][11] = 1;
    mask[10][12] = 1;
    mask[10][13] = 1;
    mask[10][14] = 1;
    mask[10][15] = 1;
    mask[10][18] = 1;
    mask[10][19] = 1;
    mask[10][20] = 1;
    mask[10][21] = 1;
    mask[10][22] = 1;
    mask[10][23] = 1;
    mask[11][8] = 1;
    mask[11][9] = 1;
    mask[11][10] = 1;
    mask[11][11] = 1;
    mask[11][12] = 1;
    mask[11][13] = 1;
    mask[11][14] = 1;
    mask[11][15] = 1;
    mask[11][16] = 1;
    mask[11][17] = 1;
    mask[11][18] = 1;
    mask[11][19] = 1;
    mask[11][20] = 1;
    mask[11][21] = 1;
    mask[11][22] = 1;
    mask[12][8] = 1;
    mask[12][9] = 1;
    mask[12][10] = 1;
    mask[12][14] = 1;
    mask[12][15] = 1;
    mask[12][16] = 1;
    mask[12][17] = 1;
    mask[12][18] = 1;
    mask[12][19] = 1;
    mask[12][23] = 1;
    mask[13][8] = 1;
    mask[13][9] = 1;
    mask[13][10] = 1;
    mask[13][15] = 1;
    mask[13][16] = 1;
    mask[13][17] = 1;
    mask[13][18] = 1;
    mask[13][23] = 1;
    mask[13][24] = 1;
    mask[14][8] = 1;
    mask[14][9] = 1;
    mask[14][10] = 1;
    mask[14][15] = 1;
    mask[14][16] = 1;
    mask[14][17] = 1;
    mask[14][18] = 1;
    mask[14][23] = 1;
    mask[14][24] = 1;
    mask[14][25] = 1;
    mask[15][8] = 1;
    mask[15][9] = 1;
    mask[15][10] = 1;
    mask[15][15] = 1;
    mask[15][16] = 1;
    mask[15][17] = 1;
    mask[15][18] = 1;
    mask[15][23] = 1;
    mask[15][24] = 1;
    mask[15][25] = 1;
    mask[16][8] = 1;
    mask[16][9] = 1;
    mask[16][10] = 1;
    mask[16][15] = 1;
    mask[16][16] = 1;
    mask[16][17] = 1;
    mask[16][18] = 1;
    mask[16][23] = 1;
    mask[16][24] = 1;
    mask[16][25] = 1;
    mask[17][8] = 1;
    mask[17][9] = 1;
    mask[17][10] = 1;
    mask[17][15] = 1;
    mask[17][16] = 1;
    mask[17][17] = 1;
    mask[17][18] = 1;
    mask[17][23] = 1;
    mask[17][24] = 1;
    mask[17][25] = 1;
    mask[18][9] = 1;
    mask[18][10] = 1;
    mask[18][15] = 1;
    mask[18][16] = 1;
    mask[18][17] = 1;
    mask[18][18] = 1;
    mask[18][23] = 1;
    mask[18][24] = 1;
    mask[18][25] = 1;
    mask[19][10] = 1;
    mask[19][13] = 1;
    mask[19][14] = 1;
    mask[19][15] = 1;
    mask[19][16] = 1;
    mask[19][17] = 1;
    mask[19][18] = 1;
    mask[19][19] = 1;
    mask[19][20] = 1;
    mask[19][23] = 1;
    mask[19][24] = 1;
    mask[19][25] = 1;
    mask[20][11] = 1;
    mask[20][12] = 1;
    mask[20][13] = 1;
    mask[20][14] = 1;
    mask[20][15] = 1;
    mask[20][16] = 1;
    mask[20][17] = 1;
    mask[20][18] = 1;
    mask[20][19] = 1;
    mask[20][20] = 1;
    mask[20][21] = 1;
    mask[20][22] = 1;
    mask[20][23] = 1;
    mask[20][24] = 1;
    mask[20][25] = 1;
    mask[21][10] = 1;
    mask[21][11] = 1;
    mask[21][12] = 1;
    mask[21][13] = 1;
    mask[21][14] = 1;
    mask[21][15] = 1;
    mask[21][18] = 1;
    mask[21][19] = 1;
    mask[21][20] = 1;
    mask[21][21] = 1;
    mask[21][22] = 1;
    mask[21][23] = 1;
    mask[21][24] = 1;
    mask[21][25] = 1;
    mask[22][8] = 1;
    mask[22][9] = 1;
    mask[22][10] = 1;
    mask[22][11] = 1;
    mask[22][12] = 1;
    mask[22][13] = 1;
    mask[22][20] = 1;
    mask[22][21] = 1;
    mask[22][22] = 1;
    mask[22][23] = 1;
    mask[22][24] = 1;
    mask[23][9] = 1;
    mask[23][10] = 1;
    mask[23][11] = 1;
    mask[23][22] = 1;

    // Store original colors for each point
    // Left part (blue gradient)
    original_colors[8][10][0] = 149; original_colors[8][10][1] = 192; original_colors[8][10][2] = 246;
    original_colors[8][11][0] = 151; original_colors[8][11][1] = 189; original_colors[8][11][2] = 246;
    original_colors[8][12][0] = 159; original_colors[8][12][1] = 172; original_colors[8][12][2] = 246;
    original_colors[8][22][0] = 220; original_colors[8][22][1] = 156; original_colors[8][22][2] = 208;
    original_colors[8][23][0] = 223; original_colors[8][23][1] = 157; original_colors[8][23][2] = 205;
    original_colors[8][24][0] = 232; original_colors[8][24][1] = 160; original_colors[8][24][2] = 199;
    original_colors[9][9][0] = 146; original_colors[9][9][1] = 202; original_colors[9][9][2] = 247;
    original_colors[9][10][0] = 149; original_colors[9][10][1] = 192; original_colors[9][10][2] = 246;
    original_colors[9][11][0] = 153; original_colors[9][11][1] = 184; original_colors[9][11][2] = 246;
    original_colors[9][12][0] = 159; original_colors[9][12][1] = 172; original_colors[9][12][2] = 246;
    original_colors[9][13][0] = 166; original_colors[9][13][1] = 161; original_colors[9][13][2] = 245;
    original_colors[9][20][0] = 204; original_colors[9][20][1] = 150; original_colors[9][20][2] = 220;
    original_colors[9][21][0] = 211; original_colors[9][21][1] = 153; original_colors[9][21][2] = 215;
    original_colors[9][22][0] = 220; original_colors[9][22][1] = 157; original_colors[9][22][2] = 208;
    original_colors[9][23][0] = 228; original_colors[9][23][1] = 159; original_colors[9][23][2] = 201;
    original_colors[9][24][0] = 236; original_colors[9][24][1] = 162; original_colors[9][24][2] = 200;
    original_colors[9][25][0] = 240; original_colors[9][25][1] = 162; original_colors[9][25][2] = 195;
    original_colors[10][8][0] = 145; original_colors[10][8][1] = 210; original_colors[10][8][2] = 247;
    original_colors[10][9][0] = 147; original_colors[10][9][1] = 203; original_colors[10][9][2] = 248;
    original_colors[10][10][0] = 148; original_colors[10][10][1] = 198; original_colors[10][10][2] = 247;
    original_colors[10][11][0] = 154; original_colors[10][11][1] = 184; original_colors[10][11][2] = 246;
    original_colors[10][12][0] = 159; original_colors[10][12][1] = 172; original_colors[10][12][2] = 246;
    original_colors[10][13][0] = 166; original_colors[10][13][1] = 162; original_colors[10][13][2] = 245;
    original_colors[10][14][0] = 172; original_colors[10][14][1] = 154; original_colors[10][14][2] = 243;
    original_colors[10][15][0] = 178; original_colors[10][15][1] = 147; original_colors[10][15][2] = 243;
    original_colors[10][18][0] = 191; original_colors[10][18][1] = 144; original_colors[10][18][2] = 235;
    original_colors[10][19][0] = 196; original_colors[10][19][1] = 148; original_colors[10][19][2] = 229;
    original_colors[10][20][0] = 203; original_colors[10][20][1] = 150; original_colors[10][20][2] = 222;
    original_colors[10][21][0] = 212; original_colors[10][21][1] = 153; original_colors[10][21][2] = 214;
    original_colors[10][22][0] = 219; original_colors[10][22][1] = 156; original_colors[10][22][2] = 208;
    original_colors[10][23][0] = 226; original_colors[10][23][1] = 158; original_colors[10][23][2] = 202;
    original_colors[11][8][0] = 145; original_colors[11][8][1] = 209; original_colors[11][8][2] = 247;
    original_colors[11][9][0] = 146; original_colors[11][9][1] = 203; original_colors[11][9][2] = 247;
    original_colors[11][10][0] = 148; original_colors[11][10][1] = 194; original_colors[11][10][2] = 246;
    original_colors[11][11][0] = 153; original_colors[11][11][1] = 184; original_colors[11][11][2] = 246;
    original_colors[11][12][0] = 159; original_colors[11][12][1] = 172; original_colors[11][12][2] = 245;
    original_colors[11][13][0] = 165; original_colors[11][13][1] = 162; original_colors[11][13][2] = 245;
    original_colors[11][14][0] = 172; original_colors[11][14][1] = 154; original_colors[11][14][2] = 243;
    original_colors[11][15][0] = 179; original_colors[11][15][1] = 147; original_colors[11][15][2] = 243;
    original_colors[11][16][0] = 182; original_colors[11][16][1] = 142; original_colors[11][16][2] = 242;
    original_colors[11][17][0] = 186; original_colors[11][17][1] = 141; original_colors[11][17][2] = 239;
    original_colors[11][18][0] = 191; original_colors[11][18][1] = 144; original_colors[11][18][2] = 235;
    original_colors[11][19][0] = 196; original_colors[11][19][1] = 147; original_colors[11][19][2] = 228;
    original_colors[11][20][0] = 203; original_colors[11][20][1] = 149; original_colors[11][20][2] = 220;
    original_colors[11][21][0] = 212; original_colors[11][21][1] = 153; original_colors[11][21][2] = 215;
    original_colors[11][22][0] = 220; original_colors[11][22][1] = 157; original_colors[11][22][2] = 208;
    original_colors[12][8][0] = 145; original_colors[12][8][1] = 209; original_colors[12][8][2] = 247;
    original_colors[12][9][0] = 146; original_colors[12][9][1] = 202; original_colors[12][9][2] = 247;
    original_colors[12][10][0] = 149; original_colors[12][10][1] = 194; original_colors[12][10][2] = 246;
    original_colors[12][14][0] = 172; original_colors[12][14][1] = 153; original_colors[12][14][2] = 243;
    original_colors[12][15][0] = 178; original_colors[12][15][1] = 147; original_colors[12][15][2] = 242;
    original_colors[12][16][0] = 183; original_colors[12][16][1] = 142; original_colors[12][16][2] = 243;
    original_colors[12][17][0] = 185; original_colors[12][17][1] = 142; original_colors[12][17][2] = 240;
    original_colors[12][18][0] = 191; original_colors[12][18][1] = 144; original_colors[12][18][2] = 234;
    original_colors[12][19][0] = 197; original_colors[12][19][1] = 147; original_colors[12][19][2] = 229;
    original_colors[12][23][0] = 226; original_colors[12][23][1] = 158; original_colors[12][23][2] = 203;
    original_colors[13][8][0] = 146; original_colors[13][8][1] = 211; original_colors[13][8][2] = 247;
    original_colors[13][9][0] = 146; original_colors[13][9][1] = 204; original_colors[13][9][2] = 247;
    original_colors[13][10][0] = 149; original_colors[13][10][1] = 195; original_colors[13][10][2] = 247;
    original_colors[13][15][0] = 178; original_colors[13][15][1] = 148; original_colors[13][15][2] = 242;
    original_colors[13][16][0] = 184; original_colors[13][16][1] = 142; original_colors[13][16][2] = 242;
    original_colors[13][17][0] = 185; original_colors[13][17][1] = 142; original_colors[13][17][2] = 240;
    original_colors[13][18][0] = 190; original_colors[13][18][1] = 144; original_colors[13][18][2] = 235;
    original_colors[13][23][0] = 228; original_colors[13][23][1] = 158; original_colors[13][23][2] = 204;
    original_colors[13][24][0] = 235; original_colors[13][24][1] = 161; original_colors[13][24][2] = 198;
    original_colors[14][8][0] = 145; original_colors[14][8][1] = 209; original_colors[14][8][2] = 247;
    original_colors[14][9][0] = 147; original_colors[14][9][1] = 203; original_colors[14][9][2] = 247;
    original_colors[14][10][0] = 149; original_colors[14][10][1] = 194; original_colors[14][10][2] = 246;
    original_colors[14][15][0] = 178; original_colors[14][15][1] = 147; original_colors[14][15][2] = 243;
    original_colors[14][16][0] = 183; original_colors[14][16][1] = 142; original_colors[14][16][2] = 242;
    original_colors[14][17][0] = 186; original_colors[14][17][1] = 142; original_colors[14][17][2] = 241;
    original_colors[14][18][0] = 190; original_colors[14][18][1] = 144; original_colors[14][18][2] = 235;
    original_colors[14][23][0] = 227; original_colors[14][23][1] = 159; original_colors[14][23][2] = 203;
    original_colors[14][24][0] = 234; original_colors[14][24][1] = 161; original_colors[14][24][2] = 197;
    original_colors[14][25][0] = 241; original_colors[14][25][1] = 163; original_colors[14][25][2] = 195;
    original_colors[15][8][0] = 145; original_colors[15][8][1] = 209; original_colors[15][8][2] = 247;
    original_colors[15][9][0] = 147; original_colors[15][9][1] = 203; original_colors[15][9][2] = 247;
    original_colors[15][10][0] = 149; original_colors[15][10][1] = 194; original_colors[15][10][2] = 246;
    original_colors[15][15][0] = 178; original_colors[15][15][1] = 147; original_colors[15][15][2] = 243;
    original_colors[15][16][0] = 183; original_colors[15][16][1] = 142; original_colors[15][16][2] = 242;
    original_colors[15][17][0] = 186; original_colors[15][17][1] = 142; original_colors[15][17][2] = 241;
    original_colors[15][18][0] = 190; original_colors[15][18][1] = 144; original_colors[15][18][2] = 235;
    original_colors[15][23][0] = 227; original_colors[15][23][1] = 159; original_colors[15][23][2] = 203;
    original_colors[15][24][0] = 234; original_colors[15][24][1] = 161; original_colors[15][24][2] = 197;
    original_colors[15][25][0] = 241; original_colors[15][25][1] = 163; original_colors[15][25][2] = 195;
    original_colors[16][8][0] = 145; original_colors[16][8][1] = 209; original_colors[16][8][2] = 247;
    original_colors[16][9][0] = 147; original_colors[16][9][1] = 203; original_colors[16][9][2] = 247;
    original_colors[16][10][0] = 149; original_colors[16][10][1] = 194; original_colors[16][10][2] = 246;
    original_colors[16][15][0] = 178; original_colors[16][15][1] = 147; original_colors[16][15][2] = 243;
    original_colors[16][16][0] = 183; original_colors[16][16][1] = 142; original_colors[16][16][2] = 242;
    original_colors[16][17][0] = 186; original_colors[16][17][1] = 142; original_colors[16][17][2] = 241;
    original_colors[16][18][0] = 190; original_colors[16][18][1] = 144; original_colors[16][18][2] = 235;
    original_colors[16][23][0] = 227; original_colors[16][23][1] = 159; original_colors[16][23][2] = 203;
    original_colors[16][24][0] = 234; original_colors[16][24][1] = 161; original_colors[16][24][2] = 197;
    original_colors[16][25][0] = 241; original_colors[16][25][1] = 163; original_colors[16][25][2] = 195;
    original_colors[17][8][0] = 145; original_colors[17][8][1] = 209; original_colors[17][8][2] = 247;
    original_colors[17][9][0] = 147; original_colors[17][9][1] = 203; original_colors[17][9][2] = 247;
    original_colors[17][10][0] = 149; original_colors[17][10][1] = 194; original_colors[17][10][2] = 246;
    original_colors[17][15][0] = 178; original_colors[17][15][1] = 147; original_colors[17][15][2] = 243;
    original_colors[17][16][0] = 183; original_colors[17][16][1] = 142; original_colors[17][16][2] = 242;
    original_colors[17][17][0] = 186; original_colors[17][17][1] = 142; original_colors[17][17][2] = 241;
    original_colors[17][18][0] = 190; original_colors[17][18][1] = 144; original_colors[17][18][2] = 235;
    original_colors[17][23][0] = 227; original_colors[17][23][1] = 159; original_colors[17][23][2] = 203;
    original_colors[17][24][0] = 234; original_colors[17][24][1] = 161; original_colors[17][24][2] = 197;
    original_colors[17][25][0] = 241; original_colors[17][25][1] = 163; original_colors[17][25][2] = 195;
    original_colors[18][9][0] = 146; original_colors[18][9][1] = 202; original_colors[18][9][2] = 247;
    original_colors[18][10][0] = 149; original_colors[18][10][1] = 194; original_colors[18][10][2] = 245;
    original_colors[18][15][0] = 178; original_colors[18][15][1] = 147; original_colors[18][15][2] = 242;
    original_colors[18][16][0] = 183; original_colors[18][16][1] = 142; original_colors[18][16][2] = 242;
    original_colors[18][17][0] = 185; original_colors[18][17][1] = 142; original_colors[18][17][2] = 240;
    original_colors[18][18][0] = 191; original_colors[18][18][1] = 144; original_colors[18][18][2] = 235;
    original_colors[18][23][0] = 227; original_colors[18][23][1] = 159; original_colors[18][23][2] = 203;
    original_colors[18][24][0] = 234; original_colors[18][24][1] = 161; original_colors[18][24][2] = 197;
    original_colors[18][25][0] = 241; original_colors[18][25][1] = 163; original_colors[18][25][2] = 195;
    original_colors[19][10][0] = 150; original_colors[19][10][1] = 193; original_colors[19][10][2] = 247;
    original_colors[19][13][0] = 165; original_colors[19][13][1] = 162; original_colors[19][13][2] = 245;
    original_colors[19][14][0] = 172; original_colors[19][14][1] = 154; original_colors[19][14][2] = 243;
    original_colors[19][15][0] = 179; original_colors[19][15][1] = 147; original_colors[19][15][2] = 243;
    original_colors[19][16][0] = 182; original_colors[19][16][1] = 142; original_colors[19][16][2] = 242;
    original_colors[19][17][0] = 186; original_colors[19][17][1] = 141; original_colors[19][17][2] = 239;
    original_colors[19][18][0] = 191; original_colors[19][18][1] = 144; original_colors[19][18][2] = 235;
    original_colors[19][19][0] = 196; original_colors[19][19][1] = 147; original_colors[19][19][2] = 228;
    original_colors[19][20][0] = 203; original_colors[19][20][1] = 149; original_colors[19][20][2] = 220;
    original_colors[19][23][0] = 227; original_colors[19][23][1] = 159; original_colors[19][23][2] = 203;
    original_colors[19][24][0] = 234; original_colors[19][24][1] = 161; original_colors[19][24][2] = 197;
    original_colors[19][25][0] = 241; original_colors[19][25][1] = 163; original_colors[19][25][2] = 195;
    original_colors[20][11][0] = 153; original_colors[20][11][1] = 184; original_colors[20][11][2] = 246;
    original_colors[20][12][0] = 159; original_colors[20][12][1] = 172; original_colors[20][12][2] = 245;
    original_colors[20][13][0] = 165; original_colors[20][13][1] = 162; original_colors[20][13][2] = 245;
    original_colors[20][14][0] = 172; original_colors[20][14][1] = 154; original_colors[20][14][2] = 243;
    original_colors[20][15][0] = 179; original_colors[20][15][1] = 147; original_colors[20][15][2] = 243;
    original_colors[20][16][0] = 182; original_colors[20][16][1] = 142; original_colors[20][16][2] = 242;
    original_colors[20][17][0] = 186; original_colors[20][17][1] = 141; original_colors[20][17][2] = 239;
    original_colors[20][18][0] = 191; original_colors[20][18][1] = 144; original_colors[20][18][2] = 235;
    original_colors[20][19][0] = 196; original_colors[20][19][1] = 147; original_colors[20][19][2] = 228;
    original_colors[20][20][0] = 203; original_colors[20][20][1] = 149; original_colors[20][20][2] = 220;
    original_colors[20][21][0] = 212; original_colors[20][21][1] = 153; original_colors[20][21][2] = 215;
    original_colors[20][22][0] = 220; original_colors[20][22][1] = 157; original_colors[20][22][2] = 208;
    original_colors[20][23][0] = 227; original_colors[20][23][1] = 159; original_colors[20][23][2] = 203;
    original_colors[20][24][0] = 234; original_colors[20][24][1] = 161; original_colors[20][24][2] = 197;
    original_colors[20][25][0] = 241; original_colors[20][25][1] = 163; original_colors[20][25][2] = 195;
    original_colors[21][10][0] = 149; original_colors[21][10][1] = 194; original_colors[21][10][2] = 246;
    original_colors[21][11][0] = 153; original_colors[21][11][1] = 183; original_colors[21][11][2] = 246;
    original_colors[21][12][0] = 158; original_colors[21][12][1] = 172; original_colors[21][12][2] = 245;
    original_colors[21][13][0] = 165; original_colors[21][13][1] = 163; original_colors[21][13][2] = 245;
    original_colors[21][14][0] = 173; original_colors[21][14][1] = 155; original_colors[21][14][2] = 244;
    original_colors[21][15][0] = 178; original_colors[21][15][1] = 147; original_colors[21][15][2] = 242;
    original_colors[21][18][0] = 191; original_colors[21][18][1] = 144; original_colors[21][18][2] = 235;
    original_colors[21][19][0] = 196; original_colors[21][19][1] = 147; original_colors[21][19][2] = 228;
    original_colors[21][20][0] = 203; original_colors[21][20][1] = 149; original_colors[21][20][2] = 220;
    original_colors[21][21][0] = 212; original_colors[21][21][1] = 153; original_colors[21][21][2] = 215;
    original_colors[21][22][0] = 220; original_colors[21][22][1] = 157; original_colors[21][22][2] = 208;
    original_colors[21][23][0] = 227; original_colors[21][23][1] = 159; original_colors[21][23][2] = 203;
    original_colors[21][24][0] = 234; original_colors[21][24][1] = 161; original_colors[21][24][2] = 197;
    original_colors[21][25][0] = 241; original_colors[21][25][1] = 163; original_colors[21][25][2] = 195;
    original_colors[22][8][0] = 145; original_colors[22][8][1] = 209; original_colors[22][8][2] = 247;
    original_colors[22][9][0] = 146; original_colors[22][9][1] = 202; original_colors[22][9][2] = 247;
    original_colors[22][10][0] = 149; original_colors[22][10][1] = 194; original_colors[22][10][2] = 246;
    original_colors[22][11][0] = 153; original_colors[22][11][1] = 183; original_colors[22][11][2] = 246;
    original_colors[22][12][0] = 158; original_colors[22][12][1] = 172; original_colors[22][12][2] = 245;
    original_colors[22][13][0] = 165; original_colors[22][13][1] = 163; original_colors[22][13][2] = 245;
    original_colors[22][20][0] = 203; original_colors[22][20][1] = 149; original_colors[22][20][2] = 220;
    original_colors[22][21][0] = 212; original_colors[22][21][1] = 153; original_colors[22][21][2] = 215;
    original_colors[22][22][0] = 220; original_colors[22][22][1] = 157; original_colors[22][22][2] = 208;
    original_colors[22][23][0] = 227; original_colors[22][23][1] = 159; original_colors[22][23][2] = 203;
    original_colors[22][24][0] = 234; original_colors[22][24][1] = 161; original_colors[22][24][2] = 197;
    original_colors[23][9][0] = 147; original_colors[23][9][1] = 202; original_colors[23][9][2] = 247;
    original_colors[23][10][0] = 149; original_colors[23][10][1] = 193; original_colors[23][10][2] = 245;
    original_colors[23][11][0] = 153; original_colors[23][11][1] = 183; original_colors[23][11][2] = 245;
    original_colors[23][21][0] = 212; original_colors[23][21][1] = 153; original_colors[23][21][2] = 215;
    original_colors[23][22][0] = 218; original_colors[23][22][1] = 156; original_colors[23][22][2] = 209;
    original_colors[23][23][0] = 227; original_colors[23][23][1] = 159; original_colors[23][23][2] = 203;
}

// Calculate the brightness based on the distance from the flash center line
float calculate_flash_brightness(int y, int x, int flash_pos) {
    // Distance from pixel to the diagonal flash line
    // The diagonal flash line is represented by the equation: y = x - flash_pos
    // Distance from point (x,y) to line y = x - flash_pos is:
    // |y - x + flash_pos| / sqrt(2)
    float distance = fabsf((float)y - (float)x + (float)flash_pos) / 1.414f;
    
    // Calculate brightness - full brightness at the center, fading to edges
    if (distance < FLASH_WIDTH) {
        // Cosine brightness falloff for a more natural light effect
        return cosf(distance * 3.14159f / (2.0f * FLASH_WIDTH));
    }
    
    return 0.0f; // No brightness outside flash width
}

// Update matrix with diagonal flash animation
void update_matrix() {
    // Clear grid (set all to dark background)
    memset(grid, 0, sizeof(grid));
    
    // Apply original colors to points at reduced brightness
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            if (mask[y][x]) {
                // Apply original colors
                RGB adjusted = adjust_brightness_saturation(
                    original_colors[y][x][0], 
                    original_colors[y][x][1], 
                    original_colors[y][x][2]
                );
                grid[y][x][0] = adjusted.r;
                grid[y][x][1] = adjusted.g;
                grid[y][x][2] = adjusted.b;
            }
        }
    }
    
    // Update flash position
    flash_position += ANIMATION_SPEED;
    
    // Reset flash position when it exits the screen
    if (flash_position > WIDTH + HEIGHT + FLASH_WIDTH) {
        flash_position = 0; // Start from (0,0)
    }
    
    // Apply flash effect to all pixels in the mask
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            if (mask[y][x]) {
                // Calculate brightness based on distance from the flash line
                float brightness = calculate_flash_brightness(y, x, flash_position);
                
                if (brightness > 0.0f) {
                    // Brighten the original color
                    float brighten_factor = 1.0f + brightness * 1.5f; // Max 2.5x brightness
                    
                    // Get original adjusted color
                    RGB adjusted = adjust_brightness_saturation(
                        original_colors[y][x][0], 
                        original_colors[y][x][1], 
                        original_colors[y][x][2]
                    );
                    
                    // Increase brightness
                    uint16_t r = (uint16_t)(adjusted.r * brighten_factor);
                    uint16_t g = (uint16_t)(adjusted.g * brighten_factor);
                    uint16_t b = (uint16_t)(adjusted.b * brighten_factor);
                    
                    // Clamp to valid range
                    grid[y][x][0] = (r > 255) ? 255 : (uint8_t)r;
                    grid[y][x][1] = (g > 255) ? 255 : (uint8_t)g;
                    grid[y][x][2] = (b > 255) ? 255 : (uint8_t)b;
                }
            }
        }
    }
    
    // Render to LED matrix (simple row-major layout)
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            int led_index = y * WIDTH + x; // Simple row-major layout
            RGB color = color_correct(grid[y][x][0], grid[y][x][1], grid[y][x][2]);
            led_strip_set_pixel(led_strip, led_index, color.r, color.g, color.b);
        }
    }
    led_strip_refresh(led_strip);
}

// Main task
void app_main(void) {
    matrix_init();
    while (1) {
        update_matrix();
        vTaskDelay(pdMS_TO_TICKS(30)); // 30ms refresh, approx 33FPS
    }
}
```