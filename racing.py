import numpy as np
import time
import pygame
pygame.init()

size = 800

full_size = 1600

t = 0

scale = 7.022648501

t_scale = 64 * ( 100 / 102 ) * ( 600 / 602 )

step_delay_scale = 1.5655

# ======================================================================================================================
# set damage model intensity: ('extreme', 'simulation', 'standard', 'reduced', 'none')
damage_model = 'simulation'
# Choose car
# (P1: 'SF90', 'W11')
p1_car = 'W11'
# (P2: 'SF90', 'police', 'W11')
p2_car = 'W11'
# police color: blue (37, 0, 224), white (246, 248, 247)
# p2_color = (246, 248, 247)
p2_siren_blue = (74, 83, 225)
p2_siren_red = (255, 97, 112)
# W11 colors: (17, 17, 17), (198, 198, 198), Ferrari red (166, 5, 26)

# set P1 and P2 car colors
p1_color = (198, 198, 198)
p2_color = (17, 17, 17)


# set tyre color
tyre_color = (22, 22, 22)

# set river color
river_color = (134, 180, 188)
# set P1 and P2 colors in river
p1_color_in_river = (p1_color[0] * 0.3 + river_color[0] * 0.7,
                     p1_color[1] * 0.3 + river_color[1] * 0.7,
                     p1_color[2] * 0.3 + river_color[2] * 0.7)

p2_color_in_river = (p2_color[0] * 0.3 + river_color[0] * 0.7,
                     p2_color[1] * 0.3 + river_color[1] * 0.7,
                     p2_color[2] * 0.3 + river_color[2] * 0.7)

tyre_color_in_river = (tyre_color[0] * 0.3 + river_color[0] * 0.7,
                       tyre_color[1] * 0.3 + river_color[1] * 0.7,
                       tyre_color[2] * 0.3 + river_color[2] * 0.7)

# set auto_throttle: ('on', 'off')
p1_auto_throttle = 'on'
p2_auto_throttle = 'on'

# set slipstream strength (float: 0 - 1)
slipstream_strength = 0.5

# set river existence
river_exist = True
# ======================================================================================================================

tree_width = 15
tree_height = 15

# divider_width = 0.6369
divider_width = 1
divider_height = 12.739

side_width = 110
lane_width = 15.924 + divider_width
divider_sep = 31.8471
divider_sep += 0.1

pole_width = 60
pole_height = 5

tree_sep = 50

win = pygame.display.set_mode((full_size, size))

win_color = (80, 80, 80)

win.fill(win_color)
pygame.display.flip()

pygame.display.set_caption("Highway Simulator")

if p1_car == 'SF90':
    # P1 car
    x = 0.32620 * size
    # P1 view
    y = 0.5 * size
    # P2 view
    yy = 0.5 * size

    width = 8.37
    height = 20
    x_vel = 0
    y_vel = -10 / scale
    x_acc_max = 0.01
    y_acc_max = 0.111 / scale
    x_fri = 0.005
    y_fri = 0.001 / scale
    x_air = 0.0001
    y_air_s = 0.000094 * scale
    # braking
    y_dcc = 0.58 * y_acc_max
    # cruise control
    cruise_control = False
    cruise_control_hold = False
    # n2o
    y_acc_n2o = 0.05 / scale
    n2o_quantity = 8 * t_scale
    full_n2o_quantity = n2o_quantity
    # turbo
    y_acc_turbo = 0.08 / scale
    turbo_boost = False
    turbo_boost_option = True
    turbo_boost_duration = 5 * t_scale
    turbo_recharge_duration = 20 * t_scale
    turbo_reboot_t = 0 * t_scale
    # gear
    gear = 1
    # life
    life = 100
    damage_c = 10
    # display or not
    show = True
    # battery deployment mode
    mode = 'n'
    # battery
    battery = 100
    full_battery = 100

elif p1_car == 'W11':
    # P1 car
    x = 0.32620 * size
    # P1 view
    y = 0.5 * size
    # P2 view
    yy = 0.5 * size

    width = 8.37
    height = 20
    x_vel = 0
    y_vel = -10 / scale
    x_acc_max = 0.04
    y_acc_max = 0.150 / scale
    x_fri = 0.0045
    y_fri = 0.001 / scale
    x_air = 0.0003
    y_air_s = 0.00008 * scale
    y_air_s_drs = 0.000055 * scale
    y_air_s_no_drs = 0.00008 * scale
    # braking
    y_dcc = 0.6 * y_acc_max
    # cruise control
    cruise_control = False
    cruise_control_hold = False
    # n2o
    y_acc_n2o = 0.075 / scale
    n2o_quantity = 25 * t_scale
    full_n2o_quantity = n2o_quantity
    # turbo
    y_acc_turbo = 0.12 / scale
    turbo_boost = False
    turbo_boost_option = True
    turbo_boost_duration = 15 * t_scale
    turbo_recharge_duration = 10 * t_scale
    turbo_reboot_t = 0 * t_scale
    # gear
    gear = 1
    # life
    life = 100
    damage_c = 12
    # display or not
    show = True
    # battery deployment mode
    mode = 'n'
    # battery
    battery = 100
    full_battery = 100
    # DRS
    drs_open = False
    button_hold = False



# P2 car
if p2_car == 'SF90':
    x_ = x + lane_width
    # P1 view
    y_ = 0.5 * size
    # P2 view
    yy_ = 0.5 * size

    width_ = 8.37
    height_ = 20
    x_vel_ = 0
    y_vel_ = -10 / scale
    x_acc_max_ = 0.01
    y_acc_max_ = 0.111 / scale
    x_fri_ = 0.005
    y_fri_ = 0.001 / scale
    x_air_ = 0.0001
    y_air_s_ = 0.000094 * scale
    # braking
    y_dcc_ = 0.58 * y_acc_max_
    # cruise control
    cruise_control_ = False
    cruise_control_hold_ = False
    # n2o
    y_acc_n2o_ = 0.05 / scale
    n2o_quantity_ = 8 * t_scale
    full_n2o_quantity_ = n2o_quantity_
    # turbo
    y_acc_turbo_ = 0.08 / scale
    turbo_boost_ = False
    turbo_boost_option_ = True
    turbo_boost_duration_ = 5 * t_scale
    turbo_recharge_duration_ = 20 * t_scale
    turbo_reboot_t_ = 0 * t_scale
    # gear
    gear_ = 1
    # life
    life_ = 100
    damage_c_ = 10
    # display or not
    show_ = True
    # battery deployment mode
    mode_ = 'n'
    # battery
    battery_ = 100
    full_battery_ = 100

elif p2_car == 'police':
    x_ = x + lane_width
    # P1 view
    y_ = 0.5 * size
    # P2 view
    yy_ = 0.5 * size

    width_ = 8.37
    height_ = 20
    x_vel_ = 0
    y_vel_ = -10 / scale
    x_acc_max_ = 0.01
    y_acc_max_ = 0.116 / scale
    x_fri_ = 0.005
    y_fri_ = 0.001 / scale
    x_air_ = 0.0001
    y_air_s_ = 0.000094 * scale
    # braking
    y_dcc_ = 0.55 * y_acc_max_
    # cruise control
    cruise_control_ = False
    cruise_control_hold_ = False
    # n2o
    y_acc_n2o_ = 0.05 / scale
    n2o_quantity_ = 10 * t_scale
    full_n2o_quantity_ = n2o_quantity_
    # turbo
    y_acc_turbo_ = 0.08 / scale
    turbo_boost_ = False
    turbo_boost_option_ = True
    turbo_boost_duration_ = 8 * t_scale
    turbo_recharge_duration_ = 18 * t_scale
    turbo_reboot_t_ = 0 * t_scale
    # gear
    gear_ = 1
    # life
    life_ = 100
    damage_c_ = 8
    # display or not
    show_ = True
    # battery deployment mode
    mode_ = 'n'
    # battery
    battery_ = 100
    full_battery_ = 100

elif p2_car == 'W11':
    x_ = x + lane_width
    # P1 view
    y_ = 0.5 * size
    # P2 view
    yy_ = 0.5 * size

    width_ = 8.37
    height_ = 20
    x_vel_ = 0
    y_vel_ = -10 / scale
    x_acc_max_ = 0.04
    y_acc_max_ = 0.150 / scale
    x_fri_ = 0.0045
    y_fri_ = 0.001 / scale
    x_air_ = 0.0003
    y_air_s_ = 0.00008 * scale
    y_air_s_drs_ = 0.000055 * scale
    y_air_s_no_drs_ = 0.00008 * scale
    # braking
    y_dcc_ = 0.6 * y_acc_max_
    # cruise control
    cruise_control_ = False
    cruise_control_hold_ = False
    # n2o
    y_acc_n2o_ = 0.075 / scale
    n2o_quantity_ = 25 * t_scale
    full_n2o_quantity_ = n2o_quantity_
    # turbo
    y_acc_turbo_ = 0.12 / scale
    turbo_boost_ = False
    turbo_boost_option_ = True
    turbo_boost_duration_ = 15 * t_scale
    turbo_recharge_duration_ = 10 * t_scale
    turbo_reboot_t_ = 0 * t_scale
    # gear
    gear_ = 1
    # life
    life_ = 100
    damage_c_ = 12
    # display or not
    show_ = True
    # battery deployment mode
    mode_ = 'n'
    # battery
    battery_ = 100
    full_battery_ = 100
    # DRS
    drs_open_ = False
    button_hold_ = False


# damage model intensity
if damage_model == 'extreme':
    damage_c = 20 * damage_c
    damage_c_ = 20 * damage_c_
elif damage_model == 'simulation':
    damage_c = 10 * damage_c
    damage_c_ = 10 * damage_c_
elif damage_model == 'standard':
    damage_c = 6 * damage_c
    damage_c_ = 6 * damage_c_
elif damage_model == 'reduced':
    damage_c = 3 * damage_c
    damage_c_ = 3 * damage_c_
elif damage_model == 'none':
    damage_c = 0 * damage_c
    damage_c_ = 0 * damage_c_



# P1
# initial distance
distance = 0

# P2
# initial distance
distance_ = 0


# tree locations by the side of the road
x_1 = 10
# P1 view
y_1 = 10

y_2 = y_1 + tree_sep
y_3 = y_2 + tree_sep
y_4 = y_3 + tree_sep
y_5 = y_4 + tree_sep
y_6 = y_5 + tree_sep
y_7 = y_6 + tree_sep
y_8 = y_7 + tree_sep
y_9 = y_8 + tree_sep
y_10 = y_9 + tree_sep
y_11 = y_10 + tree_sep
y_12 = y_11 + tree_sep
y_13 = y_12 + tree_sep
y_14 = y_13 + tree_sep
y_15 = y_14 + tree_sep
y_16 = y_15 + tree_sep

tree_y_array = np.array([y_1, y_2, y_3, y_4, y_5, y_6, y_7, y_8, y_9, y_10, y_11, y_12, y_13, y_14, y_15, y_16])

# P2 view
y_1_ = 10

y_2_ = y_1_ + tree_sep
y_3_ = y_2_ + tree_sep
y_4_ = y_3_ + tree_sep
y_5_ = y_4_ + tree_sep
y_6_ = y_5_ + tree_sep
y_7_ = y_6_ + tree_sep
y_8_ = y_7_ + tree_sep
y_9_ = y_8_ + tree_sep
y_10_ = y_9_ + tree_sep
y_11_ = y_10_ + tree_sep
y_12_ = y_11_ + tree_sep
y_13_ = y_12_ + tree_sep
y_14_ = y_13_ + tree_sep
y_15_ = y_14_ + tree_sep
y_16_ = y_15_ + tree_sep

tree_y_array_ = np.array([y_1_, y_2_, y_3_, y_4_, y_5_, y_6_, y_7_, y_8_, y_9_, y_10_, y_11_, y_12_, y_13_, y_14_, y_15_, y_16_])

# lane divider locations
x_100 = x_1 + side_width + lane_width

# P1 view
y_101 = y_1

y_102 = y_101 + 1 * divider_sep
y_103 = y_101 + 2 * divider_sep
y_104 = y_101 + 3 * divider_sep
y_105 = y_101 + 4 * divider_sep
y_106 = y_101 + 5 * divider_sep
y_107 = y_101 + 6 * divider_sep
y_108 = y_101 + 7 * divider_sep
y_109 = y_101 + 8 * divider_sep
y_110 = y_101 + 9 * divider_sep
y_111 = y_101 + 10 * divider_sep
y_112 = y_101 + 11 * divider_sep
y_113 = y_101 + 12 * divider_sep
y_114 = y_101 + 13 * divider_sep
y_115 = y_101 + 14 * divider_sep
y_116 = y_101 + 15 * divider_sep
y_117 = y_101 + 16 * divider_sep
y_118 = y_101 + 17 * divider_sep
y_119 = y_101 + 18 * divider_sep
y_120 = y_101 + 19 * divider_sep
y_121 = y_101 + 20 * divider_sep
y_122 = y_101 + 21 * divider_sep
y_123 = y_101 + 22 * divider_sep
y_124 = y_101 + 23 * divider_sep
y_125 = y_101 + 24 * divider_sep

divider_y_array = np.array([y_101, y_102, y_103, y_104, y_105, y_106, y_107, y_108, y_109, y_110, y_111, y_112, y_113,
                            y_114, y_115, y_116, y_117, y_118, y_119, y_120, y_121, y_122, y_123, y_124, y_125])

# P2 view
y_101_ = y_1_

y_102_ = y_101_ + 1 * divider_sep
y_103_ = y_101_ + 2 * divider_sep
y_104_ = y_101_ + 3 * divider_sep
y_105_ = y_101_ + 4 * divider_sep
y_106_ = y_101_ + 5 * divider_sep
y_107_ = y_101_ + 6 * divider_sep
y_108_ = y_101_ + 7 * divider_sep
y_109_ = y_101_ + 8 * divider_sep
y_110_ = y_101_ + 9 * divider_sep
y_111_ = y_101_ + 10 * divider_sep
y_112_ = y_101_ + 11 * divider_sep
y_113_ = y_101_ + 12 * divider_sep
y_114_ = y_101_ + 13 * divider_sep
y_115_ = y_101_ + 14 * divider_sep
y_116_ = y_101_ + 15 * divider_sep
y_117_ = y_101_ + 16 * divider_sep
y_118_ = y_101_ + 17 * divider_sep
y_119_ = y_101_ + 18 * divider_sep
y_120_ = y_101_ + 19 * divider_sep
y_121_ = y_101_ + 20 * divider_sep
y_122_ = y_101_ + 21 * divider_sep
y_123_ = y_101_ + 22 * divider_sep
y_124_ = y_101_ + 23 * divider_sep
y_125_ = y_101_ + 24 * divider_sep

divider_y_array_ = np.array([y_101_, y_102_, y_103_, y_104_, y_105_, y_106_, y_107_, y_108_, y_109_, y_110_, y_111_, y_112_, y_113_,
                            y_114_, y_115_, y_116_, y_117_, y_118_, y_119_, y_120_, y_121_, y_122_, y_123_, y_124_, y_125_])

x_200 = x_100 + 1 * lane_width
x_300 = x_100 + 2 * lane_width
x_400 = x_100 + 3 * lane_width
x_500 = x_100 + 4 * lane_width
x_600 = x_100 + 5 * lane_width
x_700 = x_100 + 6 * lane_width
x_800 = x_100 + 7 * lane_width
x_900 = x_100 + 8 * lane_width

# light pole location
x_2 = 50

# AI cars location
x_a = 0.25 * size
# P1 view
y_a = 0.8 * size
# P2 view
y_a_ = 0.8 * size

x_b = 0.20 * size
# P1 view
y_b = 0.7 * size
# P2 view
y_b_ = 0.7 * size

# AI car velocity
a_vel = 11 / scale
b_vel = 25 / scale

# ======================================================================================================================
# river edge x location (danger line for cars)

danger_x = size - divider_width - x_900

# ======================================================================================================================
# create loading time (artificial) (best at 10)
time.sleep(0)
# ======================================================================================================================

# running program
run = True
while run:

    # no time delay
    # pygame.time.delay(round(10 / step_delay_scale))
    # pygame.time.delay(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # # create infinite fast W11
    # if p2_car == 'W11':
    #     y_acc_n2o_ = y_acc_n2o_ * 1.001
    #     y_acc_turbo_ = y_acc_turbo_ * 1.001


    # determine lateral acceleration
    x_acc = (- y_vel / (30 / scale) ) * x_acc_max
    x_acc_ = (- y_vel_ / (30 / scale) ) * x_acc_max_

    # determine slipstream
    if np.abs(distance - distance_) < size / 2:
        # P1 in front of P2
        if np.abs(x_ - x) < width + width * np.abs((y_ - y) / (10 * height)) and y_ > y + height:
            y_air = y_air_s
            y_air_ = (slipstream_strength * ((y_ - y)/(size / 2)) + (1 - slipstream_strength)) * y_air_s_
        # P2 in front of P1
        elif np.abs(x_ - x) < width + width * np.abs((y_ - y) / (10 * height)) and y_ + height < y:
            y_air = (slipstream_strength * ((y - y_)/(size / 2)) + (1 - slipstream_strength)) * y_air_s
            y_air_ = y_air_s_
        else:
            y_air = y_air_s
            y_air_ = y_air_s_
    else:
        y_air = y_air_s
        y_air_ = y_air_s_

    # determine the value of y_acc depending y_vel
    # P1 Ferrari SF 90
    # gear 1
    if y_vel <= 0 / scale and y_vel >= -7 / scale:
        y_acc = 0.85 * y_acc_max
        gear = 1
    # gear 1 to gear 2
    elif y_vel < -7 / scale and y_vel >= -7.1 / scale:
        y_acc = 0.095 * y_acc_max
        gear = 1
    # gear 2
    elif y_vel < -7.1 / scale and y_vel >= -11 / scale:
        y_acc = 0.55 * y_acc_max
        gear = 2
    # gear 2 to gear 3
    elif y_vel < -11 / scale and y_vel >= -11.1 / scale:
        y_acc = 0.165 * y_acc_max
        gear = 2
    # gear 3
    elif y_vel < -11.1 / scale and y_vel >= -15 / scale:
        y_acc = 0.55 * y_acc_max
        gear = 3
    # gear 3 to gear 4
    elif y_vel < -15 / scale and y_vel >= -15.1 / scale:
        y_acc = 0.235 * y_acc_max
        gear = 3
    # gear 4
    elif y_vel < -15.1 / scale and y_vel >= -19 / scale:
        y_acc = 0.5 * y_acc_max
        gear = 4
    # gear 4 to gear 5
    elif y_vel < -19 / scale and y_vel >= -19.1 / scale:
        y_acc = 0.365 * y_acc_max
        gear = 4
    # gear 5
    elif y_vel < -19.1 / scale and y_vel >= -23 / scale:
        y_acc = 0.62 * y_acc_max
        gear = 5
    # gear 5 to gear 6
    elif y_vel < -23 / scale and y_vel >= -23.1 / scale:
        y_acc = 0.505 * y_acc_max
        gear = 5
    # gear 6
    elif y_vel < -23.1 / scale and y_vel >= -27 / scale:
        y_acc = 0.77 * y_acc_max
        gear = 6
    # gear 6 to gear 7
    elif y_vel < -27 / scale and y_vel >= -27.1 / scale:
        y_acc = 0.685 * y_acc_max
        gear = 6
    # gear 7
    elif y_vel < -27.1 / scale and y_vel >= -31 / scale:
        y_acc = 0.9 * y_acc_max
        gear = 7
    # gear 7 to gear 8
    elif y_vel < -31 / scale and y_vel >= -31.1 / scale:
        y_acc = 0.88 * y_acc_max
        gear = 7
    # gear 8
    elif y_vel < -31.1 / scale:
        y_acc = 1 * y_acc_max
        gear = 8

    # determine the value of y_acc_ depending y_vel_
    # P2 Ferrari SF 90
    # gear 1
    if y_vel_ <= 0 / scale and y_vel_ >= -7 / scale:
        y_acc_ = 0.85 * y_acc_max_
        gear_ = 1
    # gear 1 to gear 2
    elif y_vel_ < -7 / scale and y_vel_ >= -7.1 / scale:
        y_acc_ = 0.095 * y_acc_max_
        gear_ = 1
    # gear 2
    elif y_vel_ < -7.1 / scale and y_vel_ >= -11 / scale:
        y_acc_ = 0.55 * y_acc_max_
        gear_ = 2
    # gear 2 to gear 3
    elif y_vel_ < -11 / scale and y_vel_ >= -11.1 / scale:
        y_acc_ = 0.165 * y_acc_max_
        gear_ = 2
    # gear 3
    elif y_vel_ < -11.1 / scale and y_vel_ >= -15 / scale:
        y_acc_ = 0.55 * y_acc_max_
        gear_ = 3
    # gear 3 to gear 4
    elif y_vel_ < -15 / scale and y_vel_ >= -15.1 / scale:
        y_acc_ = 0.235 * y_acc_max_
        gear_ = 3
    # gear 4
    elif y_vel_ < -15.1 / scale and y_vel_ >= -19 / scale:
        y_acc_ = 0.5 * y_acc_max_
        gear_ = 4
    # gear 4 to gear 5
    elif y_vel_ < -19 / scale and y_vel_ >= -19.1 / scale:
        y_acc_ = 0.365 * y_acc_max_
        gear_ = 4
    # gear 5
    elif y_vel_ < -19.1 / scale and y_vel_ >= -23 / scale:
        y_acc_ = 0.62 * y_acc_max_
        gear_ = 5
    # gear 5 to gear 6
    elif y_vel_ < -23 / scale and y_vel_ >= -23.1 / scale:
        y_acc_ = 0.505 * y_acc_max_
        gear_ = 5
    # gear 6
    elif y_vel_ < -23.1 / scale and y_vel_ >= -27 / scale:
        y_acc_ = 0.77 * y_acc_max_
        gear_ = 6
    # gear 6 to gear 7
    elif y_vel_ < -27 / scale and y_vel_ >= -27.1 / scale:
        y_acc_ = 0.685 * y_acc_max_
        gear_ = 6
    # gear 7
    elif y_vel_ < -27.1 / scale and y_vel_ >= -31 / scale:
        y_acc_ = 0.9 * y_acc_max_
        gear_ = 7
    # gear 7 to gear 8
    elif y_vel_ < -31 / scale and y_vel_ >= -31.1 / scale:
        y_acc_ = 0.88 * y_acc_max_
        gear_ = 7
    # gear 8
    elif y_vel_ < -31.1 / scale:
        y_acc_ = 1 * y_acc_max_
        gear_ = 8


    keys = pygame.key.get_pressed()

    # P1
    # battery deployment mode
    if keys[pygame.K_3]:
        mode = 'n'
    if keys[pygame.K_4]:
        mode = 'l'
    if keys[pygame.K_5]:
        mode = 'm'
    if keys[pygame.K_6]:
        mode = 'h'

    if not keys[pygame.K_s]:
        if mode == 'n':
            battery += 0.03 * np.abs(y_vel)
            if battery > 0 and (keys[pygame.K_w] or p1_auto_throttle == 'on'):
                y_acc += 0 * y_acc_max
                battery -= 0
            elif not (keys[pygame.K_w] or p1_auto_throttle == 'on'):
                battery += 0.01 * np.abs(y_vel)
        elif mode == 'l':
            battery += 0.02 * np.abs(y_vel)
            if battery > 0 and (keys[pygame.K_w] or p1_auto_throttle == 'on'):
                y_acc += 0.1 * y_acc_max
                battery -= 0.1
            elif not (keys[pygame.K_w] or p1_auto_throttle == 'on'):
                battery += 0.02 * np.abs(y_vel)
        elif mode == 'm':
            battery += 0.01 * np.abs(y_vel)
            if battery > 0 and (keys[pygame.K_w] or p1_auto_throttle == 'on'):
                y_acc += 0.2 * y_acc_max
                battery -= 0.2
            elif not (keys[pygame.K_w] or p1_auto_throttle == 'on'):
                battery += 0.03 * np.abs(y_vel)
        elif mode == 'h':
            battery += 0 * np.abs(y_vel)
            if battery > 0 and (keys[pygame.K_w] or p1_auto_throttle == 'on'):
                y_acc += 0.3 * y_acc_max
                battery -= 0.3
            elif battery == 0 and (keys[pygame.K_w] or p1_auto_throttle == 'on'):
                mode = 'm'
            elif not (keys[pygame.K_w] or p1_auto_throttle == 'on'):
                battery += 0.04 * np.abs(y_vel)
    elif keys[pygame.K_s] and y_vel < 0:
        if p1_car == 'W11':
            battery += 0.1 * np.abs(y_vel) * (1 + ( - y_vel / (15 / scale)) ** 2 )
        else:
            battery += 0.1 * np.abs(y_vel)


    battery += 0.005

    if battery > 99.9:
        battery = 100
    elif battery < 0.1:
        battery = 0


    # P2
    # battery deployment mode
    if keys[pygame.K_QUOTE]:
        mode_ = 'n'
    if keys[pygame.K_SEMICOLON]:
        mode_ = 'l'
    if keys[pygame.K_l]:
        mode_ = 'm'
    if keys[pygame.K_k]:
        mode_ = 'h'

    if not keys[pygame.K_DOWN]:
        if mode_ == 'n':
            battery_ += 0.03 * np.abs(y_vel_)
            if battery_ > 0 and (keys[pygame.K_UP] or p2_auto_throttle == 'on'):
                y_acc_ += 0 * y_acc_max_
                battery_ -= 0
            elif not (keys[pygame.K_UP] or p2_auto_throttle == 'on'):
                battery_ += 0.01 * np.abs(y_vel_)
        elif mode_ == 'l':
            battery_ += 0.02 * np.abs(y_vel_)
            if battery_ > 0 and (keys[pygame.K_UP] or p2_auto_throttle == 'on'):
                y_acc_ += 0.1 * y_acc_max_
                battery_ -= 0.1
            elif not (keys[pygame.K_UP] or p2_auto_throttle == 'on'):
                battery_ += 0.02 * np.abs(y_vel_)
        elif mode_ == 'm':
            battery_ += 0.01 * np.abs(y_vel_)
            if battery_ > 0 and (keys[pygame.K_UP] or p2_auto_throttle == 'on'):
                y_acc_ += 0.2 * y_acc_max_
                battery_ -= 0.2
            elif not (keys[pygame.K_UP] or p2_auto_throttle == 'on'):
                battery_ += 0.03 * np.abs(y_vel_)
        elif mode_ == 'h':
            battery_ += 0 * np.abs(y_vel_)
            if battery_ > 0 and (keys[pygame.K_UP] or p2_auto_throttle == 'on'):
                y_acc_ += 0.3 * y_acc_max_
                battery_ -= 0.3
            elif battery_ == 0 and (keys[pygame.K_UP] or p2_auto_throttle == 'on'):
                mode_ = 'm'
            elif not (keys[pygame.K_UP] or p2_auto_throttle == 'on'):
                battery_ += 0.04 * np.abs(y_vel_)
    elif keys[pygame.K_DOWN] and y_vel_ < 0:
        if p2_car == 'W11':
            battery_ += 0.1 * np.abs(y_vel_) * (1 + ( - y_vel_ / (15 / scale)) ** 2 )
        else:
            battery_ += 0.1 * np.abs(y_vel_)

    battery_ += 0.005

    if battery_ > 99.9:
        battery_ = 100
    elif battery_ < 0.1:
        battery_ = 0


    # P1
    # cruise control (part one)
    # can be used between 60 kph to 341 kph
    if keys[pygame.K_1] and cruise_control == False and y_vel > -34.1 / scale and y_vel < -6 / scale:
        cruise_control = True
        constant = y_vel
    elif ( keys[pygame.K_2] or keys[pygame.K_s] ) and cruise_control == True:
        cruise_control = False
    elif keys[pygame.K_w] and cruise_control == True:
        cruise_control_hold = True


    # P2
    # cruise control (part one)
    # can be used between 60 kph to 341 kph
    if keys[pygame.K_PERIOD] and cruise_control_ == False and y_vel_ > -34.1 / scale and y_vel_ < -6 / scale:
        cruise_control_ = True
        constant_ = y_vel_
    elif ( keys[pygame.K_SLASH] or keys[pygame.K_DOWN] ) and cruise_control_ == True:
        cruise_control_ = False
    elif keys[pygame.K_UP] and cruise_control_ == True:
        cruise_control_hold_ = True

    # P1
    # determine if car is wrecked or damaged
    if life == 0:
        y_acc = 0
        turbo_boost_option = False
        cruise_control = False
    elif life > 0 and life <= 99.99:
        y_acc = ( life / 100 ) * y_acc
        life += 0.01


    # P2
    # determine if car is wrecked or damaged
    if life_ == 0:
        y_acc_ = 0
        turbo_boost_option_ = False
        cruise_control_ = False
    elif life_ > 0 and life_ <= 99.99:
        y_acc_ = ( life_ / 100 ) * y_acc
        life_ += 0.01

    # P1
    # acceleration / braking and steering
    if keys[pygame.K_a]:
        x_vel -= x_acc
    if keys[pygame.K_d]:
        x_vel += x_acc
    if p1_auto_throttle == 'on':
        if not keys[pygame.K_s]:
            y_vel -= y_acc
    elif p1_auto_throttle == 'off':
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            y_vel -= y_acc
    if keys[pygame.K_s] and y_vel < 0:
        y_vel += y_dcc
    # n2o boost
    if keys[pygame.K_e] and n2o_quantity >= 1:
        y_vel -= y_acc_n2o
        n2o_quantity -= 1
    elif n2o_quantity < full_n2o_quantity:
        n2o_quantity += 0.1 * ( - y_vel / (10 / scale))
    # turbo boost
    if t >= turbo_reboot_t and life != 0:
        turbo_boost_option = True
    if keys[pygame.K_r] and (keys[pygame.K_w] or p1_auto_throttle == 'on') and turbo_boost_option == True:
        turbo_boost_option = False
        turbo_boost = True
        turbo_end_t = t + turbo_boost_duration
        turbo_reboot_t = turbo_end_t + turbo_recharge_duration
    if turbo_boost == True and t <= turbo_end_t:
        y_vel -= y_acc_turbo
    else:
        turbo_boost = False

    # P2
    # acceleration / braking and steering
    if keys[pygame.K_LEFT]:
        x_vel_ -= x_acc_
    if keys[pygame.K_RIGHT]:
        x_vel_ += x_acc_
    if p2_auto_throttle == 'on':
        if not keys[pygame.K_DOWN]:
            y_vel_ -= y_acc_
    elif p2_auto_throttle == 'off':
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            y_vel_ -= y_acc_
    if keys[pygame.K_DOWN] and y_vel_ < 0:
        if p2_car == 'W11':
            y_vel_ += y_dcc_ * (1 + ( - y_vel_ / (15 / scale)) ** 2 )
        else:
            y_vel_ += y_dcc_
    # n2o boost
    if keys[pygame.K_RSHIFT] and n2o_quantity_ >= 1:
        y_vel_ -= y_acc_n2o_
        n2o_quantity_ -= 1
    elif n2o_quantity_ < full_n2o_quantity_:
        n2o_quantity_ += 0.1 * ( - y_vel_ / (10 / scale))
    # turbo boost
    if t >= turbo_reboot_t_ and life_ != 0:
        turbo_boost_option_ = True
    if keys[pygame.K_COMMA] and (keys[pygame.K_UP] or p2_auto_throttle == 'on') and turbo_boost_option_ == True:
        turbo_boost_option_ = False
        turbo_boost_ = True
        turbo_end_t_ = t + turbo_boost_duration_
        turbo_reboot_t_ = turbo_end_t_ + turbo_recharge_duration_
    if turbo_boost_ == True and t <= turbo_end_t_:
        y_vel_ -= y_acc_turbo_
    else:
        turbo_boost_ = False


    # P1
    # determine DRS for Mercedes W11
    # complex touch to open / to close mechanism
    if p1_car == 'W11':
        if keys[pygame.K_q] and button_hold == False:
            if drs_open == False:
                drs_open = True
                button_hold = True
            elif drs_open == True:
                drs_open = False
                button_hold = True
        elif keys[pygame.K_q] and button_hold == True:
            pass
        else:
            button_hold = False

        if drs_open == True:
            y_air_s = y_air_s_drs
        elif drs_open == False:
            y_air_s = y_air_s_no_drs


    # P2
    # determine DRS for Mercedes W11
    # complex touch to open / to close mechanism
    if p2_car == 'W11':
        if keys[pygame.K_RETURN] and button_hold_ == False:
            if drs_open_ == False:
                drs_open_ = True
                button_hold_ = True
            elif drs_open_ == True:
                drs_open_ = False
                button_hold_ = True
        elif keys[pygame.K_RETURN] and button_hold_ == True:
            pass
        else:
            button_hold_ = False

        if drs_open_ == True:
            y_air_s_ = y_air_s_drs_
        elif drs_open_ == False:
            y_air_s_ = y_air_s_no_drs_



    # coefficient of restitution
    e = 0.2 + 0.8 * np.exp(- np.abs(x_vel_ - x_vel) / (10 / scale))
    e_ = 0.2 + 0.8 * np.exp(- np.abs(y_vel_ - y_vel) / (10 / scale))

    # P1 & P2
    # horizontal and vertical bumping between P1 and P2
    if np.abs(x_ - x) - width < np.abs(x_vel_ - x_vel) and np.abs(y_ - y) < height:
        # record x velocity before impact
        x_vel_i = x_vel
        x_vel_i_ = x_vel_
        # update x velocity post impact
        x_vel = ((1 - e) / 2) * x_vel_i + ((1 + e) / 2) * x_vel_i_ - 0.001 * (x_ - x)
        x_vel_ = ((1 + e) / 2) * x_vel_i + ((1 - e) / 2) * x_vel_i_ + 0.001 * (x_ - x)
        # record x velocity after impact
        x_vel_f = x_vel
        x_vel_f_ = x_vel_
        # update car life
        if life > 0:
            life -= damage_c * ( x_vel_i - x_vel_f ) ** 2
        else:
            life = 0
        if life_ > 0:
            life_ -= damage_c_ * ( x_vel_i_ - x_vel_f_ ) ** 2
        else:
            life_ = 0
    else:
        pass
    # P1 in front of P2
    if np.abs(y_ - y) - height < np.abs(y_vel_ - y_vel) and np.abs(x_ - x) < width and y_ > y:
        # record y velocity before impact
        y_vel_i = y_vel
        y_vel_i_ = y_vel_
        # update y velocity post impact
        y_vel = ((1 - e_) / 2) * y_vel_i + ((1 + e_) / 2) * y_vel_i_ - 0.001 * (y_ - y)
        y_vel_ = ((1 + e_) / 2) * y_vel_i + ((1 - e_) / 2) * y_vel_i_ + 0.001 * (y_ - y)
        # record y velocity after impact
        y_vel_f = y_vel
        y_vel_f_ = y_vel_
        # update car life
        if life > 0:
            life -= 0.9 * damage_c * ( y_vel_i - y_vel_f ) ** 2
        else:
            life = 0
        if life_ > 0:
            life_ -= 0.8 * damage_c_ * ( y_vel_i_ - y_vel_f_ ) ** 2
        else:
            life_ = 0
    # P2 in front of P1
    elif np.abs(y_ - y) - height < np.abs(y_vel_ - y_vel) and np.abs(x_ - x) < width and y_ < y:
        # record y velocity before impact
        y_vel_i = y_vel
        y_vel_i_ = y_vel_
        # update y velocity post impact
        y_vel = ((1 - e_) / 2) * y_vel_i + ((1 + e_) / 2) * y_vel_i_ - 0.001 * (y_ - y)
        y_vel_ = ((1 + e_) / 2) * y_vel_i + ((1 - e_) / 2) * y_vel_i_ + 0.001 * (y_ - y)
        # record y velocity after impact
        y_vel_f = y_vel
        y_vel_f_ = y_vel_
        # update car life
        if life > 0:
            life -= 0.8 * damage_c * ( y_vel_i - y_vel_f ) ** 2
        else:
            life = 0
        if life_ > 0:
            life_ -= 0.9 * damage_c_ * ( y_vel_i_ - y_vel_f_ ) ** 2
        else:
            life_ = 0
    else:
        pass


    # if y_ > -y_vel_ and y_ < size - height_ - y_vel_:
    #     pass
    # else:
    #     y_vel_ = y_vel


    # P1
    # horizontal bumping (with map edge) and update location
    if x > -x_vel and x < size - width - x_vel:
        x += x_vel
    else:
        if life > 0:
            life -= damage_c * x_vel ** 2
        else:
            life = 0
        x_vel = - 0.5 * x_vel
    # # check if P1 is in P2 field of view
    # if y > -y_vel and y < size - height - y_vel:
    #     y += y_vel
    # else:
    #     y_vel = -y_vel

    # P2
    # horizontal bumping (with map edge) and update location
    if x_ > -x_vel_ and x_ < size - width_ - x_vel_:
        x_ += x_vel_
    else:
        if life_ > 0:
            life_ -= damage_c_ * x_vel_ ** 2
        else:
            life_ = 0
        x_vel_ = - 0.5 * x_vel_
    # if y_ > -y_vel_ and y_ < size - height_ - y_vel_:
    #     pass
    # elif y_ <= -y_vel_:
    #     y_vel_ = y_vel + 0.5
    # elif y_ >= size - height_ - y_vel_:
    #     y_vel_ = y_vel - 0.5

    # set below zero life to zero
    if life < 0:
        life = 0
    if life_ < 0:
        life_ = 0


    # P1
    # friction reduces velocity
    if x_vel > 0:
        x_vel -= x_fri + x_air * x_vel ** 2
    elif x_vel < 0:
        x_vel += x_fri + x_air * x_vel ** 2

    if y_vel > 0:
        y_vel -= y_fri + y_air * y_vel ** 2
    elif y_vel < 0:
        y_vel += y_fri + y_air * y_vel ** 2

    # P2
    # friction reduces velocity
    if x_vel_ > 0:
        x_vel_ -= x_fri_ + x_air_ * x_vel_ ** 2
    elif x_vel_ < 0:
        x_vel_ += x_fri_ + x_air_ * x_vel_ ** 2

    if y_vel_ > 0:
        y_vel_ -= y_fri_ + y_air_ * y_vel_ ** 2
    elif y_vel_ < 0:
        y_vel_ += y_fri_ + y_air_ * y_vel_ ** 2

    # P1
    # cruise control (part two)
    if cruise_control_hold == False:
        if cruise_control == True:
            y_vel = constant
    elif cruise_control_hold == True:
        if y_vel > constant - 0.1:
            accelerated = True
        if accelerated == True:
            if y_vel > constant and y_vel < constant + 0.1:
                y_vel = constant
                cruise_control_hold = False
                accelerated = False

    # P2
    # cruise control (part two)
    if cruise_control_hold_ == False:
        if cruise_control_ == True and y_ > 0 and y_ < size:
            y_vel_ = constant_
    elif cruise_control_hold_ == True:
        if y_vel_ > constant_ - 0.1:
            accelerated_ = True
        if accelerated_ == True:
            if y_vel_ > constant_ and y_vel_ < constant_ + 0.1:
                y_vel_ = constant_
                cruise_control_hold_ = False
                accelerated_ = False

    # P1 view
    # update tree location
    tree_y_array = tree_y_array - y_vel
    for i in range(0, 16):
        if tree_y_array[i] > size:
            tree_y_array[i] -= size
        globals()['y_{}'.format(i + 1)] = tree_y_array[i]

    # y_1 -= y_vel
    # if y_1 > size:
    #     y_1 -= size
    #
    # y_2 -= y_vel
    # if y_2 > size:
    #     y_2 -= size
    #
    # y_3 -= y_vel
    # if y_3 > size:
    #     y_3 -= size
    #
    # y_4 -= y_vel
    # if y_4 > size:
    #     y_4 -= size
    #
    # y_5 -= y_vel
    # if y_5 > size:
    #     y_5 -= size
    #
    # y_6 -= y_vel
    # if y_6 > size:
    #     y_6 -= size
    #
    # y_7 -= y_vel
    # if y_7 > size:
    #     y_7 -= size
    #
    # y_8 -= y_vel
    # if y_8 > size:
    #     y_8 -= size
    #
    # y_9 -= y_vel
    # if y_9 > size:
    #     y_9 -= size
    #
    # y_10 -= y_vel
    # if y_10 > size:
    #     y_10 -= size
    #
    # y_11 -= y_vel
    # if y_11 > size:
    #     y_11 -= size
    #
    # y_12 -= y_vel
    # if y_12 > size:
    #     y_12 -= size
    #
    # y_13 -= y_vel
    # if y_13 > size:
    #     y_13 -= size
    #
    # y_14 -= y_vel
    # if y_14 > size:
    #     y_14 -= size
    #
    # y_15 -= y_vel
    # if y_15 > size:
    #     y_15 -= size
    #
    # y_16 -= y_vel
    # if y_16 > size:
    #     y_16 -= size

    # P2 view
    # update tree location
    tree_y_array_ = tree_y_array_ - y_vel_
    for i in range(0, 16):
        if tree_y_array_[i] > size:
            tree_y_array_[i] -= size
        globals()['y_{}_'.format(i + 1)] = tree_y_array_[i]


    # y_1_ -= y_vel_
    # if y_1_ > size:
    #     y_1_ -= size
    #
    # y_2_ -= y_vel_
    # if y_2_ > size:
    #     y_2_ -= size
    #
    # y_3_ -= y_vel_
    # if y_3_ > size:
    #     y_3_ -= size
    #
    # y_4_ -= y_vel_
    # if y_4_ > size:
    #     y_4_ -= size
    #
    # y_5_ -= y_vel_
    # if y_5_ > size:
    #     y_5_ -= size
    #
    # y_6_ -= y_vel_
    # if y_6_ > size:
    #     y_6_ -= size
    #
    # y_7_ -= y_vel_
    # if y_7_ > size:
    #     y_7_ -= size
    #
    # y_8_ -= y_vel_
    # if y_8_ > size:
    #     y_8_ -= size
    #
    # y_9_ -= y_vel_
    # if y_9_ > size:
    #     y_9_ -= size
    #
    # y_10_ -= y_vel_
    # if y_10_ > size:
    #     y_10_ -= size
    #
    # y_11_ -= y_vel_
    # if y_11_ > size:
    #     y_11_ -= size
    #
    # y_12_ -= y_vel_
    # if y_12_ > size:
    #     y_12_ -= size
    #
    # y_13_ -= y_vel_
    # if y_13_ > size:
    #     y_13_ -= size
    #
    # y_14_ -= y_vel_
    # if y_14_ > size:
    #     y_14_ -= size
    #
    # y_15_ -= y_vel_
    # if y_15_ > size:
    #     y_15_ -= size
    #
    # y_16_ -= y_vel_
    # if y_16_ > size:
    #     y_16_ -= size

    # P1 view
    # update lane divider location
    divider_y_array = divider_y_array - y_vel
    for i in range(0, 25):
        if divider_y_array[i] > size:
            divider_y_array[i] -= size
        if i in range(0, 9):
            globals()['y_10{}'.format(i + 1)] = divider_y_array[i]
        elif i in range(9, 25):
            globals()['y_1{}'.format(i + 1)] = divider_y_array[i]

    # y_101 -= y_vel
    # if y_101 > size:
    #     y_101 -= size
    #
    # y_102 -= y_vel
    # if y_102 > size:
    #     y_102 -= size
    #
    # y_103 -= y_vel
    # if y_103 > size:
    #     y_103 -= size
    #
    # y_104 -= y_vel
    # if y_104 > size:
    #     y_104 -= size
    #
    # y_105 -= y_vel
    # if y_105 > size:
    #     y_105 -= size
    #
    # y_106 -= y_vel
    # if y_106 > size:
    #     y_106 -= size
    #
    # y_107 -= y_vel
    # if y_107 > size:
    #     y_107 -= size
    #
    # y_108 -= y_vel
    # if y_108 > size:
    #     y_108 -= size
    #
    # y_109 -= y_vel
    # if y_109 > size:
    #     y_109 -= size
    #
    # y_110 -= y_vel
    # if y_110 > size:
    #     y_110 -= size
    #
    # y_111 -= y_vel
    # if y_111 > size:
    #     y_111 -= size
    #
    # y_112 -= y_vel
    # if y_112 > size:
    #     y_112 -= size
    #
    # y_113 -= y_vel
    # if y_113 > size:
    #     y_113 -= size
    #
    # y_114 -= y_vel
    # if y_114 > size:
    #     y_114 -= size
    #
    # y_115 -= y_vel
    # if y_115 > size:
    #     y_115 -= size
    #
    # y_116 -= y_vel
    # if y_116 > size:
    #     y_116 -= size
    #
    # y_117 -= y_vel
    # if y_117 > size:
    #     y_117 -= size
    #
    # y_118 -= y_vel
    # if y_118 > size:
    #     y_118 -= size
    #
    # y_119 -= y_vel
    # if y_119 > size:
    #     y_119 -= size
    #
    # y_120 -= y_vel
    # if y_120 > size:
    #     y_120 -= size
    #
    # y_121 -= y_vel
    # if y_121 > size:
    #     y_121 -= size
    #
    # y_122 -= y_vel
    # if y_122 > size:
    #     y_122 -= size
    #
    # y_123 -= y_vel
    # if y_123 > size:
    #     y_123 -= size
    #
    # y_124 -= y_vel
    # if y_124 > size:
    #     y_124 -= size
    #
    # y_125 -= y_vel
    # if y_125 > size:
    #     y_125 -= size

    # P2 view
    # update lane divider location
    divider_y_array_ = divider_y_array_ - y_vel_
    for i in range(0, 25):
        if divider_y_array_[i] > size:
            divider_y_array_[i] -= size
        if i in range(0, 9):
            globals()['y_10{}_'.format(i + 1)] = divider_y_array_[i]
        elif i in range(9, 25):
            globals()['y_1{}_'.format(i + 1)] = divider_y_array_[i]


    # y_101_ -= y_vel_
    # if y_101_ > size:
    #     y_101_ -= size
    #
    # y_102_ -= y_vel_
    # if y_102_ > size:
    #     y_102_ -= size
    #
    # y_103_ -= y_vel_
    # if y_103_ > size:
    #     y_103_ -= size
    #
    # y_104_ -= y_vel_
    # if y_104_ > size:
    #     y_104_ -= size
    #
    # y_105_ -= y_vel_
    # if y_105_ > size:
    #     y_105_ -= size
    #
    # y_106_ -= y_vel_
    # if y_106_ > size:
    #     y_106_ -= size
    #
    # y_107_ -= y_vel_
    # if y_107_ > size:
    #     y_107_ -= size
    #
    # y_108_ -= y_vel_
    # if y_108_ > size:
    #     y_108_ -= size
    #
    # y_109_ -= y_vel_
    # if y_109_ > size:
    #     y_109_ -= size
    #
    # y_110_ -= y_vel_
    # if y_110_ > size:
    #     y_110_ -= size
    #
    # y_111_ -= y_vel_
    # if y_111_ > size:
    #     y_111_ -= size
    #
    # y_112_ -= y_vel_
    # if y_112_ > size:
    #     y_112_ -= size
    #
    # y_113_ -= y_vel_
    # if y_113_ > size:
    #     y_113_ -= size
    #
    # y_114_ -= y_vel_
    # if y_114_ > size:
    #     y_114_ -= size
    #
    # y_115_ -= y_vel_
    # if y_115_ > size:
    #     y_115_ -= size
    #
    # y_116_ -= y_vel_
    # if y_116_ > size:
    #     y_116_ -= size
    #
    # y_117_ -= y_vel_
    # if y_117_ > size:
    #     y_117_ -= size
    #
    # y_118_ -= y_vel_
    # if y_118_ > size:
    #     y_118_ -= size
    #
    # y_119_ -= y_vel_
    # if y_119_ > size:
    #     y_119_ -= size
    #
    # y_120_ -= y_vel_
    # if y_120_ > size:
    #     y_120_ -= size
    #
    # y_121_ -= y_vel_
    # if y_121_ > size:
    #     y_121_ -= size
    #
    # y_122_ -= y_vel_
    # if y_122_ > size:
    #     y_122_ -= size
    #
    # y_123_ -= y_vel_
    # if y_123_ > size:
    #     y_123_ -= size
    #
    # y_124_ -= y_vel_
    # if y_124_ > size:
    #     y_124_ -= size
    #
    # y_125_ -= y_vel_
    # if y_125_ > size:
    #     y_125_ -= size

    # P1 view
    # update AI car location (constant speed)
    y_a -= y_vel + a_vel
    y_b -= y_vel + b_vel

    # P2 view
    # update AI car location (constant speed)
    y_a_ -= y_vel_ + a_vel
    y_b_ -= y_vel_ + b_vel

    # P1 view
    # update P2 car location
    y_ -= y_vel - y_vel_

    # P2 view
    # update P1 car location
    yy -= y_vel_ - y_vel



    # P1
    # update travelled distance
    distance -= y_vel

    # P2
    # update travelled distance
    distance_ -= y_vel_

    # P1
    # calculate speed
    # vel = np.sqrt( x_vel ** 2 + y_vel ** 2 )
    vel = np.abs(y_vel)

    # P2
    # calculate speed
    # vel_ = np.sqrt( x_vel_ ** 2 + y_vel_ ** 2 )
    vel_ = np.abs(y_vel_)

    # P1
    # update car separation
    separation = y - y_

    # P2
    # update car separation
    separation_ = y_ - y


    # fill road surface color
    win.fill(win_color)

    # draw center gray area
    # P1 view
    pygame.draw.rect(win, (100, 100, 100), (0.4 * size, 0, 0.2 * size, size))
    # P2 view
    pygame.draw.rect(win, (100, 100, 100), (size + 0.4 * size, 0, 0.2 * size, size))

    # draw orange lines
    # P1 view
    pygame.draw.rect(win, (214, 139, 0), (0.4 * size - 3 * divider_width, 0, divider_width, size))
    pygame.draw.rect(win, (214, 139, 0), (0.6 * size + 2 * divider_width, 0, divider_width, size))
    # P2 view
    pygame.draw.rect(win, (214, 139, 0), (size + 0.4 * size - 3 * divider_width, 0, divider_width, size))
    pygame.draw.rect(win, (214, 139, 0), (size + 0.6 * size + 2 * divider_width, 0, divider_width, size))

    # draw white lines
    # P1 view
    pygame.draw.rect(win, (200, 200, 200), (x_1 + side_width - divider_width, 0, divider_width, size))
    pygame.draw.rect(win, (200, 200, 200), (size - x_1 - side_width, 0, divider_width, size))

    pygame.draw.rect(win, (200, 200, 200), (x_900 + lane_width, 0, divider_width, size))
    pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900 - lane_width, 0, divider_width, size))
    # P2 view
    pygame.draw.rect(win, (200, 200, 200), (size + x_1 + side_width - divider_width, 0, divider_width, size))
    pygame.draw.rect(win, (200, 200, 200), (size + size - x_1 - side_width, 0, divider_width, size))

    pygame.draw.rect(win, (200, 200, 200), (size + x_900 + lane_width, 0, divider_width, size))
    pygame.draw.rect(win, (200, 200, 200), (size + size - divider_width - x_900 - lane_width, 0, divider_width, size))

    # draw lane dividers

    # # from left side
    # # P1 view
    # # column 1
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_100, y_125, divider_width, divider_height))
    # # P2 view
    # # column 1
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_100, y_125_, divider_width, divider_height))

    # # P1 view
    # # column 2
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_200, y_125, divider_width, divider_height))
    # # P2 view
    # # column 2
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_200, y_125_, divider_width, divider_height))

    # P1 view
    # column 3
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_101, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_102, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_103, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_104, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_105, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_106, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_107, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_108, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_109, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_110, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_111, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_112, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_113, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_114, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_115, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_116, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_117, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_118, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_119, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_120, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_121, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_122, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_123, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_124, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_300, y_125, divider_width, divider_height))
    # P2 view
    # column 3
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_101_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_102_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_103_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_104_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_105_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_106_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_107_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_108_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_109_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_110_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_111_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_112_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_113_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_114_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_115_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_116_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_117_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_118_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_119_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_120_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_121_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_122_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_123_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_124_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_300, y_125_, divider_width, divider_height))

    # P1 view
    # column 4
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_101, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_102, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_103, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_104, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_105, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_106, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_107, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_108, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_109, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_110, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_111, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_112, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_113, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_114, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_115, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_116, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_117, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_118, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_119, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_120, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_121, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_122, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_123, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_124, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_400, y_125, divider_width, divider_height))
    # P2 view
    # column 4
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_101_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_102_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_103_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_104_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_105_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_106_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_107_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_108_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_109_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_110_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_111_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_112_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_113_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_114_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_115_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_116_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_117_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_118_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_119_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_120_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_121_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_122_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_123_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_124_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_400, y_125_, divider_width, divider_height))

    # P1 view
    # column 5
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_101, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_102, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_103, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_104, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_105, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_106, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_107, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_108, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_109, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_110, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_111, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_112, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_113, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_114, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_115, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_116, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_117, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_118, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_119, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_120, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_121, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_122, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_123, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_124, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_500, y_125, divider_width, divider_height))
    # P2 view
    # column 5
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_101_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_102_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_103_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_104_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_105_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_106_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_107_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_108_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_109_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_110_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_111_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_112_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_113_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_114_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_115_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_116_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_117_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_118_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_119_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_120_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_121_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_122_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_123_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_124_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_500, y_125_, divider_width, divider_height))

    # P1 view
    # column 6
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_101, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_102, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_103, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_104, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_105, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_106, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_107, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_108, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_109, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_110, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_111, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_112, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_113, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_114, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_115, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_116, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_117, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_118, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_119, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_120, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_121, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_122, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_123, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_124, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_600, y_125, divider_width, divider_height))
    # P2 view
    # column 6
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_101_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_102_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_103_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_104_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_105_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_106_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_107_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_108_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_109_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_110_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_111_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_112_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_113_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_114_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_115_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_116_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_117_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_118_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_119_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_120_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_121_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_122_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_123_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_124_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_600, y_125_, divider_width, divider_height))

    # P1 view
    # column 7
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_101, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_102, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_103, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_104, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_105, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_106, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_107, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_108, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_109, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_110, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_111, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_112, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_113, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_114, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_115, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_116, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_117, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_118, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_119, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_120, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_121, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_122, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_123, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_124, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (x_700, y_125, divider_width, divider_height))
    # P2 view
    # column 7
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_101_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_102_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_103_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_104_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_105_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_106_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_107_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_108_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_109_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_110_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_111_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_112_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_113_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_114_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_115_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_116_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_117_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_118_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_119_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_120_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_121_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_122_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_123_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_124_, divider_width, divider_height))
    pygame.draw.rect(win, (200, 200, 200), (size + x_700, y_125_, divider_width, divider_height))

    # # P1 view
    # # column 8
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_800, y_125, divider_width, divider_height))
    # # P1 view
    # # column 8
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_800, y_125_, divider_width, divider_height))
    #
    # # P1 view
    # # column 9
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (x_900, y_125, divider_width, divider_height))
    # # P2 view
    # # column 9
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size + x_900, y_125_, divider_width, divider_height))

    #
    # # from right side
    # # P1 view
    # # column 1
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_100, y_125, divider_width, divider_height))
    # # P2 view
    # # column 1
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_100, y_125_, divider_width, divider_height))
    #
    # # P1 view
    # # column 2
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_200, y_125, divider_width, divider_height))
    # # P2 view
    # # column 2
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_200, y_125_, divider_width, divider_height))
    #
    # # P1 view
    # # column 3
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_300, y_125, divider_width, divider_height))
    # # P2 view
    # # column 3
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_300, y_125_, divider_width, divider_height))
    #
    # # P1 view
    # # column 4
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_400, y_125, divider_width, divider_height))
    # # P2 view
    # # column 4
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_400, y_125_, divider_width, divider_height))
    #
    # # P1 view
    # # column 5
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_500, y_125, divider_width, divider_height))
    # # P2 view
    # # column 5
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_500, y_125_, divider_width, divider_height))
    #
    # # P1 view
    # # column 6
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_600, y_125, divider_width, divider_height))
    # # P2 view
    # # column 6
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_600, y_125_, divider_width, divider_height))
    #
    # # P1 view
    # # column 7
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_700, y_125, divider_width, divider_height))
    # # P2 view
    # # column 7
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_700, y_125_, divider_width, divider_height))
    #
    # # P1 view
    # # column 8
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_800, y_125, divider_width, divider_height))
    # # P2 view
    # # column 8
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_800, y_125_, divider_width, divider_height))
    #
    # # P1 view
    # # column 9
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_101, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_102, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_103, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_104, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_105, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_106, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_107, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_108, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_109, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_110, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_111, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_112, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_113, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_114, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_115, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_116, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_117, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_118, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_119, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_120, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_121, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_122, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_123, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_124, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (size - divider_width - x_900, y_125, divider_width, divider_height))
    # # P2 view
    # # column 9
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_101_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_102_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_103_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_104_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_105_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_106_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_107_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_108_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_109_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_110_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_111_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_112_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_113_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_114_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_115_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_116_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_117_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_118_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_119_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_120_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_121_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_122_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_123_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_124_, divider_width, divider_height))
    # pygame.draw.rect(win, (200, 200, 200), (2 * size - divider_width - x_900, y_125_, divider_width, divider_height))

    # lanes changed to river
    if river_exist == True:
        # P1 view
        pygame.draw.rect(win, (river_color[0], river_color[1], river_color[2]), (size - divider_width - x_900, 0, 8.2 * lane_width, size))
        # P2 view
        pygame.draw.rect(win, (river_color[0], river_color[1], river_color[2]), (2 * size - divider_width - x_900, 0, 8.2 * lane_width, size))

        # P1
        # determine if car is in river and therefore destroyed
        # if x > size - divider_width - x_900 and x < size - divider_width - x_900 + 8.2 * lane_width:
        if x > danger_x:
            life = 0
            x_vel = x_vel * 0.9
            y_vel = y_vel * 0.98
            show = False
        else:
            show = True

        # P2
        # determine if car is in river and therefore destroyed
        # if x_ > size - divider_width - x_900 and x_ < size - divider_width - x_900 + 8.2 * lane_width:
        if x_ > danger_x:
            life_ = 0
            x_vel_ = x_vel_ * 0.9
            y_vel_ = y_vel_ * 0.98
            show_ = False
        else:
            show_ = True


    # P1 car n2o effect
    # P1 view
    # show n2o effect
    if keys[pygame.K_e] and n2o_quantity >= 1:
        pygame.draw.rect(win, (180, 180, 255), (x + 0.1 * width, y + height, 0.3 * width, 0.3 * height))
        pygame.draw.rect(win, (180, 180, 255), (x + 0.6 * width, y + height, 0.3 * width, 0.3 * height))
    # P2 view
    # show n2o effect
    if keys[pygame.K_e] and n2o_quantity >= 1:
        pygame.draw.rect(win, (180, 180, 255), (size + x + 0.1 * width, yy + height, 0.3 * width, 0.3 * height))
        pygame.draw.rect(win, (180, 180, 255), (size + x + 0.6 * width, yy + height, 0.3 * width, 0.3 * height))

    # P2 car n2o effect
    # P1 view
    # show n2o effect
    if keys[pygame.K_RSHIFT] and n2o_quantity_ >= 1:
        pygame.draw.rect(win, (180, 180, 255), (x_ + 0.1 * width_, y_ + height_, 0.3 * width_, 0.3 * height_))
        pygame.draw.rect(win, (180, 180, 255), (x_ + 0.6 * width_, y_ + height_, 0.3 * width_, 0.3 * height_))
    # P2 view
    # show n2o effect
    if keys[pygame.K_RSHIFT] and n2o_quantity_ >= 1:
        pygame.draw.rect(win, (180, 180, 255), (size + x_ + 0.1 * width_, yy_ + height_, 0.3 * width_, 0.3 * height_))
        pygame.draw.rect(win, (180, 180, 255), (size + x_ + 0.6 * width_, yy_ + height_, 0.3 * width_, 0.3 * height_))


    # P1 car turbo effect
    # P1 view
    # show turbo effect
    if turbo_boost == True:
        pygame.draw.rect(win, (180, 255, 180), (x + 0.1 * width, y + height, 0.3 * width, 0.3 * height))
        pygame.draw.rect(win, (180, 255, 180), (x + 0.6 * width, y + height, 0.3 * width, 0.3 * height))
    # P2 view
    # show turbo effect
    if turbo_boost == True:
        pygame.draw.rect(win, (180, 255, 180), (size + x + 0.1 * width, yy + height, 0.3 * width, 0.3 * height))
        pygame.draw.rect(win, (180, 255, 180), (size + x + 0.6 * width, yy + height, 0.3 * width, 0.3 * height))

    # P2 car turbo effect
    # P1 view
    # show turbo effect
    if turbo_boost_ == True:
        pygame.draw.rect(win, (180, 255, 180), (x_ + 0.1 * width_, y_ + height_, 0.3 * width_, 0.3 * height_))
        pygame.draw.rect(win, (180, 255, 180), (x_ + 0.6 * width_, y_ + height_, 0.3 * width_, 0.3 * height_))
    # P2 view
    # show turbo effect
    if turbo_boost_ == True:
        pygame.draw.rect(win, (180, 255, 180), (size + x_ + 0.1 * width_, yy_ + height_, 0.3 * width_, 0.3 * height_))
        pygame.draw.rect(win, (180, 255, 180), (size + x_ + 0.6 * width_, yy_ + height_, 0.3 * width_, 0.3 * height_))

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> P1 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    if p1_car == 'SF90':
        # P1 view
        # draw P1 car
        pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
        if show == False:
            pygame.draw.rect(win, (164, 180, 188), (x, y, width, height))

        # P2 view
        # draw P1 car
        pygame.draw.rect(win, (255, 0, 0), (size + x, yy, width, height))
        if show == False:
            pygame.draw.rect(win, (164, 180, 188), (size + x, yy, width, height))

    elif p1_car == 'W11':
        # P1 view
        # draw P2 car
        # pygame.draw.rect(win, (100, 100, 100), (x, y, width, height))
        pygame.draw.rect(win, p1_color, (x, y, width, 0.1 * height))
        pygame.draw.rect(win, p1_color, (x, y + 0.2 * height, width, 0.05 * height))
        pygame.draw.rect(win, p1_color, (x + 0.4 * width, y, 0.2 * width, height))
        pygame.draw.rect(win, p1_color, (x + 0.3 * width, y + 0.2 * height, 0.4 * width, height))
        pygame.draw.rect(win, p1_color, (x + 0.2 * width, y + 0.4 * height, 0.6 * width, 0.6 * height))
        pygame.draw.rect(win, p1_color, (x, y + 0.6 * height, width, 0.4 * height))
        pygame.draw.rect(win, p1_color, (x, y + 1.1 * height, width, 0.1 * height))

        pygame.draw.rect(win, tyre_color, (x, y + 0.15 * height, 0.2 * width, 0.2 * height))
        pygame.draw.rect(win, tyre_color, (x + 0.8 * width, y + 0.15 * height, 0.2 * width, 0.2 * height))
        pygame.draw.rect(win, tyre_color, (x, y + 0.85 * height, 0.3 * width, 0.2 * height))
        pygame.draw.rect(win, tyre_color, (x + 0.7 * width, y + 0.85 * height, 0.3 * width, 0.2 * height))
        if show == False:
            pygame.draw.rect(win, p1_color_in_river, (x, y, width, 0.1 * height))
            pygame.draw.rect(win, p1_color_in_river, (x, y + 0.2 * height, width, 0.05 * height))
            pygame.draw.rect(win, p1_color_in_river, (x + 0.4 * width, y, 0.2 * width, height))
            pygame.draw.rect(win, p1_color_in_river, (x + 0.3 * width, y + 0.2 * height, 0.4 * width, height))
            pygame.draw.rect(win, p1_color_in_river, (x + 0.2 * width, y + 0.4 * height, 0.6 * width, 0.6 * height))
            pygame.draw.rect(win, p1_color_in_river, (x, y + 0.6 * height, width, 0.4 * height))
            pygame.draw.rect(win, p1_color_in_river, (x, y + 1.1 * height, width, 0.1 * height))

            pygame.draw.rect(win, tyre_color_in_river, (x, y + 0.15 * height, 0.2 * width, 0.2 * height))
            pygame.draw.rect(win, tyre_color_in_river, (x + 0.8 * width, y + 0.15 * height, 0.2 * width, 0.2 * height))
            pygame.draw.rect(win, tyre_color_in_river, (x, y + 0.85 * height, 0.3 * width, 0.2 * height))
            pygame.draw.rect(win, tyre_color_in_river, (x + 0.7 * width, y + 0.85 * height, 0.3 * width, 0.2 * height))

        # P2 view
        # draw P2 car
        # pygame.draw.rect(win, (100, 100, 100), (size + x, yy, width, height))
        pygame.draw.rect(win, p1_color, (size + x, yy, width, 0.1 * height))
        pygame.draw.rect(win, p1_color, (size + x, yy + 0.2 * height, width, 0.05 * height))
        pygame.draw.rect(win, p1_color, (size + x + 0.4 * width, yy, 0.2 * width, height))
        pygame.draw.rect(win, p1_color, (size + x + 0.3 * width, yy + 0.2 * height, 0.4 * width, height))
        pygame.draw.rect(win, p1_color, (size + x + 0.2 * width, yy + 0.4 * height, 0.6 * width, 0.6 * height))
        pygame.draw.rect(win, p1_color, (size + x, yy + 0.6 * height, width, 0.4 * height))
        pygame.draw.rect(win, p1_color, (size + x, yy + 1.1 * height, width, 0.1 * height))

        pygame.draw.rect(win, tyre_color, (size + x, yy + 0.15 * height, 0.2 * width, 0.2 * height))
        pygame.draw.rect(win, tyre_color, (size + x + 0.8 * width, yy + 0.15 * height, 0.2 * width, 0.2 * height))
        pygame.draw.rect(win, tyre_color, (size + x, yy + 0.85 * height, 0.3 * width, 0.2 * height))
        pygame.draw.rect(win, tyre_color, (size + x + 0.7 * width, yy + 0.85 * height, 0.3 * width, 0.2 * height))
        if show == False:
            pygame.draw.rect(win, p1_color_in_river, (size + x, yy, width, 0.1 * height))
            pygame.draw.rect(win, p1_color_in_river, (size + x, yy + 0.2 * height, width, 0.05 * height))
            pygame.draw.rect(win, p1_color_in_river, (size + x + 0.4 * width, yy, 0.2 * width, height))
            pygame.draw.rect(win, p1_color_in_river, (size + x + 0.3 * width, yy + 0.2 * height, 0.4 * width, height))
            pygame.draw.rect(win, p1_color_in_river, (size + x + 0.2 * width, yy + 0.4 * height, 0.6 * width, 0.6 * height))
            pygame.draw.rect(win, p1_color_in_river, (size + x, yy + 0.6 * height, width, 0.4 * height))
            pygame.draw.rect(win, p1_color_in_river, (size + x, yy + 1.1 * height, width, 0.1 * height))

            pygame.draw.rect(win, tyre_color_in_river, (size + x, yy + 0.15 * height, 0.2 * width, 0.2 * height))
            pygame.draw.rect(win, tyre_color_in_river,
                             (size + x + 0.8 * width, yy + 0.15 * height, 0.2 * width, 0.2 * height))
            pygame.draw.rect(win, tyre_color_in_river, (size + x, yy + 0.85 * height, 0.3 * width, 0.2 * height))
            pygame.draw.rect(win, tyre_color_in_river,
                             (size + x + 0.7 * width, yy + 0.85 * height, 0.3 * width, 0.2 * height))

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> P2 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    if p2_car == 'SF90':
        # P1 view
        # draw P2 car
        pygame.draw.rect(win, (240, 200, 30), (x_, y_, width_, height_))
        if show_ == False:
            pygame.draw.rect(win, (162, 204, 192), (x_, y_, width_, height_))

        # P2 view
        # draw P2 car
        pygame.draw.rect(win, (240, 200, 30), (size + x_, yy_, width_, height_))
        if show_ == False:
            pygame.draw.rect(win, (162, 204, 192), (size + x_, yy_, width_, height_))

    elif p2_car == 'police':
        # P1 view
        # draw P2 car
        pygame.draw.rect(win, (p2_color[0], p2_color[1], p2_color[2]), (x_, y_, width_, height_))
        if round((t / t_scale) * 8) % 2 == 0:
            pygame.draw.rect(win, (p2_siren_red[0], p2_siren_red[1], p2_siren_red[2]),
                             (x_, y_ + height_ * 0.4, width_ * 0.5, height_ * 0.1))
            pygame.draw.rect(win, (100, 100, 100),
                             (x_ + width_ * 0.5, y_ + height_ * 0.4, width_ * 0.5, height_ * 0.1))
        elif round((t / t_scale) * 8) % 2 == 1:
            pygame.draw.rect(win, (100, 100, 100),
                             (x_, y_ + height_ * 0.4, width_ * 0.5, height_ * 0.1))
            pygame.draw.rect(win, (p2_siren_blue[0], p2_siren_blue[1], p2_siren_blue[2]),
                             (x_ + width_ * 0.5, y_ + height_ * 0.4, width_ * 0.5, height_ * 0.1))
        if show_ == False:
            pygame.draw.rect(win, (p2_color[0] * 0.3 + river_color[0] * 0.7,
                                   p2_color[1] * 0.3 + river_color[1] * 0.7,
                                   p2_color[2] * 0.3 + river_color[2] * 0.7,
                                   ), (x_, y_, width_, height_))
        # P2 view
        # draw P2 car
        pygame.draw.rect(win, (p2_color[0], p2_color[1], p2_color[2]), (size + x_, yy_, width_, height_))
        if round((t / t_scale) * 8) % 2 == 0:
            pygame.draw.rect(win, (p2_siren_red[0], p2_siren_red[1], p2_siren_red[2]),
                             (size + x_, yy_ + height_ * 0.4, width_ * 0.5, height_ * 0.1))
            pygame.draw.rect(win, (100, 100, 100),
                             (size + x_ + width_ * 0.5, yy_ + height_ * 0.4, width_ * 0.5, height_ * 0.1))
        elif round((t / t_scale) * 8) % 2 == 1:
            pygame.draw.rect(win, (100, 100, 100),
                             (size + x_, yy_ + height_ * 0.4, width_ * 0.5, height_ * 0.1))
            pygame.draw.rect(win, (p2_siren_blue[0], p2_siren_blue[1], p2_siren_blue[2]),
                             (size + x_ + width_ * 0.5, yy_ + height_ * 0.4, width_ * 0.5, height_ * 0.1))
        if show_ == False:
            pygame.draw.rect(win, (p2_color[0] * 0.3 + river_color[0] * 0.7,
                                   p2_color[1] * 0.3 + river_color[1] * 0.7,
                                   p2_color[2] * 0.3 + river_color[2] * 0.7
                                   ), (size + x_, yy_, width_, height_))

    elif p2_car == 'W11':
        # P1 view
        # draw P2 car
        # pygame.draw.rect(win, (100, 100, 100), (x_, y_, width_, height_))
        pygame.draw.rect(win, p2_color, (x_, y_, width_, 0.1 * height_))
        pygame.draw.rect(win, p2_color, (x_, y_ + 0.2 * height_, width_, 0.05 * height_))
        pygame.draw.rect(win, p2_color, (x_ + 0.4 * width_, y_, 0.2 * width_, height_))
        pygame.draw.rect(win, p2_color, (x_ + 0.3 * width_, y_ + 0.2 * height_, 0.4 * width_, height_))
        pygame.draw.rect(win, p2_color, (x_ + 0.2 * width_, y_ + 0.4 * height_, 0.6 * width_, 0.6 * height_))
        pygame.draw.rect(win, p2_color, (x_, y_ + 0.6 * height_, width_, 0.4 * height_))
        pygame.draw.rect(win, p2_color, (x_, y_ + 1.1 * height_, width_, 0.1 * height_))

        pygame.draw.rect(win, tyre_color, (x_, y_ + 0.15 * height_, 0.2 * width_, 0.2 * height_))
        pygame.draw.rect(win, tyre_color, (x_ + 0.8 * width_, y_ + 0.15 * height_, 0.2 * width_, 0.2 * height_))
        pygame.draw.rect(win, tyre_color, (x_, y_ + 0.85 * height_, 0.3 * width_, 0.2 * height_))
        pygame.draw.rect(win, tyre_color, (x_ + 0.7 * width_, y_ + 0.85 * height_, 0.3 * width_, 0.2 * height_))
        if show_ == False:
            pygame.draw.rect(win, p2_color_in_river, (x_, y_, width_, 0.1 * height_))
            pygame.draw.rect(win, p2_color_in_river, (x_, y_ + 0.2 * height_, width_, 0.05 * height_))
            pygame.draw.rect(win, p2_color_in_river, (x_ + 0.4 * width_, y_, 0.2 * width_, height_))
            pygame.draw.rect(win, p2_color_in_river, (x_ + 0.3 * width_, y_ + 0.2 * height_, 0.4 * width_, height_))
            pygame.draw.rect(win, p2_color_in_river, (x_ + 0.2 * width_, y_ + 0.4 * height_, 0.6 * width_, 0.6 * height_))
            pygame.draw.rect(win, p2_color_in_river, (x_, y_ + 0.6 * height_, width_, 0.4 * height_))
            pygame.draw.rect(win, p2_color_in_river, (x_, y_ + 1.1 * height_, width_, 0.1 * height_))

            pygame.draw.rect(win, tyre_color_in_river, (x_, y_ + 0.15 * height_, 0.2 * width_, 0.2 * height_))
            pygame.draw.rect(win, tyre_color_in_river, (x_ + 0.8 * width_, y_ + 0.15 * height_, 0.2 * width_, 0.2 * height_))
            pygame.draw.rect(win, tyre_color_in_river, (x_, y_ + 0.85 * height_, 0.3 * width_, 0.2 * height_))
            pygame.draw.rect(win, tyre_color_in_river, (x_ + 0.7 * width_, y_ + 0.85 * height_, 0.3 * width_, 0.2 * height_))

        # P2 view
        # draw P2 car
        # pygame.draw.rect(win, (100, 100, 100), (size + x_, yy_, width_, height_))
        pygame.draw.rect(win, p2_color, (size + x_, yy_, width_, 0.1 * height_))
        pygame.draw.rect(win, p2_color, (size + x_, yy_ + 0.2 * height_, width_, 0.05 * height_))
        pygame.draw.rect(win, p2_color, (size + x_ + 0.4 * width_, yy_, 0.2 * width_, height_))
        pygame.draw.rect(win, p2_color, (size + x_ + 0.3 * width_, yy_ + 0.2 * height_, 0.4 * width_, height_))
        pygame.draw.rect(win, p2_color, (size + x_ + 0.2 * width_, yy_ + 0.4 * height_, 0.6 * width_, 0.6 * height_))
        pygame.draw.rect(win, p2_color, (size + x_, yy_ + 0.6 * height_, width_, 0.4 * height_))
        pygame.draw.rect(win, p2_color, (size + x_, yy_ + 1.1 * height_, width_, 0.1 * height_))

        pygame.draw.rect(win, tyre_color, (size + x_, yy_ + 0.15 * height_, 0.2 * width_, 0.2 * height_))
        pygame.draw.rect(win, tyre_color, (size + x_ + 0.8 * width_, yy_ + 0.15 * height_, 0.2 * width_, 0.2 * height_))
        pygame.draw.rect(win, tyre_color, (size + x_, yy_ + 0.85 * height_, 0.3 * width_, 0.2 * height_))
        pygame.draw.rect(win, tyre_color, (size + x_ + 0.7 * width_, yy_ + 0.85 * height_, 0.3 * width_, 0.2 * height_))
        if show_ == False:
            pygame.draw.rect(win, p2_color_in_river, (size + x_, yy_, width_, 0.1 * height_))
            pygame.draw.rect(win, p2_color_in_river, (size + x_, yy_ + 0.2 * height_, width_, 0.05 * height_))
            pygame.draw.rect(win, p2_color_in_river, (size + x_ + 0.4 * width_, yy_, 0.2 * width_, height_))
            pygame.draw.rect(win, p2_color_in_river, (size + x_ + 0.3 * width_, yy_ + 0.2 * height_, 0.4 * width_, height_))
            pygame.draw.rect(win, p2_color_in_river, (size + x_ + 0.2 * width_, yy_ + 0.4 * height_, 0.6 * width_, 0.6 * height_))
            pygame.draw.rect(win, p2_color_in_river, (size + x_, yy_ + 0.6 * height_, width_, 0.4 * height_))
            pygame.draw.rect(win, p2_color_in_river, (size + x_, yy_ + 1.1 * height_, width_, 0.1 * height_))

            pygame.draw.rect(win, tyre_color_in_river, (size + x_, yy_ + 0.15 * height_, 0.2 * width_, 0.2 * height_))
            pygame.draw.rect(win, tyre_color_in_river,
                             (size + x_ + 0.8 * width_, yy_ + 0.15 * height_, 0.2 * width_, 0.2 * height_))
            pygame.draw.rect(win, tyre_color_in_river, (size + x_, yy_ + 0.85 * height_, 0.3 * width_, 0.2 * height_))
            pygame.draw.rect(win, tyre_color_in_river,
                             (size + x_ + 0.7 * width_, yy_ + 0.85 * height_, 0.3 * width_, 0.2 * height_))

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # P1 view
    # draw AI car
    pygame.draw.rect(win, (10, 0, 200), (x_a, y_a, width, height))
    pygame.draw.rect(win, (10, 50, 120), (x_b, y_b, width, height))

    # P2 view
    # draw AI car
    pygame.draw.rect(win, (10, 0, 200), (size + x_a, y_a_, width, height))
    pygame.draw.rect(win, (10, 50, 120), (size + x_b, y_b_, width, height))

    # P1 view
    # draw light poles
    pygame.draw.rect(win, (125, 125, 125), (x_2, y_5, pole_width, pole_height))
    pygame.draw.rect(win, (125, 125, 125), (size - x_2 - pole_width, y_5, pole_width, pole_height))

    # P2 view
    # draw light poles
    pygame.draw.rect(win, (125, 125, 125), (size + x_2, y_5_, pole_width, pole_height))
    pygame.draw.rect(win, (125, 125, 125), (size + size - x_2 - pole_width, y_5_, pole_width, pole_height))

    # draw trees
    # P1 view
    # left hand side
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_1, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_2, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_3, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_4, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_5, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_6, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_7, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_8, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_9, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_10, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_11, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_12, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_13, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_14, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_15, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (x_1, y_16, tree_width, tree_height))
    # P2 view
    # left hand side
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_1_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_2_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_3_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_4_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_5_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_6_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_7_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_8_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_9_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_10_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_11_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_12_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_13_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_14_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_15_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + x_1, y_16_, tree_width, tree_height))

    # P1 view
    # right hand side
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_1, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_2, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_3, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_4, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_5, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_6, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_7, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_8, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_9, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_10, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_11, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_12, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_13, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_14, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_15, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size - x_1 - tree_width, y_16, tree_width, tree_height))
    # P2 view
    # right hand side
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_1_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_2_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_3_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_4_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_5_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_6_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_7_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_8_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_9_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_10_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_11_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_12_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_13_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_14_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_15_, tree_width, tree_height))
    pygame.draw.rect(win, (0, 125, 0), (size + size - x_1 - tree_width, y_16_, tree_width, tree_height))

    # draw a white strip at the top
    # P1 view
    pygame.draw.rect(win, (210, 210, 210), (0, 0, size, tree_height))
    # P2 view
    pygame.draw.rect(win, (210, 210, 210), (size, 0, size, tree_height))

    # update time
    t += 1

    # show time elapsed
    myfont_t = pygame.font.SysFont("monospace", 20)
    if round(t / t_scale, 1) < 10:
        label_t = myfont_t.render(" Time:     " + str(round(t / t_scale, 1)) + " s", 1, (255, 255, 255))
    elif round(t / t_scale, 1) >= 10 and round(t / t_scale, 1) < 100:
        label_t = myfont_t.render(" Time:    " + str(round(t / t_scale, 1)) + " s", 1, (255, 255, 255))
    elif round(t / t_scale, 1) >= 100 and round(t / t_scale, 1) < 1000:
        label_t = myfont_t.render(" Time:   " + str(round(t / t_scale, 1)) + " s", 1, (255, 255, 255))
    elif round(t / t_scale, 1) >= 1000 and round(t / t_scale, 1) < 10000:
        label_t = myfont_t.render(" Time:  " + str(round(t / t_scale, 1)) + " s", 1, (255, 255, 255))
    elif round(t / t_scale, 1) >= 10000 and round(t / t_scale, 1) < 100000:
        label_t = myfont_t.render(" Time: " + str(round(t / t_scale, 1)) + " s", 1, (255, 255, 255))
    elif round(t / t_scale, 1) >= 100000:
        label_t = myfont_t.render(" Time:" + str(round(t / t_scale, 1)) + " s", 1, (255, 255, 255))
    # P1 view timer
    win.blit(label_t, (300, size - 90))
    # P2 view timer
    win.blit(label_t, (size + 300, size - 90))

    # P1
    # show speed
    myfont = pygame.font.SysFont("monospace", 20)
    if round(vel * 10 * scale) < 10:
        label = myfont.render("Speed:   " + str(round(vel * 10 * scale)) + " km/h", 1, (255, 255, 255))
    elif round(vel * 10 * scale) >= 10 and round(vel * 10 * scale) < 100:
        label = myfont.render("Speed:  " + str(round(vel * 10 * scale)) + " km/h", 1, (255, 255, 255))
    elif round(vel * 10 * scale) >= 100:
        label = myfont.render("Speed: " + str(round(vel * 10 * scale)) + " km/h", 1, (255, 255, 255))
    win.blit(label, (45, size - 30))
    # show gear
    myfont = pygame.font.SysFont("monospace", 20)
    label = myfont.render("                " + "(" + str(gear) + ")", 1, (255, 255, 100))
    win.blit(label, (45, size - 30))
    # show cruise control speed setting (if there is one)
    if cruise_control == True:
        myfont = pygame.font.SysFont("monospace", 20)
        if round(- constant * 10 * scale) < 100:
            label = myfont.render("Speed:  " + str(round(- constant * 10 * scale)) + " km/h", 1, (180, 180, 180))
        elif round(- constant * 10 * scale) >= 100:
            label = myfont.render("Speed: " + str(round(- constant * 10 * scale)) + " km/h", 1, (180, 180, 180))
        win.blit(label, (300, size - 120))
    # show n2o reserve
    myfont = pygame.font.SysFont("monospace", 20)
    if round((n2o_quantity / full_n2o_quantity) * 100) == 100:
        label = myfont.render("  N\u2082O: " + str(round((n2o_quantity / full_n2o_quantity) * 100)) + " %", 1, (255, 255, 255))
    elif round((n2o_quantity / full_n2o_quantity) * 100) < 100 and round((n2o_quantity / full_n2o_quantity) * 100) >= 10:
        label = myfont.render("  N\u2082O:  " + str(round((n2o_quantity / full_n2o_quantity) * 100)) + " %", 1, (255, 255, 255))
    elif round((n2o_quantity / full_n2o_quantity) * 100) < 10:
        label = myfont.render("  N\u2082O:   " + str(round((n2o_quantity / full_n2o_quantity) * 100)) + " %", 1, (255, 255, 255))
    win.blit(label, (45, size - 90))
    pygame.draw.rect(win, (180, 180, 255), (45, size - 100, (n2o_quantity / full_n2o_quantity) * 100 * 1.8, 5))
    # show turbo boost availability (by blinking)
    if turbo_boost_option == True and round((t / t_scale) * 4) % 2 == 0:
        myfont = pygame.font.SysFont("monospace", 20)
        label = myfont.render("                (T)", 1, (180, 255, 180))
        win.blit(label, (45, size - 90))
    elif turbo_boost_option == True and t - turbo_reboot_t > 3 * t_scale:
        myfont = pygame.font.SysFont("monospace", 20)
        label = myfont.render("                (T)", 1, (180, 255, 180))
        win.blit(label, (45, size - 90))
    # show life value and life bar
    myfont = pygame.font.SysFont("monospace", 20)
    if round(life, 1) == 100:
        label = myfont.render(" Life: " + str(100.0) + " %", 1, (255, 255, 255))
    elif round(life, 1) == 10:
        label = myfont.render(" Life:  " + '10.0' + " %", 1, (255, 255, 255))
    elif round(life, 1) < 100 and round(life, 1) > 10:
        label = myfont.render(" Life:  " + str(round(life, 1)) + " %", 1, (255, 255, 255))
    elif round(life, 1) < 10:
        label = myfont.render(" Life:   " + str(round(life, 1)) + " %", 1, (255, 255, 255))
    win.blit(label, (45, size - 55))
    pygame.draw.rect(win, (200, 100, 100), (45, size - 65, life * 1.8, 5))
    # show battery reserve
    myfont = pygame.font.SysFont("monospace", 20)
    if round((battery / full_battery) * 100) == 100:
        label = myfont.render("  Bat: " + str(round((battery / full_battery) * 100)) + " %", 1, (255, 255, 255))
    elif round((battery / full_battery) * 100) < 100 and round((battery / full_battery) * 100) >= 10:
        label = myfont.render("  Bat:  " + str(round((battery / full_battery) * 100)) + " %", 1, (255, 255, 255))
    elif round((battery / full_battery) * 100) < 10:
        label = myfont.render("  Bat:   " + str(round((battery / full_battery) * 100)) + " %", 1, (255, 255, 255))
    win.blit(label, (45, size - 125))
    pygame.draw.rect(win, (0, 206, 209), (45, size - 135, (battery / full_battery) * 100 * 1.8, 5))
    # show battery deployment mode
    myfont = pygame.font.SysFont("monospace", 20)
    label = myfont.render("                " + "(" + mode.upper() + ")", 1, (135, 206, 235))
    win.blit(label, (45, size - 125))
    # show DRS if it is W11
    if p1_car == 'W11':
        if drs_open == True:
            myfont = pygame.font.SysFont("monospace", 20)
            label = myfont.render("                (DRS)", 1, (0, 161, 156))
            win.blit(label, (40, size - 55))


    # P2
    # show speed
    myfont_ = pygame.font.SysFont("monospace", 20)
    if round(vel_ * 10 * scale) < 10:
        label_ = myfont_.render("Speed:   " + str(round(vel_ * 10 * scale)) + " km/h", 1, (255, 255, 255))
    elif round(vel_ * 10 * scale) >= 10 and round(vel_ * 10 * scale) < 100:
        label_ = myfont_.render("Speed:  " + str(round(vel_ * 10 * scale)) + " km/h", 1, (255, 255, 255))
    elif round(vel_ * 10 * scale) >= 100:
        label_ = myfont_.render("Speed: " + str(round(vel_ * 10 * scale)) + " km/h", 1, (255, 255, 255))
    win.blit(label_, (size + 45, size - 30))
    # show gear
    myfont_ = pygame.font.SysFont("monospace", 20)
    label_ = myfont_.render("                " + "(" + str(gear_) + ")", 1, (255, 255, 100))
    win.blit(label_, (size + 45, size - 30))
    # show cruise control speed setting (if there is one)
    if cruise_control_ == True:
        myfont_ = pygame.font.SysFont("monospace", 20)
        if round(- constant_ * 10 * scale) < 100:
            label_ = myfont_.render("Speed:  " + str(round(- constant_ * 10 * scale)) + " km/h", 1, (180, 180, 180))
        elif round(- constant_ * 10 * scale) >= 100:
            label_ = myfont_.render("Speed: " + str(round(- constant_ * 10 * scale)) + " km/h", 1, (180, 180, 180))
        win.blit(label_, (size + 300, size - 120))
    # show n2o reserve
    myfont_ = pygame.font.SysFont("monospace", 20)
    if round((n2o_quantity_ / full_n2o_quantity_) * 100) == 100:
        label_ = myfont_.render("  N\u2082O: " + str(round((n2o_quantity_ / full_n2o_quantity_) * 100)) + " %", 1, (255, 255, 255))
    elif round((n2o_quantity_ / full_n2o_quantity_) * 100) < 100 and round((n2o_quantity_ / full_n2o_quantity_) * 100) >= 10:
        label_ = myfont_.render("  N\u2082O:  " + str(round((n2o_quantity_ / full_n2o_quantity_) * 100)) + " %", 1, (255, 255, 255))
    elif round((n2o_quantity_ / full_n2o_quantity_) * 100) < 10:
        label_ = myfont_.render("  N\u2082O:   " + str(round((n2o_quantity_ / full_n2o_quantity_) * 100)) + " %", 1, (255, 255, 255))
    win.blit(label_, (size + 45, size - 90))
    pygame.draw.rect(win, (180, 180, 255), (size + 45, size - 100, (n2o_quantity_ / full_n2o_quantity_) * 100 * 1.8, 5))
    # show turbo boost availability (by blinking)
    if turbo_boost_option_ == True and round((t / t_scale) * 4) % 2 == 0:
        myfont_ = pygame.font.SysFont("monospace", 20)
        label_ = myfont_.render("                (T)", 1, (180, 255, 180))
        win.blit(label_, (size + 45, size - 90))
    elif turbo_boost_option_ == True and t - turbo_reboot_t_ > 3 * t_scale:
        myfont_ = pygame.font.SysFont("monospace", 20)
        label_ = myfont_.render("                (T)", 1, (180, 255, 180))
        win.blit(label_, (size + 45, size - 90))
    # show life value and life bar
    myfont_ = pygame.font.SysFont("monospace", 20)
    if round(life_, 1) == 100:
        label_ = myfont_.render(" Life: " + str(100.0) + " %", 1, (255, 255, 255))
    elif round(life_, 1) == 10:
        label_ = myfont_.render(" Life:  " + '10.0' + " %", 1, (255, 255, 255))
    elif round(life_, 1) < 100 and round(life_, 1) > 10:
        label_ = myfont_.render(" Life:  " + str(round(life_, 1)) + " %", 1, (255, 255, 255))
    elif round(life_, 1) < 10:
        label_ = myfont_.render(" Life:   " + str(round(life_, 1)) + " %", 1, (255, 255, 255))
    win.blit(label_, (size + 45, size - 55))
    pygame.draw.rect(win, (200, 100, 100), (size + 45, size - 65, life_ * 1.8, 5))
    # show battery reserve
    myfont_ = pygame.font.SysFont("monospace", 20)
    if round((battery_ / full_battery_) * 100) == 100:
        label_ = myfont_.render("  Bat: " + str(round((battery_ / full_battery_) * 100)) + " %", 1, (255, 255, 255))
    elif round((battery_ / full_battery_) * 100) < 100 and round((battery_ / full_battery_) * 100) >= 10:
        label_ = myfont_.render("  Bat:  " + str(round((battery_ / full_battery_) * 100)) + " %", 1, (255, 255, 255))
    elif round((battery_ / full_battery_) * 100) < 10:
        label_ = myfont_.render("  Bat:   " + str(round((battery_ / full_battery_) * 100)) + " %", 1, (255, 255, 255))
    win.blit(label_, (size + 45, size - 125))
    pygame.draw.rect(win, (0, 206, 209), (size + 45, size - 135, (battery_ / full_battery_) * 100 * 1.8, 5))
    # show gear
    myfont_ = pygame.font.SysFont("monospace", 20)
    label_ = myfont_.render("                " + "(" + mode_.upper() + ")", 1, (135, 206, 235))
    win.blit(label_, (size + 45, size - 125))
    # show DRS if it is W11
    if p2_car == 'W11':
        if drs_open_ == True:
            myfont_ = pygame.font.SysFont("monospace", 20)
            label_ = myfont_.render("                (DRS)", 1, (0, 161, 156))
            win.blit(label_, (size + 40, size - 55))





    # P1 view
    # show distance travelled
    myfont_1 = pygame.font.SysFont("monospace", 20)
    label_1 = myfont_1.render("Distance: " + str(round(distance * 188.4 / (800 * 1000) , 1)) + " km", 1, (255, 255, 255))
    win.blit(label_1, (300, size - 30))

    # P2 view
    # show distance travelled
    myfont_1_ = pygame.font.SysFont("monospace", 20)
    label_1_ = myfont_1_.render("Distance: " + str(round(distance_ * 188.4 / (800 * 1000) , 1)) + " km", 1, (255, 255, 255))
    win.blit(label_1_, (size + 300, size - 30))

    # P1 view
    # show car separation
    myfont_1 = pygame.font.SysFont("monospace", 20)
    label_1 = myfont_1.render(" Car gap: " + str(round(separation * 188.4 / (800))) + " m", 1, (180, 180, 180))
    win.blit(label_1, (300, size - 60))

    # P2 view
    # show car separation
    myfont_1_ = pygame.font.SysFont("monospace", 20)
    label_1_ = myfont_1_.render(" Car gap: " + str(round(separation_ * 188.4 / (800))) + " m", 1, (180, 180, 180))
    win.blit(label_1_, (size + 300, size - 60))

    # splitscreen divider
    pygame.draw.rect(win, (0, 0, 0), (size - divider_width, 0, divider_width, size))
    pygame.draw.rect(win, (0, 0, 0), (size, 0, divider_width, size))

    pygame.display.update()

pygame.quit()